#!/usr/bin/env python3
"""Finite exact rational reductions for a p=3 genus-two Frobenius truncation.

No analytic limits or point-count values are supplied to the calculation.
This is a *bounded approximation* of the characteristic-three lift, not
by itself a proof that the truncated matrix is a cohomological Frobenius.
"""
from fractions import Fraction as Q
from math import inf

P=3
ZERO=(Q(0),)
ONE=(Q(1),)

def poly(a):
    a=list(map(Q,a))
    if not a:return ZERO
    while len(a)>1 and a[-1]==0:a.pop()
    return tuple(a)

def add(a,b):
    return poly([(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))])

def neg(a):return tuple(-v for v in a)

def sub(a,b):return add(a,neg(b))

def scale(a,q):return poly((q*v for v in a))

def mul(a,b):
    o=[Q(0)]*(len(a)+len(b)-1)
    for i,u in enumerate(a):
        if u:
            for j,v in enumerate(b):
                o[i+j]+=u*v
    return poly(o)

def powpoly(a,k):
    o=ONE
    while k:
        if k&1:o=mul(o,a)
        a=mul(a,a);k//=2
    return o

def diff(a):return poly([i*a[i] for i in range(1,len(a))])

def divmodpoly(a,b):
    a=list(a);n=len(b)-1
    if b==ZERO:raise ZeroDivisionError()
    quotient=[Q(0)]*max(1,len(a)-n)
    while len(a)>n and (len(a)>1 or a[0]!=0):
        k=len(a)-n-1
        coefficient=a[-1]/b[-1]
        quotient[k]+=coefficient
        for j,v in enumerate(b):a[k+j]-=coefficient*v
        while len(a)>1 and a[-1]==0:a.pop()
    return poly(quotient),poly(a)

def extgcd(a,b):
    s0,s1=ONE,ZERO
    t0,t1=ZERO,ONE
    while b!=ZERO:
        q,r=divmodpoly(a,b)
        a,b=b,r
        s0,s1=s1,sub(s0,mul(q,s1))
        t0,t1=t1,sub(t0,mul(q,t1))
    return a,s0,t0

def inverse_mod(a,f):
    gcd,s,_=extgcd(a,f)
    if len(gcd)!=1 or not gcd[0]:raise ValueError('singular curve or invalid inverse')
    return divmodpoly(scale(s,Q(1)/gcd[0]),f)[1]

def reduce_poles(P,highest_m,f,fp,inv):
    # Exact identity: d(S/y^(2m-1)) is cohomologous to zero.
    # P dx/y^(2m+1) reduces to ((P + (2m-1) S f'/2)/f - S') dx/y^(2m-1).
    for m in range(highest_m,0,-1):
        S=scale(divmodpoly(mul(P,inv),f)[1],Q(-2,2*m-1))
        num=add(P,scale(mul(S,fp),Q(2*m-1,2)))
        q,r=divmodpoly(num,f)
        if r!=ZERO:raise ArithmeticError('nonexact pole reduction')
        P=sub(q,diff(S))
    return P

def reduce_degree(P,f,fp):
    # Exact differential d(2*x^k*y) = (2*k*x^(k-1)*f+x^k*f') dx/y.
    while len(P)>4:
        k=len(P)-5
        c=P[-1]/Q(2*k+5)
        monomial=poly([0]*k+[c])
        P=sub(P,add(scale(mul(diff(monomial),f),2),mul(monomial,fp)))
    return tuple(P[i] if i<len(P) else Q(0) for i in range(4))

def frobenius_term(f,fp,inv,delta,degree,k,binom):
    coeff=3*binom
    numerator=scale(mul(poly([0]*(3*degree+2)+[1]),powpoly(delta,k)),coeff)
    return reduce_degree(reduce_poles(numerator,1+3*k,f,fp,inv),f,fp)

def matrix_add_term(m,f,fp,inv,delta,k,binom):
    for i in range(4):
        v=frobenius_term(f,fp,inv,delta,i,k,binom)
        for j in range(4):m[j][i]+=v[j]

def characteristic(m):
    n=4
    B=[[Q(int(i==j)) for j in range(n)] for i in range(n)]
    coeff=[Q(1)]
    for k in range(1,n+1):
        A=[[sum(m[i][v]*B[v][j] for v in range(n)) for j in range(n)] for i in range(n)]
        c=-sum(A[i][i] for i in range(n))/k
        coeff.append(c)
        B=[[A[i][j]+(c if i==j else 0) for j in range(n)] for i in range(n)]
    return coeff

def v3(q):
    if not q:return inf
    u,v=abs(q.numerator),q.denominator
    count=0
    while u%3==0:count+=1;u//=3
    while v%3==0:count-=1;v//=3
    return count

def mod9(q):
    """Project a 3-integral rational number into Z/9Z; reject otherwise."""
    if v3(q)<0:raise ValueError('not 3-integral')
    num,den=q.numerator,q.denominator
    while den%3==0:
        den//=3
        num//=3
    return num*pow(den,-1,9)%9

def compute(coeff,terms=4):
    if len(coeff)!=5 or any(c not in (0,1,2) for c in coeff):raise ValueError('quintic trits required')
    f=poly(list(coeff)+[1]);fp=diff(f)
    inv=inverse_mod(fp,f)
    delta=sub(poly([f[i//3] if i%3==0 and i//3<len(f) else 0 for i in range(16)]),powpoly(f,3))
    assert all(c.denominator==1 and c.numerator%3==0 for c in delta)
    m=[[Q(0) for _ in range(4)] for _ in range(4)]
    binom=Q(1)
    for k in range(terms):
        matrix_add_term(m,f,fp,inv,delta,k,binom)
        binom*=Q(-2*k-1,2*(k+1))
    cp=characteristic(m)
    return m,cp

if __name__=='__main__':
    from time import perf_counter
    t=perf_counter()
    m,cp=compute((1,0,1,0,0),4)
    print('3-adic valuations',[[v3(v) for v in row] for row in m])
    print('charpoly mod 9',[mod9(v) for v in cp])
    print('elapsed seconds',perf_counter()-t)
