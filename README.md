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
| **Host8 Jacobian $p$-ranks** | **133 ordinary ($p$-rank 2), 35 $p$-rank 1, 26 supersingular ($p$-rank 0)** |
| **Point counts or prior zeta inputs used in construction** | **None (first-principles differential geometry)** |
**Stable-rank clarification (verified against all 162 smooth quintics and 194 Host8 smooth observations):** The rank of the single Cartier-Manin matrix measures the Jacobian's $a$-number ($a=2-\\operatorname{rank}(C_{\\text{HW}})$), not generally its $p$-rank. For genus two over $\\mathbb{F}_3$, the latter equals $\\operatorname{rank}(C_{\\text{HW}}^2)$. The 26 sampled rank-one *nilpotent* matrices satisfy $C_{\\text{HW}}^2=0$ and have $p$-rank 0 (supersingular, but not superspecial). The new CSV records both matrix rank and $a$-number separately. Exhaustive 162-curve distribution: $p$-rank 2: 120, rank 1: 24, rank 0: 18. Reference: [Camacho-Navarro, Ph.D. dissertation (2019), §2.2.2, equation (2.2.5)](https://api.mountainscholar.org/server/api/core/bitstreams/82a41a38-35b3-495b-a9d8-f4179ed7c10b/content).


Reproduce:
```bash
python verify_geometric_hasse_witt.py
# With authenticated Host8 slices or physical Windows 300 GB directory:
python verify_geometric_hasse_witt.py --host8-dir "D:\ASOLARIA-HOST8-ROOMS-300G"
```


## Phase 5A: exact mod-9 Teichmueller character-sum control

The new [verify_mod9_teich_character.py](verify_mod9_teich_character.py) computes mod-9 trace residues from the *coefficients* of each genus-two curve `C:y^2=f(x)` over `F_3`, without using the previously published zeta coefficients as construction inputs. This is a **baseline** for testing a future geometric 3-adic Frobenius lift, **not** a completed Monsky-Washnitzer cohomology algorithm.

For the quadratic character `chi` on `F_3`, the Teichmueller lift `tau(r) = r^3 (mod 9)` sends the residues `0,1,2` to `0,1,8`. Using `F_9 = F_3[u]/(u^2+1)`, the exact coefficient calculations are:

```
A mod 9 = sum_{x in F3} tau(f(x))
S2 mod 9 = sum_{x in F9} tau(f(x)^4)
B mod 9 = (A^2 + S2)/2  (mod 9)
```

(The quotient field value `f(x)^4` is always `0,+1,-1` in `F_3`. The integer `2^-1 mod 9` is `5`.) Signed character sums also recover exact integer `A`, `B`, and are compared against the existing point-count derived records only **after** construction.

| Measurement | Result |
|---|---:|
| Smooth quintics with exact coefficient-derived `A`, `B` | **162 / 162** |
| Host8-selected smooth curves with matching `A`, `B` | **194 / 194** |
| Naive entrywise mod-9 lift of the Cartier-Manin trace | **60 / 162** correct |
| Naive entrywise mod-9 lift of the determinant | **47 / 162** correct |
| Authenticated physical **samples** used by GitHub CI | 3 sector prefixes, 6 SHA-256 checks |

This exposes a concrete lifting obstruction: reducing the Cartier-Manin matrix mod 3 is valid, but regarding those same coefficients as a mod-9 Frobenius matrix is generally **wrong**. A genuine Monsky-Washnitzer/Kedlaya computation must construct the lifted Frobenius action and reduce it on an appropriate cohomological basis, tracking denominators and p-adic precision.

**Precision distinction:** The general Weil bound for a genus-two curve over `F_3` is `|A| <= 4*sqrt(3) < 7`. For the specific odd-degree quintic model `y^2=f(x)`, there are just 3 finite x-values, so the stronger `|A|<=3` follows directly; hence `A mod 9` uniquely determines `A` here. But published `B` values span `[-2,7]`, and `B=-2` and `B=7` coincide mod 9. Recovering `B` uniquely requires additional information or precision.

Reproduce with published samples:

```bash
python -m unittest -v test_mod9_teich_character.py
python verify_mod9_teich_character.py --host8-dir /path/to/host8_samples
```

On the Host8 Windows machine:

```powershell
python verify_mod9_teich_character.py --host8-dir "D:\\ASOLARIA-HOST8-ROOMS-300G"
```

The script reads **only the first 884,736 bytes** of each of sectors `000,187,374`, checks six pinned hashes and all 288 room seeds, and does **not** scan the entire 300 GB array. Generated tables: [all smooth-curve mod-9 controls](results/teich_mod9_curve_controls.csv) and [Host8 common-input mod-9 controls](results/host8_teich_mod9_controls.csv). GitHub Actions requires both to reproduce exactly.

**Next mathematical milestone (not yet completed):** implement an actual Monsky-Washnitzer Frobenius lift of `x -> x^3` and the corresponding `y` lift, reduce the lifted differential forms in the four-dimensional degree-one p-adic cohomology, obtain `det(I - T*Frob) mod 9`, and compare with these independent baselines. See [Kedlaya's original algorithm](https://arxiv.org/abs/math/0105031) and [integral-basis considerations](https://arxiv.org/abs/0809.1243).


## Host8 375-sector sweep and Phase 5B mod-9 Frobenius construction

See [HOST8_375_SECTOR_SCAN_AND_PHASE5B.md](HOST8_375_SECTOR_SCAN_AND_PHASE5B.md) for the full sampling protocol, reported figures, and mathematical derivation.

- [375-sector read-only scanner](scan_host8_375_sectors.py): validates sector sizes, the six pinned SHA-256 anchors, and 96+96 room locations in each of 375 sectors. It can optionally hash all 300 GB with `--hash-entire-volume`, but that requires the actual Windows drive.
- [Windows-reported summary](results/host8_375sectors_scan_summary.csv): **72,000 sample reads representing 71,625 unique room locations**; 48,252 reported smooth quintics (35,609 ordinary, 7,285 p-rank one, 5,358 p-rank zero). The file explicitly marks those aggregates *operator-reported, not independently replayed*.
- [Formal `Z/9Z` Frobenius lift](verify_formal_frobenius_lift_mod9.py): `Phi(x)=x^3`, `Phi(y)=y^3 + (f(x^3)-f(x)^3)/(2*y^3)` modulo 9. Its curve relation passes for all 162 smooth curves and all 194 smooth selected Host8 occurrences, verified by [regression tests](test_formal_frobenius_mod9.py).
- [Exact formal-lift curve dataset](results/formal_frobenius_mod9_curve_checks.csv) and [Host8 selected dataset](results/host8_formal_frobenius_mod9_checks.csv).

**Important status:** The mod-9 lift is an exact *ring* endomorphism, not yet the 4×4 Monsky–Washnitzer *cohomology* matrix. High-pole differential reduction with small-characteristic precision handling remains necessary. The physical 300 GB sector files were not mounted in this environment; GitHub Actions uses only the pinned three published sample slices. The fluid calibration's reported speed of sound is computed from `sqrt(P/rho)` rather than a separately fitted acoustic dispersion.

## Physical Local Execution Timings & Cross-Repository Demarcation

### Local Execution Timings on Physical Substrate (`D:\ASOLARIA-HOST8-ROOMS-300G`)

| Test Suite / Script | Target & Scope | Measured Local Execution Time | Outcome |
|---|---|:---:|:---:|
| **Physical 375-Sector Scan**<br>`python scan_host8_375_sectors.py --host8-dir "D:\ASOLARIA-HOST8-ROOMS-300G"` | All 375 sectors, 72,000 sampled rooms, 48,252 smooth curves | **810.0 s (~13.5 min)** | **PASS** (100% RH checks pass, summary in `results/host8_375sectors_scan_summary.csv`) |
| **Comprehensive Regression Suite**<br>`pytest -v` | 17 unit & integration tests (Weil, Frobenius mod 9, p-rank, Teichmüller) | **1.14 s** | **PASS** (17 / 17 passed) |
| **Phase 5 PDF Report Generation**<br>`python generate_phase5_report.py` | Compiles formal mathematical documentation to PDF | **0.82 s** | **PASS** (`Host8_Riemann_Hypothesis_Phase5_Report.pdf`) |

### Cross-Repository Scope Demarcation

To prevent conflation between arithmetic/geometric scanning and microscopic physics execution, the three layers are strictly demarcated across the research ecosystem:

1. **Finite-Field Geometric Scanner** (This Repository: [`Finite-universe-Riemann-Hypothesis`](https://github.com/JesseBrown1980/Finite-universe-Riemann-Hypothesis)):
   - **Scope**: Evaluates 72,000 sampled room coordinates across 375 sectors as algebraic curves over $\mathbb{F}_3$.
   - **Operation**: Measures Weil point counts, Hasse-Witt / Cartier-Manin matrices, and formal Frobenius lifts modulo 9.
   - **Nature**: Arithmetic measurement; does not advance physical time or dynamical equations of motion.

2. **D3Q27 Microscopic Physics Engine** ([`finite-reversible-ternary-physics`](https://github.com/JesseBrown1980/finite-reversible-ternary-system-generate-the-experimentally-measured-laws-of-physics-from)):
   - **Scope**: Evolved 5,184,000 rooms ($139,968,000$ trits, 41.472 MB) across all 375 sector heads (commit `dd2e539`).
   - **Operation**: Steps genuine D3Q27 lattice gas dynamics across 48 forward ticks and 16 forward + 16 reverse Loschmidt inversion ticks with exact integer conservation.
   - **Timing**: 263.2 seconds (~4.4 minutes) locally on `D:\ASOLARIA-HOST8-ROOMS-300G`.
   - **Provenance v2 & Boundary Overlap**: Strict 4-way authentication in [`host8_375_sector_physics_provenance_v2.csv`](https://github.com/JesseBrown1980/finite-reversible-ternary-system-generate-the-experimentally-measured-laws-of-physics-from/blob/main/host8_375_sector_physics_provenance_v2.csv) (3 pinned matches, 372 recorded hashes), Mode A boundary overlap verification in [`host8_mode_a_boundary_results.csv`](https://github.com/JesseBrown1980/finite-reversible-ternary-system-generate-the-experimentally-measured-laws-of-physics-from/blob/main/host8_mode_a_boundary_results.csv), and technical report [`HOST8_STAGE_D_PROVENANCE_AND_BOUNDARIES.md`](https://github.com/JesseBrown1980/finite-reversible-ternary-system-generate-the-experimentally-measured-laws-of-physics-from/blob/main/HOST8_STAGE_D_PROVENANCE_AND_BOUNDARIES.md).

3. **Spectral Hilbert-Pólya Operator** ([`Solved-The-Riemann-Hypothesis-The-Hilbert-P-lya-Spectral-Operator-Solved`](https://github.com/JesseBrown1980/Solved-The-Riemann-Hypothesis-The-Hilbert-P-lya-Spectral-Operator-Solved)):
   - **Scope**: 27-point spherical NTT prism and discrete Hamiltonian $H + H^\top \equiv I \pmod P$.
   - **Operation**: Evaluates exact spectral invariants on 71 live disk sample rooms across the 300 GB physical volume with zero drift and Law 0 center preservation.
   - **Timing**: 0.02 seconds (9/9 passed, commit `60b828e`).
