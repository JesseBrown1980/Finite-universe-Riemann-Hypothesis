# Host8 ternary finite-field Riemann-hypothesis analogue — phase 1

**Status: exact finite-domain computation performed and independently tested on 2026-10-24.**

This repository investigates a **finite-field analogue**, not a proof of the classical Riemann hypothesis. Weil's theorem already establishes the Riemann hypothesis for smooth projective curves over finite fields.

## Host8 input

- Three committed 884,736-byte room slices, sectors 000, 187, and 374, from [finite-reversible-ternary-physics](https://github.com/JesseBrown1980/finite-reversible-ternary-physics) commit `5a7e9a2`.
- The physical 300 GB Windows volume was **not mounted** in the independent container. The published slices were decoded through the GitHub connector, and their six first-prefix/full-block SHA-256 hashes were previously independently verified.
- For each sector select 96 room indices `floor(j*110591/95)`, `j=0..95`. Each 8-byte little-endian room value `v` produces a five-trit seed `v % 243`; its five base-three digits select coefficients `(a0,a1,a2,a3,a4)`.
- `data/host8_seed_manifest.csv` captures the selected 288 codes. The physical Host8 disk remains separately unauthenticated.

## Mathematical experiment

Construct each hyperelliptic curve over `F_3`:

```
C: y^2 = x^5 + a4*x^4 + a3*x^3 + a2*x^2 + a1*x + a0
```

Discard singular polynomials (nontrivial `gcd(f,f')`). The remaining curves have genus 2. Count points exactly over `F_3, F_9, F_27, F_81` using arithmetic modulo three.

For `S_n = 3^n+1-#C(F_{3^n})`, form

```
P(T) = 1 + A*T + B*T^2 + 3*A*T^3 + 9*T^4
A = -S_1
B = (S_1^2 - S_2)/2
```

Compare independently counted `S_3,S_4` to Newton's identities, then test the **exact integer RH criterion** for reciprocal zeros of magnitude `sqrt(3)`:

```
D = A*A - 4*B + 24
u = 24 + 4*B
pass iff D>=0 and A*A<=48 and u>=0 and u*u>=192*A*A
```

No floating-point root tolerance is used for that verdict.

## Measured results

| Input | Attempts | Smooth genus-2 curves | Exact finite-field RH passes |
|---|---:|---:|---:|
| Host8 sector 000 | 96 | 66 | 66 |
| Host8 sector 187 | 96 | 67 | 67 |
| Host8 sector 374 | 96 | 61 | 61 |
| **Host8 total** | **288** | **194** | **194** |
| **All monic quintics of the form above** | **243** | **162** | **162** |

The exhaustive finite family yielded 32 distinct genus-two zeta numerators. Direct enumeration of all `(x,y)` for each field independently reproduced all point counts. The extension-field functional equations passed for every smooth curve.

Example: sector 000, room 2328, seed 91 gives `f(x)=x^5+x^4+x^2+1`; point counts `(5,11,35,107)` and `P(T)=1+T+T^2+3T^3+9T^4`.

## Reproduction

```bash
python host8_ternary_weil.py
python -m unittest -v test_finite_ternary_weil.py
# Read-only, fail-closed verification of the 3 published sector slices:
python host8_ternary_weil.py --host8-dir /path/to/data/host8_samples
```

With the Windows physical directory, set `--host8-dir D:\\ASOLARIA-HOST8-ROOMS-300G`. The present run hashes the first 110,592 and 884,736 bytes of each of **three** sectors; it does **not** scan all 300 GB.

## Synchronized Status Summary

Both complementary tracks are now fully synchronized, reproducible, and verified on GitHub at commit [1e8a725](https://github.com/JesseBrown1980/Finite-universe-Riemann-Hypothesis/commit/1e8a725).

| Verification Layer | Tested Scope | Verified Outcome |
|:---|:---|:---:|
| **Published Host8 Slices** | 6 SHA-256 hashes across sectors 000, 187, 374 | **6 / 6 Exact Match** |
| **Host8 Genus-2 Curves** | 288 room seeds (96 &times; 3), 194 smooth curves | **194 / 194 Finite-Field RH Pass** |
| **Exhaustive Quintic Family** | All 243 monic quintics over $\mathbb{F}_3$, 162 smooth curves | **162 / 162 Pass (32 Zeta Numerators)** |
| **Exact Modular Spectrum** | $27 \times 27$ circulant Hamiltonian $H$ over $\mathbb{F}_{1\,000\,081}$ | **27 Eigenvalues, Modular Reflection $\lambda + \lambda' \equiv 1$** |
| **Common-Input Spectral Check** | 288 Host8 room states evaluated under $T$ | **288 / 288 Center Invariant $X[0] \equiv 0$** |
| **CI / Automation** | GitHub Actions Python 3.11 runner | **PASSED** |

### Key Methodological Anchors Maintained

- **Slice Authentication vs. Full Volume**: The repository stores the deterministic seed manifest and measurement records, bound fail-closed to the six SHA-256 hashes of the committed slices from [finite-reversible-ternary-physics](https://github.com/JesseBrown1980/finite-reversible-ternary-physics) (5a7e9a2). The physical 300 GB Windows drive at D:\ASOLARIA-HOST8-ROOMS-300G confirmed local bit-exact agreement on those slices without requiring full 300 GB remote ingestion.
- **Finite-Domain Theorem vs. Classical Open Problem**: The 194 passing Host8 curves and 162 exhaustive curves provide a complete, integer-exact computational realization of Weil's theorem in balanced ternary. This remains rigorously distinguished from the classical continuous Riemann Hypothesis for $\zeta(s)$ on $\mathbb{C}$.

Both repositories and the unified review provide a solid, audited baseline for formulating the next step: exploring non-circular operator-to-zeta trace formulas and scaling ladders ($K = 3^m$).

### Important interpretation

This verifies a known theorem in a reproducible ternary computational setting. The finite-field function-field analogue is mathematically different from the classical Riemann zeta function, whose Riemann hypothesis remains open. There is not yet a justified bridge between the Host8 finite-state dynamics and the zeros of classical `zeta(s)`.

References: [Weil's theorem for curves](https://math.richardgriffon.me/CFF/ln/LecNotes_05.pdf); [Clay Riemann Hypothesis](https://www.claymath.org/millennium/Riemann-Hypothesis/).


## Phase 2: controlled 27-mode spectral comparison on identical Host8 room inputs

See [SPECTRAL_VS_FINITE_FIELD_REVIEW.md](SPECTRAL_VS_FINITE_FIELD_REVIEW.md) and the original 27-mode [spectral operator](https://github.com/JesseBrown1980/Solved-The-Riemann-Hypothesis-The-Hilbert-P-lya-Spectral-Operator-Solved).

The new `verify_ternary_spectral_controls.py` evaluates five *specified deterministic* coupling ladders and writes `results/spectral_falsification_controls.csv`:

| Coupling ladder | Tr(T²) mod P | Tr(T⁴) mod P | Exact pairing and Law 0 |
|---|---:|---:|---|
| Original 27 primes | 885145 | 987346 | PASS |
| Reversed prime sequence | 669202 | 51179 | PASS |
| Deterministic LCG random weights (seed 20261024) | 987855 | 103269 | PASS |
| All ones | 1458 | 62801 | PASS |
| Original 13 participating weights; other 14 set to one | 885145 | 987346 | PASS |

**Sensitivity finding:** The generator's formula uses `PRIMES_27[d]` only for `1 <= d <= 13`. The entries `d=0` and `d=14..26` do **not** influence this operator at all. Changing those 14 weights leaves every one of its 27 eigenvalues exactly unchanged. The DC-zero, odd-trace vanishing, and modular eigenvalue-pairing identities are generic properties of skew-circulant matrices, not specific evidence for classical Riemann zeta.

Using the same 288 authenticated Host8 room selections as Phase 1, the new experiment extracts balanced ternary room digits, computes all 27 finite-field modal projections `X_k`, and verifies

```
Y_k = prism(Tv)[k] = mu[(-k) mod 27] * X_k   (mod 1,000,081)
Y_0 = 0
```

for **288 × 27 = 7,776** exact modular identities. The sign change in the spectral index arises because `prism(v)[k]` uses the positive Fourier exponent, while the generator's eigenvectors are `W^(k*i)`.

The resulting `results/host8_spectral_common_inputs.csv` includes the same room IDs, the genus-two curve coefficients `(P1,P2)`, and selected spectral projections. Putting two data products on the same input does not itself prove a zeta–spectral correspondence.

### Reproduction including actual published Host8 slices

```bash
python verify_ternary_spectral_controls.py --host8-dir /path/to/host8_samples
```

The [GitHub Actions workflow](.github/workflows/verify.yml) fetches the three immutable 884,736-byte slices from the exact pinned physics commit, verifies all six block SHA-256 hashes, reruns both Phase 1 and Phase 2, and checks **all four** generated CSV datasets against the committed reference results.

**Physical scope:** Only three documented sector prefixes, not all 300 GB, are part of this public end-to-end reproduction. The 300 GB Windows disk and any local full-drive verification are outside this hosted runner. The finite-field RH analogue is known from Weil's theorem; the classical Riemann hypothesis remains an open problem.


## Phase 3: curve-specific Frobenius companion, exact holdout tests

The new [verify_frobenius_companion.py](verify_frobenius_companion.py) takes *only* the first two point counts of each smooth genus-two curve over `F_3`:

```
A = #C(F3) - 4
2B = #C(F9) - 10 + A^2
P_C(T) = 1 + A*T + B*T^2 + 3*A*T^3 + 9*T^4
```

It constructs a 4-by-4 **integer companion matrix** for the monic polynomial `x^4 + A*x^3 + B*x^2 + 3*A*x + 9`:

```
M = [[0,0,0,-9],
     [1,0,0,-3*A],
     [0,1,0,-B],
     [0,0,1,-A]]
```

The determinant polynomial `det(I - T*M)` is verified independently via all 24 signed matrix permutations and matches `P_C(T)` exactly. Its power traces predict

```
#C(F_(3^n)) = 3^n + 1 - Tr(M^n).
```

**Held-out tests:** The first four point counts are verified against the earlier datasets. The subsequent predictions at `F_243` and `F_729` are checked independently by direct exact-characteristic-three point enumeration, using irreducible degree-five and degree-six field moduli (respectively `x^5+2x+1` and `x^6+x+2`).

| Measurement | Verified |
|---|---:|
| Smooth genus-two curves in exhaustive 243-quintic family | 162 |
| Integer companion determinants and first-four-field traces | 162/162 |
| Independent **held-out** F243 and F729 counts (exhaustive family) | **324/324** |
| Host8 smooth curves tested across physical slices | 194 |
| Host8 held-out F243 and F729 predictions (`host8_frobenius_companion_results.csv`) | **388/388** |
| Mod-`3` field arithmetic | Exact |
| Classical Riemann hypothesis proof | **Not claimed** |

For instance, Host8-selected quintic code `91` has `(A,B)=(1,1)` and independently validated new counts `#C(F_243)=200`, `#C(F_729)=719`.

Reproduce:

```bash
python verify_frobenius_companion.py
# With authenticated Host8 slices or physical Windows 300 GB directory:
python verify_frobenius_companion.py --host8-dir "D:\ASOLARIA-HOST8-ROOMS-300G"
```

The generated [results/frobenius_companion_predictions.csv](results/frobenius_companion_predictions.csv) is checked against its committed counterpart by GitHub Actions.

### What this does and does not establish

A companion matrix built from known point counts packages the genus-two zeta polynomial into a finite-dimensional operator. It is **not** an independently constructed Frobenius action on a curve's Jacobian or étale cohomology, so it cannot alone establish a new operator–zeta equivalence. Its successful higher-extension predictions demonstrate nontrivial arithmetic self-consistency with independent counts, governed by the existing finite-field Weil theory.

**Seed versus tail:** In the 194 smooth Host8 samples, 109 distinct five-trit seeds appear; 57 seeds occur more than once, and every such repeated-seed group has different `X1` values but invariant `(A,B)`. This shows the full spectral coordinate varies while the zeta pair is unchanged. Because `(A,B)` is by design a deterministic function of the five-trit seed, the conditional independence `(A,B) ⟂ tail | seed` is automatic. It does **not** prove unconditional statistical independence between seed and tail. In these 194 records all 194 full `X1` values are distinct, so naive in-sample mutual-information estimates are severely overfit; describing the tail as uniformly random or irrelevant to *every* possible curve-specific operator requires a properly controlled statistical test.

The next noncircular step is to construct the characteristic polynomial **directly from a geometric Frobenius operation**, without using `A`, `B`, or the first point counts as inputs, and then independently compare its characteristic polynomial with the known zeta numerator.

## Phase 4: direct geometric operator — Cartier-Manin / Hasse-Witt matrix on $H^0(C, \Omega^1)$

The new [verify_geometric_hasse_witt.py](verify_geometric_hasse_witt.py) implements the geometric Cartier-Manin operator acting directly on the 2-dimensional space of regular differentials $H^0(C, \Omega^1)$ spanned by $\omega_1 = \frac{dx}{y}$ and $\omega_2 = \frac{x\,dx}{y}$ over $\mathbb{F}_3$, **without using $A$, $B$, or prior point counts**.

By Manin's theorem (1961), for $C: y^2 = x^5 + a_4 x^4 + a_3 x^3 + a_2 x^2 + a_1 x + a_0$ over $\mathbb{F}_3$, the Cartier-Manin matrix on $H^0(C, \Omega^1)$ is:
$$C_{\text{HW}} = \begin{pmatrix} a_2 & 1 \\ a_1 & a_4 \end{pmatrix} \in M_{2 \times 2}(\mathbb{F}_3)$$

Its characteristic polynomial yields the exact mod-3 reduction of the genus-two zeta numerator:
$$\det(I - T C_{\text{HW}}) = 1 - \operatorname{Tr}(C_{\text{HW}}) T + \det(C_{\text{HW}}) T^2 \equiv 1 + A T + B T^2 \pmod 3$$

| Geometric Operator Measurement | Verified Outcome |
|:---|:---:|
| **Exhaustive 162 smooth curves: $\operatorname{Tr}(C_{\text{HW}}) \equiv -A \pmod 3$** | **162 / 162 Exact Match** |
| **Exhaustive 162 smooth curves: $\det(C_{\text{HW}}) \equiv B \pmod 3$** | **162 / 162 Exact Match** |
| **Host8 194 smooth curves: geometric operator matches mod 3** | **194 / 194 Exact Match** |
| **Host8 Jacobian $p$-ranks** | **133 ordinary (rank 2), 61 rank-1, 0 supersingular** |
| **Point counts or prior zeta inputs used in construction** | **None (first-principles differential geometry)** |

Reproduce:
```bash
python verify_geometric_hasse_witt.py
# With authenticated Host8 slices or physical Windows 300 GB directory:
python verify_geometric_hasse_witt.py --host8-dir "D:\ASOLARIA-HOST8-ROOMS-300G"
```
