#!/usr/bin/env python3
"""Independent arithmetic audit of the public Asolaria 27x27 finite-field operator.

Source definition: JesseBrown1980/Solved-The-Riemann-Hypothesis-The-Hilbert-P-lya-Spectral-Operator-Solved,
main commit 99043074e28825eb73e655a53750129e5f71341d, src/lib.rs.
This verifies finite-field algebra, NOT the classical Riemann hypothesis.
"""
import json, math
P = 1_000_081
G = 7
W = 951_846
K = 27
PRIMES = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103]
HALF = (P + 1) // 2

def is_prime(n):
    if n < 2: return False
    if n % 2 == 0: return n == 2
    return all(n % d for d in range(3, math.isqrt(n) + 1, 2))

def order(a):
    if not is_prime(P): raise AssertionError('P is not prime')
    r, k = a % P, 1
    while r != 1:
        r = r * a % P
        k += 1
        assert k <= P - 1
    return k

assert is_prime(P)
assert order(G) == P - 1
assert order(W) == 27
assert (2*HALF)%P == 1

c = [0]*K
for d in range(1,14):
    z = ((pow(W,d,P) - pow(W,K-d,P)) * PRIMES[d])%P
    c[d] = z
    c[K-d] = (-z)%P
T = [[c[(j - i)%K] for j in range(K)] for i in range(K)]
H = [[((HALF if i == j else 0) + T[i][j]) % P for j in range(K)] for i in range(K)]
assert all(T[i][i] == 0 and sum(T[i])%P == 0 for i in range(K))
assert all((T[i][j]+T[j][i])%P == 0 for i in range(K) for j in range(K))
assert all((H[i][j]+H[j][i])%P == (1 if i==j else 0) for i in range(K) for j in range(K))

# Fully diagonalize the circulant matrix using its 27 distinct Fourier vectors
# over F_P: z_j[i] = W^(j*i). This requires no floating point arithmetic.
eigen_T = [sum(c[d]*pow(W,(k*d)%K,P) for d in range(K))%P for k in range(K)]
eigen_H = [(HALF + q)%P for q in eigen_T]
for k in range(K):
    vec=[pow(W,(k*i)%K,P) for i in range(K)]
    result=[sum(T[i][j]*vec[j] for j in range(K))%P for i in range(K)]
    assert result == [eigen_T[k]*v%P for v in vec]
assert eigen_H[0] == HALF
assert all((eigen_H[k] + eigen_H[(-k)%K])%P == 1 for k in range(K))
assert sum(eigen_T)%P == 0
assert sum(pow(a,3,P) for a in eigen_T)%P == 0
assert sum(pow(a,2,P) for a in eigen_T)%P != 0

# exact NTT test of the Law 0 statement on 27 deterministic vectors
for seed in range(27):
    vec=[(seed + 11*i*i + 7*i + 3)%P for i in range(K)]
    evolved=[sum(T[i][j]*vec[j] for j in range(K))%P for i in range(K)]
    dc=sum(evolved)%P
    assert dc == 0

res={
 'p':P,'p_is_prime':True,'generator_7_multiplicative_order':order(G),
 'w_951846_order':order(W),'half_mod_p':HALF,
 'modular_skew_symmetry':True,'H_plus_transpose_equals_I_mod_p':True,
 'zero_row_and_column_sums':True,'center_prism_Tv_mod_p':0,
 'all_27_Fp_eigenvalues':eigen_H,
 'distinct_eigenvalues_count':len(set(eigen_H)),
 'eigenvalues_equal_modular_half':sum(x==HALF for x in eigen_H),
 'lambda_1':eigen_H[1],'lambda_26':eigen_H[26],
 'lambda_1_plus_lambda_26_mod_P':(eigen_H[1]+eigen_H[26])%P,
 'finite_field_has_canonical_complex_real_part':False,
 'conclusion':'Modular spectral pairing is exact; no classical-zeta spectral identification proven.'
}
print(json.dumps(res,indent=2))
import os
out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'spectral_results.json')
with open(out_path, 'w') as f:
    json.dump(res, f, indent=2)
