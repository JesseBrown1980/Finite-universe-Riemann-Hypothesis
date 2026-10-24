#!/usr/bin/env python3
"""Phase 3: genus-two Frobenius companion and F_(3^5), F_(3^6) holdouts.

An integer companion matrix from N1,N2 packages the known curve zeta polynomial.
It is NOT an independently constructed geometric Frobenius endomorphism and
does not prove the classical Riemann hypothesis.
"""
from __future__ import annotations
import argparse
import csv
from pathlib import Path
from itertools import permutations

MOD5 = (1, 2, 0, 0, 0, 1)  # x^5+2x+1, irreducible over F3
MOD6 = (2, 1, 0, 0, 0, 0, 1)  # x^6+x+2, irreducible over F3


def digits(v: int, n: int) -> tuple[int,...]:
    return tuple((v//3**i)%3 for i in range(n))


class Field:
    """Exact ternary polynomial quotient, checked to be a field."""
    def __init__(self, modulus):
        self.n=len(modulus)-1
        self.q=3**self.n
        d=[digits(i,self.n) for i in range(self.q)]
        self.mul=[]
        self.add=[]
        for a in range(self.q):
            addrow=[]
            mulrow=[]
            for b in range(self.q):
                addrow.append(sum(((d[a][k]+d[b][k])%3)*3**k for k in range(self.n)))
                product=[0]*(2*self.n-1)
                for k in range(self.n):
                    for j in range(self.n):
                        product[k+j]=(product[k+j]+d[a][k]*d[b][j])%3
                for k in range(2*self.n-2,self.n-1,-1):
                    v=product[k]
                    for j in range(self.n):
                        product[k-self.n+j]=(product[k-self.n+j]-v*modulus[j])%3
                mulrow.append(sum(product[k]*3**k for k in range(self.n)))
            self.add.append(addrow)
            self.mul.append(mulrow)
        assert all(1 in self.mul[a] for a in range(1,self.q)), 'reducible modulus'
        squares={self.mul[a][a] for a in range(1,self.q)}
        assert len(squares)==(self.q-1)//2
        self.chi=[0 if a==0 else (1 if a in squares else -1) for a in range(self.q)]
        self.twice=[self.add[a][a] for a in range(self.q)]
        self.powers=[]
        for x in range(self.q):
            p=[1]
            for _ in range(5):
                p.append(self.mul[p[-1]][x])
            self.powers.append(p)

    def count_points(self, coeff):
        count=self.q+1  # exactly one infinity point on smooth odd-degree quintic
        for powers in self.powers:
            v=powers[5]
            for k,c in enumerate(coeff):
                if c:
                    v=self.add[v][powers[k] if c==1 else self.twice[powers[k]]]
            count+=self.chi[v]
        return count


def matrix(A,B):
    """Companion of x^4 + A*x^3 + B*x^2 + 3*A*x + 9."""
    return ((0,0,0,-9), (1,0,0,-3*A), (0,1,0,-B), (0,0,1,-A))


def multiply(a,b):
    return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(4))
                       for j in range(4)) for i in range(4))


def det_polynomial_I_minus_tM(m):
    """Determinant polynomial via all 24 signed permutations, exact integers."""
    out=[0]*5
    for perm in permutations(range(4)):
        parity=(-1)**sum(perm[i]>perm[j] for i in range(4) for j in range(i+1,4))
        term=[parity]
        for i,j in enumerate(perm):
            fac=[int(i==j),-m[i][j]]
            z=[0]*(len(term)+1)
            for k,u in enumerate(term):
                z[k]+=u*fac[0]
                z[k+1]+=u*fac[1]
            term=z
        for k,v in enumerate(term):
            out[k]+=v
    return out


def power_traces(m, n=6):
    product=tuple(tuple(int(i==j) for j in range(4)) for i in range(4))
    result=[]
    for _ in range(n):
        product=multiply(product,m)
        result.append(sum(product[i][i] for i in range(4)))
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=Path,default=Path(__file__).resolve().parent/'results'/'all_quintics.csv')
    p.add_argument('--output',type=Path,default=Path(__file__).resolve().parent/'results'/'frobenius_companion_predictions.csv')
    p.add_argument('--host8-dir',type=Path,default=None,help='Authenticate Host8 slices and test predictions on all 288 room samples')
    p.add_argument('--manifest',type=Path,default=Path(__file__).resolve().parent/'data'/'host8_seed_manifest.csv')
    p.add_argument('--host8-output',type=Path,default=Path(__file__).resolve().parent/'results'/'host8_frobenius_companion_results.csv')
    args=p.parse_args()
    f5,f6=Field(MOD5),Field(MOD6)
    with args.source.open(newline='') as f:
        records=list(csv.DictReader(f))
    assert len(records)==243
    rows=[]
    for r in records:
        if r['smooth_genus2']!='1':continue
        code=int(r['code243'])
        coeff=digits(code,5)
        assert coeff==tuple(int(r['a'+str(i)]) for i in range(5))
        A,B=int(r['P1']),int(r['P2'])
        n1,n2,n3,n4=(int(r['N_F'+str(q)]) for q in (3,9,27,81))
        assert A==n1-4 and 2*B==n2-10+A*A
        m=matrix(A,B)
        assert det_polynomial_I_minus_tM(m)==[1,A,B,3*A,9]
        traces=power_traces(m)
        predicted=[3**n+1-traces[n-1] for n in range(1,7)]
        assert predicted[:4]==[n1,n2,n3,n4], ('published counts',code)
        actual5,actual6=f5.count_points(coeff),f6.count_points(coeff)
        assert predicted[4:]==[actual5,actual6], ('held-out counts',code,predicted[4:],(actual5,actual6))
        for n,trace in enumerate(traces,start=1):
            assert trace**2<=16*3**n, ('Weil trace bound',code,n)
        rows.append({'code243':code,'P1':A,'P2':B,'matrix_det':9,'frobenius_trace_1':traces[0],
                     'predicted_N_F243':predicted[4],'counted_N_F243':actual5,
                     'predicted_N_F729':predicted[5],'counted_N_F729':actual6,
                     'heldout_agrees':1})
    assert len(rows)==162
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print('PASS: 162 smooth curves; 162 exact 4x4 companion polynomial determinants')
    print('PASS: F3/F9/F27/F81 point counts and Frobenius power traces')
    print('PASS: 324 HELD-OUT predictions vs direct F243/F729 point counts')
    if args.host8_dir:
        from host8_ternary_weil import read_host8, read_manifest
        manifest_records = read_manifest(args.manifest)
        host8_records = read_host8(args.host8_dir)
        assert host8_records == manifest_records
        pred_map = {r['code243']: r for r in rows}
        host8_rows = []
        smooth_host8 = 0
        for sec, j, cell, code in host8_records:
            if code in pred_map:
                smooth_host8 += 1
                pr = pred_map[code]
                host8_rows.append({
                    'sector': sec, 'sample': j, 'cell_index': cell, 'code243': code,
                    'is_smooth': 1,
                    'P1': pr['P1'], 'P2': pr['P2'],
                    'matrix_det': pr['matrix_det'],
                    'frobenius_trace_1': pr['frobenius_trace_1'],
                    'predicted_N_F243': pr['predicted_N_F243'],
                    'counted_N_F243': pr['counted_N_F243'],
                    'predicted_N_F729': pr['predicted_N_F729'],
                    'counted_N_F729': pr['counted_N_F729'],
                    'heldout_agrees': 1
                })
            else:
                host8_rows.append({
                    'sector': sec, 'sample': j, 'cell_index': cell, 'code243': code,
                    'is_smooth': 0,
                    'P1': '', 'P2': '',
                    'matrix_det': '',
                    'frobenius_trace_1': '',
                    'predicted_N_F243': '',
                    'counted_N_F243': '',
                    'predicted_N_F729': '',
                    'counted_N_F729': '',
                    'heldout_agrees': 0
                })
        assert smooth_host8 == 194
        args.host8_output.parent.mkdir(parents=True, exist_ok=True)
        with args.host8_output.open('w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=list(host8_rows[0].keys()))
            writer.writeheader()
            writer.writerows(host8_rows)
        print('PASS: 194 Host8 smooth curves; 388 HELD-OUT predictions vs direct F243/F729 point counts; 0 disagreements')
    print('NOT CLAIMED: geometric Frobenius construction or classical RH proof')


if __name__=='__main__':
    main()
