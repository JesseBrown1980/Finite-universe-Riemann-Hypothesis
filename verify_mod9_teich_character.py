#!/usr/bin/env python3
"""Phase 5A: coefficient-only Teichmueller quadratic-character mod-9 controls.

This is NOT Monsky-Washnitzer Frobenius cohomology. It computes modular
quadratic-character traces directly from the curve's defining coefficients
over F3 and F9, without enumerating (x,y) pairs or using prior zeta data
as construction inputs.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import struct
from pathlib import Path
from host8_ternary_weil import EXPECTED, read_manifest, trits, nonsingular

ROOT = Path(__file__).resolve().parent

# F9 = F3[u] / (u^2 + 1), encode a+b*u as a+3*b.
def add9(x: int, y: int) -> int:
    return (x%3+y%3)%3 + 3*((x//3+y//3)%3)

def mul9(x: int, y: int) -> int:
    a,b=x%3,x//3
    c,d=y%3,y//3
    return (a*c-b*d)%3 + 3*((a*d+b*c)%3)

def pow9(x: int, n: int) -> int:
    result=1
    while n:
        if n&1: result=mul9(result,x)
        x=mul9(x,x)
        n//=2
    return result

def f3(coeff: tuple[int,...], x: int) -> int:
    acc=1
    for a in reversed(coeff):
        acc=(acc*x+a)%3
    return acc

def f9(coeff: tuple[int,...], x: int) -> int:
    acc=1
    for a in reversed(coeff):
        acc=add9(mul9(acc,x),a)
    return acc

def chi3(x: int) -> int:
    assert 0<=x<3
    return (0,1,-1)[x]

def chi9(x: int) -> int:
    z=pow9(x,4)
    assert z in (0,1,2), (x,z)
    return chi3(z)

def teich9(r: int) -> int:
    """Teichmueller lift from F3 to Z/9, 0->0, 1->1, 2->8."""
    return pow(r,3,9)

def polynomial_only_invariants(code: int) -> dict:
    coeff=trits(code,5)
    assert nonsingular(coeff)
    r1=[f3(coeff,x) for x in range(3)]
    r2=[pow9(f9(coeff,x),4) for x in range(9)]
    a9=sum(teich9(x) for x in r1)%9
    s29=sum(teich9(x) for x in r2)%9
    b9=(a9*a9+s29)*5%9  # 2^(-1) mod 9 = 5.
    s1=sum(chi3(x) for x in r1)
    s2=sum(chi3(x) for x in r2)
    assert (s1*s1+s2)%2==0
    A=s1
    B=(s1*s1+s2)//2
    assert A%9==a9 and B%9==b9
    a0,a1,a2,a3,a4=coeff
    assert A%3==(-(a2+a4))%3
    assert B%3==(a2*a4-a1)%3
    naive_A9=(-(a2+a4))%9
    naive_B9=(a2*a4-a1)%9
    recovered_A=a9 if a9<=3 else a9-9
    assert recovered_A==A
    return {'code243':code,'a0':a0,'a1':a1,'a2':a2,'a3':a3,'a4':a4,
            'A_from_coeff':A,'B_from_coeff':B,'A_mod9':a9,'B_mod9':b9,
            'A_from_mod9':recovered_A,
            'naive_A_mod9':naive_A9,'naive_B_mod9':naive_B9,
            'naive_A_match':int(naive_A9==a9),
            'naive_B_match':int(naive_B9==b9),
            'N1_quadratic_char_sum':s1,'N2_quadratic_char_sum':s2}

def get_host8_records(host8_dir: Path, manifest: list[tuple]) -> list[tuple]:
    out=[]
    for sec,ref_hashes in EXPECTED.items():
        with (host8_dir/('sector-'+sec+'.rooms')).open('rb') as f:
            raw=f.read(884736)
        assert len(raw)==884736, ('short sector',sec)
        assert hashlib.sha256(raw[:110592]).hexdigest()==ref_hashes[0], ('bad L24 sector hash',sec)
        assert hashlib.sha256(raw).hexdigest()==ref_hashes[1], ('bad L48 sector hash',sec)
        for entry in manifest:
            if entry[0]!=sec: continue
            _sec,j,cell,_code=entry
            value=struct.unpack_from('<Q',raw,cell*8)[0]%243
            out.append((sec,j,cell,value))
    assert out==manifest, 'Host8 binary readback differs from pinned seed manifest'
    return out

def write_table(path: Path, rows: list[dict]):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--curves',type=Path,default=ROOT/'results'/'all_quintics.csv')
    p.add_argument('--manifest',type=Path,default=ROOT/'data'/'host8_seed_manifest.csv')
    p.add_argument('--host8-dir',type=Path)
    p.add_argument('--output-dir',type=Path,default=ROOT/'results')
    a=p.parse_args()
    with a.curves.open(newline='') as f:
        known=list(csv.DictReader(f))
    assert len(known)==243
    curves=[]
    for r in known:
        code=int(r['code243'])
        if r['smooth_genus2']!='1':continue
        x=polynomial_only_invariants(code)
        assert x['A_from_coeff']==int(r['P1'])
        assert x['B_from_coeff']==int(r['P2'])
        curves.append(x)
    assert len(curves)==162
    manifest=read_manifest(a.manifest)
    if a.host8_dir:
        manifest=get_host8_records(a.host8_dir,manifest)
        print('PASS: six hashes of three Host8 sector prefixes, verified byte-for-byte')
    else:
        print('Manifest-only mode: no physical Host8 bytes opened this run')
    by_code={r['code243']:r for r in curves}
    host=[]
    for sec,j,cell,code in manifest:
        row={'sector':sec,'sample':j,'cell_index':cell,'code243':code,
             'smooth_genus2':int(code in by_code)}
        if code in by_code:
            row.update({k:v for k,v in by_code[code].items() if k!='code243'})
        else:
            row.update({k:'' for k in curves[0] if k!='code243'})
        host.append(row)
    assert len(host)==288 and sum(r['smooth_genus2'] for r in host)==194
    assert sum(r['naive_A_match'] for r in curves)==60
    assert sum(r['naive_B_match'] for r in curves)==47
    write_table(a.output_dir/'teich_mod9_curve_controls.csv',curves)
    write_table(a.output_dir/'host8_teich_mod9_controls.csv',host)
    print('PASS: 162/162 smooth quintics and 194/194 Host8 smooth observations')
    print('FALSIFICATION: naive entrywise Hasse-Witt lift agrees for A:60/162 and B:47/162')
    print('LIMIT: character-sum trace control, NOT Monsky-Washnitzer Frobenius lift')

if __name__=='__main__':
    main()
