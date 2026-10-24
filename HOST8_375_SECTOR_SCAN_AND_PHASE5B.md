# Host8 375-Sector Sampling Sweep and Phase 5B Formal Frobenius

## Evidence and reproducibility

**Physical Host8 volume is not mounted in GitHub Actions or the independent container.** The physical Windows run statistics below were supplied by the Host8 operator. Their aggregate arithmetic has been checked, but raw offsets from all 375 sectors were not delivered for an independent replay.

| Windows-reported dataset | Canonical grid | Deep grid | Combined |
|---|---:|---:|---:|
| Sectors with expected file sizes | 375 | 375 | 375 |
| Room measurements | 36,000 | 36,000 | 72,000 |
| Smooth genus-two samples | 24,077 | 24,175 | 48,252 |
| Smooth with finite-field RH PASS | 24,077 | 24,175 | 48,252 |
| Stable Jacobian p-rank 2 | 17,681 | 17,928 | 35,609 |
| Stable Jacobian p-rank 1 | 3,692 | 3,593 | 7,285 |
| Stable Jacobian p-rank 0 | 2,704 | 2,654 | 5,358 |

*The 72,000 measurements contain 375 repeated room-zero positions because both grids include offset zero. There are **71,625 distinct room locations**.*

At every sector, the canonical room indices are `floor(j*110591/95)` and deep indices are `floor(j*99999999/95)` for `j=0...95`. These give **192 room reads × 375 sectors = 72,000 measurements**, totalling **576,000 bytes** of sampled room payload. The 375 sector file-size checks cover 375×800,000,000=300,000,000,000 bytes **by metadata**, not by a full-byte sequential read. All six previously authenticated reference hashes cover 110,592-byte and 884,736-byte prefixes from sectors 000, 187, and 374.

The independently verified smooth fraction of the *complete set* of 243 coefficient seeds is `162/243 = 2/3`; for 72,000 hypothetical independent uniform samples its expected count is 48,000 with standard deviation about 126.49. The Windows-reported 48,252 is about 1.99 such standard deviations above expectation, but samples are deterministic, overlapping and potentially correlated, so this simple binomial approximation **is not a formal independence test**.

The published `results/host8_375sectors_scan_summary.csv` is **explicitly marked as user-reported**, not as CI-confirmed live-drive measurements. The source `scan_host8_375_sectors.py` permits independent reproduction of the scanner and, when the Windows volume is available, emits a fresh, provenance-tagged summary and sector-by-sector payload hashes.

### Physical Windows commands

```powershell
cd C:\Finite-universe-Riemann-Hypothesis
git pull origin main

# Verify sizes on all 375 sectors; cryptographic anchors on 3;
# sample 96+96 room positions per sector.
python scan_host8_375_sectors.py --host8-dir "D:\ASOLARIA-HOST8-ROOMS-300G"

# Optional: ALSO read and hash EVERY BYTE of all 375 sectors.
python scan_host8_375_sectors.py --host8-dir "D:\ASOLARIA-HOST8-ROOMS-300G" --hash-entire-volume
```

The second command computes fresh per-sector SHA-256 digests, but those digests require an independent trusted reference to authenticate their origin. Both commands are read-only with respect to the physical sector files; report output files in `results/` are overwritten intentionally.

### GitHub CI fixture

CI downloads the three 884,736-byte pinned sector slices from the physics repository at `5a7e9a2`. The scanner smoke test verifies their six prefixes and computes full SHA-256 for each of these three *sample files*; the complete 300 GB host is never available to that test. Independent synthetic fixture tests enforce failure on missing or truncated sector files.

## Phase 5B: algebraic Frobenius lift mod 9 — completed

For a monic smooth quintic `f(x)` with integer lifts of its `F_3` coefficients, define

```
Delta(x) = f(x^3) - f(x)^3
```

Every coefficient of `Delta` is divisible by 3. Work in the localized coordinate algebra

```
R_9 = (Z/9Z)[x,y,y^(-1)] / (y^2 - f(x)).
```

The exact mod-9 endomorphism

```
Phi(x) = x^3
Phi(y) = y^3 + (1/2)*Delta(x)*y^(-3)   (mod 9)
```

has `1/2=5 (mod 9)`. Expanding its defining relation,

```
Phi(y)^2
  = y^6 + Delta(x) + (1/4)*Delta(x)^2*y^(-6)
  = f(x^3) (mod 9),
```

because `Delta^2` is divisible by 9. It reduces to the absolute cube Frobenius modulo 3. The implementation uses exact integer polynomial coefficients, and enforces this algebraic identity across all 162 smooth quintics and their 194 Host8-selected occurrences.

Files: `verify_formal_frobenius_lift_mod9.py`, `test_formal_frobenius_mod9.py`, `results/formal_frobenius_mod9_curve_checks.csv`, `results/host8_formal_frobenius_mod9_checks.csv`.

### Remaining challenge: four-dimensional cohomological Frobenius

**The 4×4 Monsky–Washnitzer matrix has NOT been computed.** The formal affine ring lift is an authentic first construction step, not its cohomological reduction.

Pulling back the degree-one differential basis `omega_i=x^i dx/(2y)`, `i=0,1,2,3`, gives (before reduction)

```
Phi*(omega_i) = 3*x^(3i+2)*dx/(2*y^3) (mod 9).
```

The simplification modulo 9 **cannot safely be applied before cohomological reduction**, because reduction of high-pole terms can divide by 3 and lose precision. A correct small-characteristic implementation must retain guard digits, account for denominators, reduce lifted differentials in a suitable integral basis, and then compute `det(I-T*Frob)` to precision 9.

SageMath's `hypellfrob` routine requires `p>(2g+1)(2N-1)`, which fails for `p=3,g=2,N=2`. See [Sage reference](https://doc.sagemath.org/html/en/reference/arithmetic_curves/sage/schemes/hyperelliptic_curves/hyperelliptic_finite_field.html), [Kedlaya's original framework](https://arxiv.org/abs/math/0105031), and [integral basis/precision considerations](https://arxiv.org/abs/0809.1243). Until that reduction is implemented and validated independently, no exact integer `A` derived from cohomology modulo 9 is claimed.

## Fluid input interpretation

In the source `asolaria_fluid_hydro_calibration.cpp` of `Neural-network-inside-a-neural-network-using-trits-to-resolve-Finiteness`, 5,184 Host8 stubs are read from **sector 000**. The decoded `base_trit` is not used as the final occupancy: the initializer computes a shear-biased occupancy using shifted stub bits, deliberately imposing a flow profile. The reported `c_s` is computed as `sqrt(P_iso/rho)`, an equation-of-state proxy rather than independent acoustic time-of-flight; the reported `nu_eff` comes from a shear-contrast logarithmic decay estimator. These measurements may be useful numerical calibration quantities but are not yet independent constitutive-law validations.
