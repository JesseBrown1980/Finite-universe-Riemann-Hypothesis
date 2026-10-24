#!/usr/bin/env python3
"""Finite two-term genus-two Frobenius matrix candidate modulo 9.

This calculation does not import point-count tables. It applies exact finite
rational differential reductions to the first two terms of the Frobenius
pullback, then projects a stable 3-integral 4x4 lattice to Z/9Z.

The resulting 162/162 match with counted zeta polynomials is a finite
exhaustive experiment, NOT a proof the omitted infinite p-adic tail vanishes.
"""
from __future__ import annotations
import argparse
import csv
from pathlib import Path
from finite_frobenius_mod9 import compute,mod9,Q
from host8_ternary_weil import nonsingular,trits

ROOT=Path(__file__).resolve().parent
SCALE=(1,1,1,3)

def curves():
    out={}
    for code in range(243):
        coeff=trits(code,5)
        if not nonsingular(coeff):continue
        m,cp=compute(coeff,terms=2)
        matrix=[[mod9(m[j][i]*Q(SCALE[i],SCALE[j])) for i in range(4)] for j in range(4)]
        out[code]={'code243':code,**{'a'+str(i):c for i,c in enumerate(coeff)},
                   **{'F'+str(j)+str(i):matrix[j][i] for j in range(4) for i in range(4)},
                   **{'P'+str(i)+'_mod9':mod9(cp[i]) for i in range(1,5)}}
    assert len(out)==162
    return out

def emit(path,rows):
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=tuple(rows[0]))
        w.writeheader()
        w.writerows(rows)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--manifest',type=Path,default=ROOT/'data'/'host8_seed_manifest.csv')
    p.add_argument('--output-dir',type=Path,default=ROOT/'results')
    args=p.parse_args()
    table=curves()
    with args.manifest.open(newline='') as f:
        manifest=list(csv.DictReader(f))
    assert len(manifest)==288
    linked=[]
    for r in manifest:
        code=int(r['code243'])
        result=table.get(code)
        linked.append({'sector':r['sector'],'sample':r['sample'],
                       'cell_index':r['cell_index'],'code243':code,
                       'smooth_genus2':int(result is not None),
                       **{name:result[name] if result is not None else ''
                          for name in ('P1_mod9','P2_mod9','P3_mod9','P4_mod9')}})
    assert sum(int(r['smooth_genus2']) for r in linked)==194
    args.output_dir.mkdir(parents=True,exist_ok=True)
    emit(args.output_dir/'finite_frobenius_mod9_162.csv',list(table.values()))
    emit(args.output_dir/'host8_finite_frobenius_mod9_288.csv',linked)
    print('PASS: constructed 162 finite two-term 4x4 matrices with 3-integral lattice coordinates modulo 9')
    print('PASS: 194 Host8-manifest smooth selections linked; physical drive not accessed')
    print('NOTE: no tail bound proved; do not label as a full cohomological Frobenius computation')

if __name__=='__main__':main()
