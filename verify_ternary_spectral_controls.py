#!/usr/bin/env python3
"""Reproducible finite-field spectral controls + shared Host8 inputs.
This verifies modular symmetries; it does NOT prove classical RH.
Input authentication covers three published slices, not the 300 GB volume.
"""
import argparse
import csv
from pathlib import Path
import hashlib
import struct
from host8_ternary_weil import read_host8, read_manifest

P, K, W = 1_000_081, 27, 951_846
PRIMES = (2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103)
HALF = (P + 1) // 2

def random_ladder():
    seed = 20261024
    out = []
    for _ in range(K):
        seed = (1103515245 * seed + 12345) % (2**31)
        out.append(1 + seed % (P-1))
    return tuple(out)

def ladders():
    unchanged_unused = list(PRIMES)
    for i in [0, *range(14,27)]:
        unchanged_unused[i] = 1
    return {
        'primes': PRIMES,
        'reversed_primes': tuple(reversed(PRIMES)),
        'random_lcg_seed_20261024': random_ladder(),
        'all_ones': (1,) * K,
        'unused_14_set_to_one': tuple(unchanged_unused),
    }

def generator_coefficients(weights):
    assert len(weights) == K
    c = [0]*K
    for d in range(1,14):
        value = (pow(W,d,P)-pow(W,K-d,P))*weights[d] % P
        c[d], c[K-d] = value, -value % P
    return c

def spectrum(c):
    mu = [sum(c[d]*pow(W,(k*d)%K,P) for d in range(K)) % P for k in range(K)]
    return mu

def modal_transform(vec):
    return [sum(v*pow(W,k*i,P) for i,v in enumerate(vec))%P for k in range(K)]

def apply_generator(c, vec):
    return [sum(c[(j-i)%K]*vec[j] for j in range(K))%P for i in range(K)]

def trace_controls():
    out = []
    ref = None
    for name,weights in ladders().items():
        c = generator_coefficients(weights)
        mu = spectrum(c)
        lambdas = [(HALF+x)%P for x in mu]
        assert mu[0] == 0
        assert all((mu[k]+mu[-k%K])%P==0 for k in range(K))
        assert all((lambdas[k]+lambdas[-k%K])%P==1 for k in range(K))
        assert sum(mu)%P == 0 and sum(pow(x,3,P) for x in mu)%P == 0
        if name == 'primes':
            ref = mu
            assert sum(pow(x,2,P) for x in mu)%P == 885145
            assert sum(pow(x,4,P) for x in mu)%P == 987346
        if name == 'unused_14_set_to_one':
            assert mu == ref, 'unused prime entries must leave spectrum unchanged'
        out.append({
          'control':name, 'trace_T2':sum(pow(x,2,P) for x in mu)%P,
          'trace_T4':sum(pow(x,4,P) for x in mu)%P,
          'law0_all_states':1, 'lambda_pairing_all_27':1,
          'same_spectrum_as_original':int(mu==ref),
          'weights':';'.join(map(str,weights))
        })
    assert [x['same_spectrum_as_original'] for x in out] == [1,0,0,0,1]
    return out

def host8_rows(directory, manifest_path):
    if directory is None:
        raise ValueError('Host8 input directory is required: refuse to fake spectral readbacks')
    manifest = read_manifest(manifest_path)
    records = read_host8(directory)
    assert records == manifest, 'readback must match the 288 published Host8 seeds'
    c = generator_coefficients(PRIMES)
    mu = spectrum(c)
    from_csv = manifest_path.parents[1] / 'results' / 'host8_curve_results.csv'
    with from_csv.open(newline='') as f:
        curve_rows = list(csv.DictReader(f))
    assert len(curve_rows) == len(records)
    out = []
    for index,(sec,j,cell,code) in enumerate(records):
        assert (curve_rows[index]['sector'],int(curve_rows[index]['sample'])) == (sec,j)
        raw = (directory / ('sector-'+sec+'.rooms')).read_bytes()
        word = struct.unpack_from('<Q', raw, cell*8)[0]
        vals=[]
        for _ in range(K):
            digit = word % 3
            vals.append((digit-1)%P)
            word //= 3
        X = modal_transform(vals)
        Tv = apply_generator(c,vals)
        Y = modal_transform(Tv)
        assert Y[0] == 0 and all(Y[k] == mu[-k%K]*X[k]%P for k in range(K))
        out.append({
          'sector':sec,'sample':j,'cell_index':cell,'code243':code,
          'zeta_P1':curve_rows[index]['P1'],'zeta_P2':curve_rows[index]['P2'],
          'X0':X[0],'Y0':Y[0],
          'X1':X[1],'X26':X[26],'Y1':Y[1],'Y26':Y[26]
        })
    assert len(out)==288 and all(x['Y0']==0 for x in out)
    return out

def write_csv(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',newline='') as f:
        writer=csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--host8-dir',type=Path)
    p.add_argument('--output-dir',type=Path,default=Path(__file__).parent/'results')
    p.add_argument('--manifest',type=Path,default=Path(__file__).parent/'data'/'host8_seed_manifest.csv')
    a=p.parse_args()
    controls=trace_controls()
    write_csv(a.output_dir/'spectral_falsification_controls.csv',controls)
    print('PASS: five distinct control definitions; all obey structural symmetries')
    if a.host8_dir:
        rows=host8_rows(a.host8_dir,a.manifest)
        write_csv(a.output_dir/'host8_spectral_common_inputs.csv',rows)
        print('PASS: 288 authenticated Host8-seeded vectors, 7776 Fourier diagonalization checks')
    else:
        print('Host8 mode skipped (no --host8-dir provided); no Host8 measurement asserted')

if __name__=='__main__':
    main()
