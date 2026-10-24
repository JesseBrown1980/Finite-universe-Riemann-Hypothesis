#!/usr/bin/env python3
"""Fail-closed read-only Host8 375-sector scanner.

Default mode: verify every sector's FILE SIZE and sample 96+96 rooms per sector.
This reads approximately 576 KB of room payload (plus the six prefix anchors);
it does NOT hash or read all 300 GB. Use --hash-entire-volume to additionally
read/hash each byte of all 375 files. Results identify the chosen scan mode.
"""
from __future__ import annotations
import argparse
from collections import Counter
import csv
from datetime import datetime, timezone
import hashlib
from pathlib import Path
import struct
import time
from host8_ternary_weil import EXPECTED, trits, nonsingular, Field, MODULI, zeta
from verify_geometric_hasse_witt import hasse_witt_invariants

SECTORS=375
SECTOR_BYTES=800_000_000
ROOM_BYTES=8
CANONICAL_ROOMS=110_592
DEEP_ROOMS=100_000_000
SAMPLES_PER_GRID=96

def sample_offsets(room_span: int, count: int):
    assert room_span>=count>=2
    return tuple(j*(room_span-1)//(count-1) for j in range(count))

def build_codebook():
    fields=[Field(n,p) for n,p in enumerate(MODULI,start=1)]
    table={}
    for code in range(243):
        coeff=trits(code,5)
        if nonsingular(coeff):
            result=zeta(code,fields)
            assert result is not None and result[3]
            a0,a1,a2,a3,a4=coeff
            tr,det,p_rank=hasse_witt_invariants(a1,a2,a4)
            A,B=result[1],result[2]
            assert tr==(-A)%3 and det==B%3
            table[code]=p_rank
        else:
            table[code]=None
    assert sum(x is not None for x in table.values())==162
    return table

def count_samples(f, span: int, samples: int, codebook: dict):
    freq=Counter()
    payload=hashlib.sha256()
    for room in sample_offsets(span,samples):
        f.seek(room*ROOM_BYTES)
        data=f.read(ROOM_BYTES)
        if len(data)!=ROOM_BYTES:
            raise ValueError(f"Short read at room offset {room}")
        payload.update(data)
        code=struct.unpack('<Q',data)[0]%243
        rank=codebook[code]
        freq['rooms']+=1
        if rank is not None:
            freq['smooth']+=1
            freq['rh_pass']+=1
            freq['p_rank_'+str(rank)]+=1
    return freq,payload.hexdigest()

def digest_bytes(file, length: int):
    d=hashlib.sha256()
    remaining=length
    while remaining:
        part=file.read(min(1024*1024,remaining))
        if not part:
            raise ValueError('File truncated while hashing')
        d.update(part)
        remaining-=len(part)
    return d.hexdigest()

def scan(directory: Path, ids: tuple[int,...], size: int, canonical: int, deep: int,
         samples: int, hash_entire_volume: bool, require_anchor: bool):
    start=time.monotonic()
    codebook=build_codebook()
    rows=[]
    totals={name:Counter() for name in ('canonical','deep')}
    for sector in ids:
        filename=f'sector-{sector:03d}.rooms'
        file=directory/filename
        if not file.is_file():
            raise FileNotFoundError(f"Missing expected sector: {file}")
        stat=file.stat()
        if stat.st_size!=size:
            raise ValueError(f"Incorrect sector size {filename}: {stat.st_size} != {size}")
        anch=EXPECTED.get(f'{sector:03d}') if require_anchor else None
        with file.open('rb',buffering=1024*1024) as f:
            if anch:
                for length,sha in zip((110_592,884_736),anch):
                    if size<length:raise ValueError('Anchored sector shorter than required prefix')
                    f.seek(0)
                    if digest_bytes(f,length)!=sha:
                        raise ValueError(f"SHA256 mismatch for {filename}: {length} bytes")
            digests={}
            for name,span in (('canonical',canonical),('deep',deep)):
                frequencies,payload_hash=count_samples(f,span,samples,codebook)
                totals[name].update(frequencies)
                digests[name]=payload_hash
                rows.append(dict(sector=f'{sector:03d}',grid=name,
                                 **{key:frequencies.get(key,0)
                                    for key in ('rooms','smooth','rh_pass','p_rank_2','p_rank_1','p_rank_0')},
                                 sample_payload_sha256=payload_hash))
            if hash_entire_volume:
                f.seek(0)
                digests['full_sector_sha256']=digest_bytes(f,size)
            # Report full-sector digest separately only when actually computed.
            if hash_entire_volume:
                for row in rows[-2:]:
                    row['full_sector_sha256']=digests['full_sector_sha256']
    summary=[]
    for name in ('canonical','deep'):
        counts=totals[name]
        assert counts['smooth']==counts['rh_pass']
        assert counts['smooth']==sum(counts['p_rank_'+str(n)] for n in range(3))
        summary.append(dict(grid=name,**{key:counts.get(key,0) for key in
                        ('rooms','smooth','rh_pass','p_rank_2','p_rank_1','p_rank_0')}))
    combined=totals['canonical']+totals['deep']
    assert combined['rooms']==len(ids)*2*samples
    assert combined['smooth']==sum(combined['p_rank_'+str(i)] for i in range(3))
    distinct_offsets=len(set(sample_offsets(canonical,samples)) |
                         set(sample_offsets(deep,samples)))
    summary.append(dict(grid='combined',**{key:combined.get(key,0) for key in
                        ('rooms','smooth','rh_pass','p_rank_2','p_rank_1','p_rank_0')}))
    metadata=dict(generated_utc=datetime.now(timezone.utc).isoformat(),
                  provenance='live_read_only_from_specified_files',
                  mode='full_byte_hash_plus_sampling' if hash_entire_volume else 'distributed_room_sampling_and_file_size',
                  sectors=len(ids),sector_bytes=size,physical_bytes_verified_by_stat=len(ids)*size,
                  sampled_room_reads=combined['rooms'],
                  unique_sampled_room_positions=len(ids)*distinct_offsets,
                  sampled_bytes_read=combined['rooms']*8,
                  full_volume_bytes_hashed=len(ids)*size if hash_entire_volume else 0,
                  anchor_prefix_sha256_checked=int(require_anchor),
                  elapsed_seconds=round(time.monotonic()-start,3))
    return rows,summary,metadata

def write_csv(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',newline='') as out:
        w=csv.DictWriter(out,fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--host8-dir',type=Path,required=True)
    p.add_argument('--output-dir',type=Path,default=Path(__file__).parent/'results')
    p.add_argument('--sectors',type=int,default=375)
    p.add_argument('--sector-ids',type=str,
                   help='Comma-delimited sector IDs for explicitly scoped tests')
    p.add_argument('--sector-bytes',type=int,default=SECTOR_BYTES)
    p.add_argument('--canonical-rooms',type=int,default=CANONICAL_ROOMS)
    p.add_argument('--deep-rooms',type=int,default=DEEP_ROOMS)
    p.add_argument('--samples-per-grid',type=int,default=SAMPLES_PER_GRID)
    p.add_argument('--hash-entire-volume',action='store_true',
                   help='Sequentially hash every byte of selected sector files')
    p.add_argument('--no-anchor-check',action='store_true',
                   help='Only for non-Host8 synthetic fixtures; never use for production')
    a=p.parse_args()
    ids=tuple(map(int,a.sector_ids.split(','))) if a.sector_ids else tuple(range(a.sectors))
    if len(set(ids))!=len(ids) or not ids or any(x<0 or x>=375 for x in ids):
        p.error('Invalid sector IDs')
    if (not a.no_anchor_check) and a.sector_bytes<884736:
        p.error('Anchored verification requires 884736 bytes')
    if a.canonical_rooms*8>a.sector_bytes or a.deep_rooms*8>a.sector_bytes:
        p.error('Sampling grid exceeds sector size')
    rows,summary,metadata=scan(a.host8_dir,ids,a.sector_bytes,
                   a.canonical_rooms,a.deep_rooms,a.samples_per_grid,
                   a.hash_entire_volume,not a.no_anchor_check)
    write_csv(a.output_dir/'host8_375sectors_scan_per_sector.csv',rows)
    write_csv(a.output_dir/'host8_375sectors_scan_summary.csv',
              [dict(metadata,**x) for x in summary])
    print('PASS:',metadata)
    for s in summary:print(s)
    print('NOTE: per-sector files were size-checked, NOT fully read, unless --hash-entire-volume was enabled.')

if __name__=='__main__':
    main()
