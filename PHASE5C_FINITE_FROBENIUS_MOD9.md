# Phase 5C — bounded four-dimensional Frobenius approximation modulo 9

## Computational status (2026-10-24)

**An explicit finite two-term differential-reduction algorithm constructs a 4x4 matrix for each of the 162 smooth monic genus-two quintics over F3.** Its characteristic polynomial modulo 9 agrees with the independently counted zeta numerator for **162/162** curves. These matrices are **bounded Frobenius approximations**, not yet certified full Monsky–Washnitzer/crystalline Frobenius matrices. In particular, stabilization at finitely many correction orders is not a proof about the uncomputed tail.

This experiment uses exact integer/rational arithmetic, finite polynomials and a final projection into Z/9Z; it does not calculate or use infinite completions. The independent existing point-count table is read **only in tests**, never by the matrix construction.

## Finite algebraic construction

Write C: y^2=f(x), with f monic of degree 5 and coefficients in {0,1,2}. Let

    Delta(x) = f(x^3) - f(x)^3,   Delta in 3 Z[x].

For the odd differential basis omega_i=x^i dx/(2y), i=0,1,2,3, consider the finite first K terms of the pullback expansion:

    R_K(omega_i) =
      sum_{k=0}^{K-1} 3 * binomial(-1/2,k) *
      x^(3i+2) Delta(x)^k dx/(2 y^(6k+3)).

The candidate uses **K=2**, meaning k=0 and k=1. The k=1 term is essential: even though its unreduced coefficients are multiples of 9, exact reduction may divide by 3.

For each high-pole term, use the finite exact derivative relation

    d(S/y^(2m-1)) =
      [S' f - (2m-1) S f'/2] dx/y^(2m+1).

Since gcd(f,f')=1 modulo 3 for smooth curves, an inverse of f' modulo f is available. Choose S=-2*(P/f' mod f)/(2m-1), with polynomial modular multiplication, and reduce the pole exponent by two. Then use

    d(2*x^k*y) =
       [2*k*x^(k-1)*f + x^k*f'] dx/y

to reduce polynomial degree to at most 3. Divisions are done exactly in Q before any mod-9 reduction, retaining the required guard precision.

The resulting raw matrix need not be 3-integral in the naive basis. For all 162 curves the finite change of basis

    (omega_0, omega_1, omega_2, 3*omega_3)

gives 3-integral entries. If D=diag(1,1,1,3), the projected candidate is

    F_K = D^(-1) M_K D (mod 9).

The output characteristic polynomial is

    det(I - T*F_K) mod 9 = 1 + c1*T + c2*T^2 + c3*T^3 + c4*T^4.

The use of rational intermediate calculations and the change of lattice must not be confused with an independently established integral model of full crystalline cohomology.

## Exhaustive controls

| Finite check | Observed result |
|---|---:|
| Smooth curves in the 3^5=243 coefficient family | 162 |
| K=2 characteristic polynomials matching point-count results modulo 9 | 162/162 |
| K=1 characteristic polynomials **not** matching point-count results | 145/162 |
| K=3 versus K=2: candidate matrices identical modulo 9 in the scaled lattice | 162/162 |
| K=4 versus K=3: candidate matrices identical modulo 9 in the scaled lattice | 162/162 in a separate local exhaustive check; CI samples this order |
| Previously published Host8 manifest entries | 288 |
| Smooth Host8 manifest entries linked to finite matrix results | 194 |

For example, f=x^5+x^2+1 (code243=10) produces the mod-9 polynomial

    det(I-T*F_2) = 1 + 2*T + 6*T^2 + 6*T^3 (mod 9).

This matches A=2 and B=6 from the independent point-count table, but neither A nor B was an input to the construction.

## Scope and unfinished proof

1. The algorithm is **finite**: finitely many exact rational polynomial reductions followed by reduction modulo 9. It avoids an infinite weak completion in the executable computation.
2. A finite-order agreement is **not yet** a proof that every omitted term k>=2 reduces to zero modulo 9. The essential missing lemma is a **uniform precision / valuation bound** for the omitted terms in the chosen scaled differential basis, including all denominators encountered by pole and degree reduction.
3. Establishing such a lemma, or constructing a direct fully finite mod-9 cochain model with proved comparison to the zeta polynomial, would upgrade the operator-to-zeta relationship beyond the present exhaustive check.
4. Nothing here implies the classical Riemann hypothesis. The 162/162 match is a complete verification for this specified finite coefficient family, not a universal theorem for arbitrary fields or curves.
5. No physical 300GB Host8 volume was accessed in this phase. Host8 entries come from the pinned manifest and repeat curves; they are not 194 independent cohomological examples.

## Reproduction

    python -m unittest -v test_finite_frobenius_mod9.py
    python verify_finite_frobenius_mod9.py --output-dir results

Output files:

- results/finite_frobenius_mod9_162.csv — 4x4 candidate matrices and mod-9 characteristic polynomials, computed without point counts
- results/host8_finite_frobenius_mod9_288.csv — pinned manifest linkage, no physical-drive access

Both files are deterministically generated; CI reconstructs them in a temporary output directory. All calculations use the Python standard library and exact integer/rational arithmetic.

**Current status:** finite 4x4 candidate PASS at K=2 for the 162-curve family, with finite truncation controls; rigorous omitted-tail precision theorem PENDING.
