#!/usr/bin/env python3
"""Host8-derived genus-two zeta computation in characteristic three.
Finite-field analogue of RH only, not a proof of the classical conjecture.
Requires only the Python standard library.
"""
from __future__ import annotations
import argparse
import csv
from decimal import Decimal, getcontext
import hashlib
from pathlib import Path
import struct

getcontext().prec = 70
EXPECTED = {
 '000': ('2dfe7d757ecb012475806b86fcdefc602680d042db836ffbcb2bfe924f2a18ee', '9da76c8b3151fa372ff2ef378cb5018490f7460581035e3268b3afd4a85e6e0f'),
 '187': ('6752ab9e2603cc5042f7c7a41c3ddc48ae5571fd0aeb945d0a3f63b1a948a652', 'b3bfb382de3eb473cd43328abb50e31c4e5222d734e8d39d8e80b47e6f19ad07'),
 '374': ('963805be806e8a290aab8dee48b0d214d03015c84e02bf844f0de87e2b37c10a', '11969dcf23ae7cb32103d40e8c12b4f7a87eec2b614c02ea2e9675bc80e2bae4'),
}
MODULI = ((0,1),(1,0,1),(1,2,0,1),(2,1,0,0,1))
SAMPLES = 96
ROOMS = 48**3

def trits(n, degree):
    return tuple((n//3**i)%3 for i in range(degree))

def strip(p):
    p=list(p)
    while p and p[-1]==0: p.pop()
    return p

def remainder(f,g):
    f,g=strip(f),strip(g)
    assert g
    inv=pow(g[-1],-1,3)
    while len(f)>=len(g):
        n=len(f)-len(g)
        a=f[-1]*inv%3
        for j,b in enumerate(g):f[j+n]=(f[j+n]-a*b)%3
        f=strip(f)
    return f

def nonsingular(coeff):
    f=[*coeff,1]
    derivative=[i*f[i]%3 for i in range(1,6)]
    a,b=f,strip(derivative)
    while b:a,b=b,remainder(a,b)
    return len(a)==1

class Field:
    def __init__(self,degree,modulus):
        self.n=degree
        self.q=3**degree
        d=[trits(i,degree) for i in range(self.q)]
        self.add=[[sum(((d[i][k]+d[j][k])%3)*3**k for k in range(degree)) for j in range(self.q)] for i in range(self.q)]
        self.mul=[]
        for i in range(self.q):
            row=[]
            for j in range(self.q):
                p=[0]*(2*degree-1)
                for a in range(degree):
                    for b in range(degree):p[a+b]=(p[a+b]+d[i][a]*d[j][b])%3
                for k in range(len(p)-1,degree-1,-1):
                    lead=p[k]
                    for m in range(degree):p[k-degree+m]=(p[k-degree+m]-lead*modulus[m])%3
                row.append(sum(p[k]*3**k for k in range(degree)))
            self.mul.append(row)
        for i in range(1,self.q):
            assert any(self.mul[i][j]==1 for j in range(1,self.q))
        squares={self.mul[i][i] for i in range(1,self.q)}
        self.character=[0 if i==0 else (1 if i in squares else -1) for i in range(self.q)]
        self.powers=[[self.power(x,k) for k in range(6)] for x in range(self.q)]
    def power(self,x,n):
        out=1
        for _ in range(n):out=self.mul[out][x]
        return out
    def points(self,coeff):
        # One point at infinity for a smooth odd-degree hyperelliptic curve.
        count=self.q+1
        for powers in self.powers:
            v=powers[5]
            for k,c in enumerate(coeff):
                if c:
                    w=powers[k] if c==1 else self.add[powers[k]][powers[k]]
                    v=self.add[v][w]
            count+=self.character[v]
        return count

def zeta(code,fields):
    coeff=trits(code,5)
    if not nonsingular(coeff):return None
    counts=[f.points(coeff) for f in fields]
    s=[3**n+1-counts[n-1] for n in range(1,5)]
    A=-s[0]
    assert (s[0]*s[0]-s[1])%2==0
    B=(s[0]*s[0]-s[1])//2
    # Independently counted F27 and F81 must obey Newton identities.
    assert s[2]==-A**3+3*A*B-9*A
    assert s[3]==A**4-4*A*A*B+2*B*B+12*A*A-36
    D=A*A-4*B+24
    u=24+4*B
    # Equivalent to both roots of z^2+(A/sqrt(3))*z+B/3-2
    # being real in [-2,2]. Exact integer predicate (no tolerance).
    good=(D>=0 and A*A<=48 and u>=0 and u*u>=192*A*A)
    if D>=0:
        sq3=Decimal(3).sqrt()
        roots=[(-Decimal(A)+sign*Decimal(D).sqrt())/(2*sq3) for sign in (-1,1)]
        assert good==all(abs(x)<=Decimal(2)+Decimal('1e-55') for x in roots)
    return (counts,A,B,good)

def read_manifest(path):
    with path.open(newline='') as f:
        records=[(r['sector'],int(r['sample']),int(r['cell_index']),int(r['code243'])) for r in csv.DictReader(f)]
    assert len(records)==3*SAMPLES
    for sector in EXPECTED:
        subs=[r for r in records if r[0]==sector]
        assert len(subs)==SAMPLES
        for j,(_,sample,cell,code) in enumerate(subs):
            assert sample==j and cell==j*(ROOMS-1)//(SAMPLES-1) and 0<=code<243
    return records

def read_host8(directory):
    result=[]
    for sector,hashes in EXPECTED.items():
        raw=(directory/('sector-'+sector+'.rooms')).read_bytes()
        assert len(raw)>=884736, ('short sector',sector,len(raw))
        assert hashlib.sha256(raw[:110592]).hexdigest()==hashes[0], ('bad L24 hash',sector)
        assert hashlib.sha256(raw[:884736]).hexdigest()==hashes[1], ('bad L48 hash',sector)
        for j in range(SAMPLES):
            cell=j*(ROOMS-1)//(SAMPLES-1)
            v=struct.unpack_from('<Q',raw,cell*8)[0]
            result.append((sector,j,cell,v%243))
    print('PASS: all six Host8 slice hashes verified')
    return result

def write_results(rows,fields,out):
    out.mkdir(parents=True,exist_ok=True)
    calculated={c:zeta(c,fields) for c in range(243)}
    smooth=sum(v is not None for v in calculated.values())
    passes=sum(v[3] for v in calculated.values() if v is not None)
    assert smooth==passes==162,(smooth,passes)
    with (out/'all_quintics.csv').open('w',newline='') as f:
        w=csv.writer(f)
        w.writerow(['code243','a0','a1','a2','a3','a4','smooth_genus2','N_F3','N_F9','N_F27','N_F81','P1','P2','RH_pass'])
        for code,v in calculated.items():
            w.writerow([code,*trits(code,5),int(v is not None),*(v[0] if v else ['']*4),*(v[1:3] if v else ['','']),int(v[3]) if v else 0])
    with (out/'host8_curve_results.csv').open('w',newline='') as f:
        w=csv.writer(f)
        w.writerow(['sector','sample','cell_index','code243','a0','a1','a2','a3','a4','smooth_genus2','N_F3','N_F9','N_F27','N_F81','P1','P2','RH_pass'])
        for sector,j,cell,code in rows:
            v=calculated[code]
            w.writerow([sector,j,cell,code,*trits(code,5),int(v is not None),*(v[0] if v else ['']*4),*(v[1:3] if v else ['','']),int(v[3]) if v else 0])
    for sec in EXPECTED:
        items=[calculated[code] for sector,_,_,code in rows if sector==sec]
        valid=[v for v in items if v is not None]
        print('sector',sec,'samples',len(items),'smooth',len(valid),'RH_pass',sum(v[3] for v in valid))
    print('ALL 243 QUINTICS:',smooth,'smooth genus-two curves;',passes,'pass exact finite-field RH zero condition')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host8-dir',type=Path,help='Read first 884736 bytes of sectors 000/187/374 and verify all six SHA256 hashes')
    parser.add_argument('--manifest',type=Path,default=Path(__file__).parent/'data'/'host8_seed_manifest.csv')
    parser.add_argument('--output-dir',type=Path,default=Path(__file__).parent/'results')
    args=parser.parse_args()
    records=read_host8(args.host8_dir) if args.host8_dir else read_manifest(args.manifest)
    if args.host8_dir and args.manifest.is_file():
        assert records==read_manifest(args.manifest),'Sector bytes do not match published trit seed manifest'
    if not args.host8_dir:print('Manifest-only mode: no physical Host8 bytes authenticated this run')
    fields=[Field(n,p) for n,p in enumerate(MODULI,start=1)]
    write_results(records,fields,args.output_dir)

if __name__=='__main__':
    main()
