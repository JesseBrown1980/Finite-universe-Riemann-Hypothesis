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

### Important interpretation

This verifies a known theorem in a reproducible ternary computational setting. The finite-field function-field analogue is mathematically different from the classical Riemann zeta function, whose Riemann hypothesis remains open. There is not yet a justified bridge between the Host8 finite-state dynamics and the zeros of classical `zeta(s)`.

References: [Weil's theorem for curves](https://math.richardgriffon.me/CFF/ln/LecNotes_05.pdf); [Clay Riemann Hypothesis](https://www.claymath.org/millennium/Riemann-Hypothesis/).
