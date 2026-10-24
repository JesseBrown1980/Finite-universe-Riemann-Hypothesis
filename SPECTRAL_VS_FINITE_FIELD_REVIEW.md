# Asolaria ternary spectral vs finite-field Riemann-hypothesis analogue

**Audit date:** 2026-10-24. **Status:** Independent exact modular computation and 288-room cross-check completed. This is not a proof of the classical Riemann hypothesis.

## Sources inspected

- `JesseBrown1980/Solved-The-Riemann-Hypothesis-The-Hilbert-P-lya-Spectral-Operator-Solved`, main `99043074e28825eb73e655a53750129e5f71341d`, `src/lib.rs`, `tests/riemann_tests.rs`.
- `JesseBrown1980/Finite-universe-Riemann-Hypothesis`, main `f9efcb0d2dd1692a93ae976c6b9c39c6aaf3ceb5`, with exact F3 genus-2 data and successful Actions run `40098238729`.
- Host8 published binary slices from `JesseBrown1980/finite-reversible-ternary-physics`, pinned commit `5a7e9a23dcacdea6fac3c5fa9d5db3069e82e9e3`.

## What was independently checked

Reconstructed the exact 27×27 circulant generator `T` from the 27 primes and W, performed Fourier diagonalization entirely modulo 1,000,081, checked every eigenpair by direct matrix-vector multiplication, verified zero row and column sums and `H+H^T=I (mod P)`, verified odd trace moments and the DC-zero property on 27 independent test vectors.

- P = 1,000,081 is prime.
- G = 7 has multiplicative order 1,000,080.
- W = 951,846 has exact multiplicative order 27.
- h = inverse(2) mod P = 500,041.
- All 27 Fourier eigenvalues lie in F_P and form modular pairs `lambda_j + lambda_(27-j) = 1 (mod P)`.
- `lambda_0 = 500041`, `lambda_1 = 215593`, `lambda_26 = 784489`.
- Exactly **one** of the 27 field eigenvalues equals 500041; this does not contradict the modular pairing.
- The exact 27 eigenvalues are included in `spectral_results.json`.

### IMPORTANT: the complex critical line has not been derived

`H+H^T=I (mod P)` is valid; however, F_P has no standard ordered real part, complex conjugation or Hermitian inner product. The derivation invoking `v^dagger` and `Re(lambda)` therefore cannot be made from the displayed modular identity alone. As a direct counter to a literal "each eigenvalue is modular one-half" interpretation, the eigenvalues of H are explicitly 215593 and 784489, neither equal to 500041; only **their modular sum** is 1.

Nor do `Tr(T)=Tr(T^3)=0` or a 27-point invertible NTT identify the eigenvalues of T with the imaginary parts of nontrivial zeros of the classical zeta function. These identities follow from circulant skew-symmetry for many matrices unrelated to zeta. The operator would need a justified spectral correspondence with classical `zeta(s)` (e.g. trace/explicit formula and correct limiting spectrum), not just the required reflection symmetry built in algebraically.

Calling F_P "3-adic" is not precise: F_P has characteristic 1,000,081, while the 3-adic field Q_3 has characteristic zero. Balanced ternary **encoding** is compatible with any numerical field but does not turn F_P into Q_3.

## New cross-check using the same Host8 inputs as the finite-field curve experiment

The full published 884736-byte slices were fetched through GitHub's connector and their 64-bit room words were decoded into 27 base-three digits, shifted to balanced trits {-1,0,+1}, then embedded modulo P. This directly tests the published spectral matrix on the same 288 room offsets used to sample the genus-2 curves (96 per sector), but **not** the private/unpublished `unmix(stub) ^ SEED` path described in the user's physical host test.

| Sector | Sampled rooms | Deterministic manifest matches | `sum(Tv) mod P == 0` |
|---|---:|---:|---:|
| 000 | 96 | 96 | 96 |
| 187 | 96 | 96 | 96 |
| 374 | 96 | 96 | 96 |
| **Total** | **288** | **288** | **288** |

This is a successful common-input software check. The Law-0 predicate is algebraically predetermined for *all* vectors, so its satisfaction is not experimental confirmation of the classical RH.

## Distinct mathematical domains

**Spectral construction:** 27-dimensional linear algebra over a million-element prime field, with mod-P skew symmetry and Fourier eigenpairs. Provides exact finite modular spectral pairing and DC-zero identity.

**Finite-field Weil computation:** curves `y^2 = x^5+a4*x^4+a3*x^3+a2*x^2+a1*x+a0` over F3; 288 Host8-selected curves, 194 smooth genus-2; 194/194 pass the exact zero-radius criterion, and 162/162 in the exhaustive 243-coefficient family. The theorem governing these zeros is known: RH for curves over finite fields (Weil). This is not classical RH.

**Physical Host8 status:** three published sample blocks are independently hash-verified. The original 300 GB hardware volume and the reported 71 local disk-readback tests were not independently mounted or rerun here. The 71-sample Rust integration test was not present in the inspected public spectral repository at this review.

## Recommended next mathematical proof obligation

Develop a **noncircular** operator-to-zeta bridge: specify a sequence of operators with increasing finite size and a mathematically controlled characteristic-zero limit, construct a spectral determinant/trace formula, and prove that this determinant or trace formula actually equals the classical Riemann xi/zeta data. In the short term add falsification controls: replace the 27 primes by shuffled or random integers while keeping the skew-symmetric construction, and show which properties change. The currently claimed critical-line property and `X[0]=0` should remain identical for those controls, demonstrating why these symmetries alone cannot distinguish zeta.

## Reproduce the independent modular tests

```bash
python verify_spectral_operator.py
```

This uses only the Python standard library and independently constructs the modular spectrum from the published constant definitions.
