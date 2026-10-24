#!/usr/bin/env python3
"""Phase 5B: *formal algebraic* Frobenius lift mod 9 for y^2=f(x), p=3.

Works in the localized algebra
    (Z/9Z)[x,y,y^(-1)]/(y^2-f(x)).
This verifies the defining curve relation and Frobenius reduction mod 3.
It does NOT yet compute Monsky-Washnitzer H^1 Frobenius or its 4x4 matrix.

For integral f, Delta=f(x^3)-f(x)^3 is coefficientwise divisible by 3.
Phi(x)=x^3,
Phi(y)=y^3+(1/2)*Delta*y^(-3)       (mod 9)
satisfies Phi(y)^2=f(x^3), exactly in this localized ring mod 9.
"""
from __future__ import annotations
import argparse
import csv
from pathlib import Path

ROOT=Path(__file__).resolve().parent
MODULUS=9
INV2=5

def multiply(a,b):
    out=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            out[i+j]+=x*y
    return out

def delta_polynomial(coeff):
    """Return Delta=f(x^3)-f(x)^3 as an integer polynomial."""
    assert len(coeff)==5 and all(0<=x<=2 for x in coeff)
    f=[*coeff,1]
    cubic=multiply(multiply(f,f),f)
    fx3=[0]*16
    for i,c in enumerate(f):
        fx3[3*i]=c
    delta=[a-b for a,b in zip(fx3,cubic)]
    assert all(c%3==0 for c in delta)
    return delta

def check_frobenius(coeff):
    delta=delta_polynomial(coeff)
    # Phi(y)=y^3 + correction / y^3; let correction=Delta/2.
    # Its square differs from y^6+2*correction by correction^2/y^6.
    correction=[INV2*d%MODULUS for d in delta]
    cross=[(2*x)%MODULUS for x in correction]
    assert cross==[x%MODULUS for x in delta]
    correction_squared=multiply(correction,correction)
    assert all(c%MODULUS==0 for c in correction_squared)
    # Therefore Phi(y)^2=y^6+Delta=f(x^3) (mod 9).
    # Phi(y) mod 3 = y^3, and Phi(x)=x^3.
    assert all(c%3==0 for c in correction)
    assert all(c%3==0 for c in delta)
    nontrivial=int(any(c%MODULUS for c in delta))
    # Pullback of omega_i=x^i dx/(2y) BEFORE cohomological reduction:
    # Phi*(omega_i) = 3*x^(3i+2) dx/(2*y^3) mod 9.
    # The correction terms are O(9) on the chain level only;
    # reducing higher-pole differentials may divide by 3 and
    # lose precision. Hence this is NOT a 4x4 H^1 matrix.
    return {'formal_lift_relation_pass':1, 'frobenius_mod3_pass':1,
            'nontrivial_delta_mod9':nontrivial,
            'delta_over3_nonzero_coeffs':sum((c//3)%3!=0 for c in delta),
            'delta_mod9_coefficients':';'.join(str(c%9) for c in delta)}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--all-quintics',type=Path,default=ROOT/'results'/'all_quintics.csv')
    p.add_argument('--host8-manifest',type=Path,default=ROOT/'data'/'host8_seed_manifest.csv')
    p.add_argument('--output-dir',type=Path,default=ROOT/'results')
    a=p.parse_args()
    with a.all_quintics.open(newline='') as f:curve_rows=list(csv.DictReader(f))
    assert len(curve_rows)==243
    out=[]
    table={}
    for row in curve_rows:
        code=int(row['code243'])
        if row['smooth_genus2']!='1':continue
        coeff=[int(row['a'+str(i)]) for i in range(5)]
        v={'code243':code,**check_frobenius(coeff)}
        out.append(v)
        table[code]=v
    assert len(out)==162
    with a.host8_manifest.open(newline='') as f:records=list(csv.DictReader(f))
    assert len(records)==288
    host=[]
    for row in records:
        code=int(row['code243'])
        item=dict(sector=row['sector'],sample=row['sample'],
                  cell_index=row['cell_index'],code243=code,
                  smooth_genus2=int(code in table))
        if code in table:
            item.update({k:v for k,v in table[code].items() if k!='code243'})
        else:
            item.update({k:'' for k in out[0] if k!='code243'})
        host.append(item)
    assert sum(row['smooth_genus2'] for row in host)==194
    a.output_dir.mkdir(parents=True,exist_ok=True)
    for name,rows in [('formal_frobenius_mod9_curve_checks.csv',out),
                      ('host8_formal_frobenius_mod9_checks.csv',host)]:
        with (a.output_dir/name).open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
    print('PASS: 162 / 162 exact formal Z/9 Frobenius lift relations')
    print('PASS: 194 / 194 Host8 smooth curve selections')
    print('NOTE: cohomological 4x4 Frobenius matrix NOT calculated')

if __name__=='__main__':
    main()
