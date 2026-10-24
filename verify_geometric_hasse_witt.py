#!/usr/bin/env python3
"""
Phase 4: Direct Geometric Operator — Cartier-Manin / Hasse-Witt Matrix on H^0(C, Omega^1).

Constructs the 2x2 Cartier-Manin operator matrix directly from the curve's
differential geometry over F_3:
    C: y^2 = x^5 + a4*x^4 + a3*x^3 + a2*x^2 + a1*x + a0
WITHOUT counting points or supplying prior zeta coefficients A, B.

Manin's Theorem (1961):
For C: y^2 = f(x) over F_3, the Cartier operator on the canonical basis
omega_1 = dx/y, omega_2 = x*dx/y of regular differentials H^0(C, Omega^1)
has matrix:
    C_HW = [[a2, 1],
            [a1, a4]]  in M_(2x2)(F_3)

Its characteristic polynomial yields the exact mod-3 reduction of the zeta polynomial:
    det(I - T * C_HW) = 1 - Tr(C_HW)*T + det(C_HW)*T^2
                      = 1 + A*T + B*T^2  (mod 3)

This proves:
    Tr(C_HW) = a2 + a4 = -A  (mod 3)
    det(C_HW) = a2*a4 - a1 = B  (mod 3)
"""

from __future__ import annotations
import argparse
import csv
from pathlib import Path
from host8_ternary_weil import read_host8, read_manifest, trits


def hasse_witt_matrix(a1: int, a2: int, a4: int) -> tuple[tuple[int, int], tuple[int, int]]:
    """Construct Cartier-Manin / Hasse-Witt matrix on H^0(C, Omega^1) over F_3."""
    return ((a2 % 3, 1), (a1 % 3, a4 % 3))


def hasse_witt_invariants(a1: int, a2: int, a4: int) -> tuple[int, int, int]:
    """Compute (trace mod 3, det mod 3, p-rank) of C_HW."""
    tr = (a2 + a4) % 3
    det = (a2 * a4 - a1) % 3
    # Rank over F_3
    if det != 0:
        p_rank = 2  # ordinary curve
    elif any(x % 3 != 0 for x in (a2, 1, a1, a4)):
        p_rank = 1  # 1-rank
    else:
        p_rank = 0  # superspecial / supersingular
    return (tr, det, p_rank)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--curves', type=Path, default=Path(__file__).resolve().parent / 'results' / 'all_quintics.csv')
    parser.add_argument('--host8-dir', type=Path, default=None, help='Physical Host8 directory or published slices')
    parser.add_argument('--manifest', type=Path, default=Path(__file__).resolve().parent / 'data' / 'host8_seed_manifest.csv')
    parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parent / 'results' / 'host8_geometric_hasse_witt_results.csv')
    args = parser.parse_args()

    # 1. Exhaustive verification on all 162 smooth curves
    with args.curves.open(newline='') as f:
        all_curves = list(csv.DictReader(f))

    smooth_curves = [r for r in all_curves if r['smooth_genus2'] == '1']
    assert len(smooth_curves) == 162

    tr_matches = 0
    det_matches = 0
    for r in smooth_curves:
        a1, a2, a4 = int(r['a1']), int(r['a2']), int(r['a4'])
        A, B = int(r['P1']), int(r['P2'])
        tr, det, _ = hasse_witt_invariants(a1, a2, a4)
        if tr == (-A) % 3:
            tr_matches += 1
        if det == B % 3:
            det_matches += 1

    assert tr_matches == 162
    assert det_matches == 162
    print(f"PASS: 162/162 smooth curves: Cartier-Manin matrix on H^0(C, Omega^1) identically matches P_C(T) mod 3")
    print(f"      Tr(C_HW) == -A (mod 3) and det(C_HW) == B (mod 3) derived purely from differential geometry")

    # 2. Host8 common-input verification
    records = read_host8(args.host8_dir) if args.host8_dir else read_manifest(args.manifest)
    if args.host8_dir and args.manifest.is_file():
        assert records == read_manifest(args.manifest)

    from_curve_csv = Path(__file__).resolve().parent / 'results' / 'host8_curve_results.csv'
    with from_curve_csv.open(newline='') as f:
        host8_curves = list(csv.DictReader(f))
    assert len(host8_curves) == len(records)

    host8_rows = []
    smooth_host8 = 0
    hw_matches = 0
    p_ranks = {0: 0, 1: 0, 2: 0}

    for idx, (sec, j, cell, code) in enumerate(records):
        cr = host8_curves[idx]
        assert (cr['sector'], int(cr['sample'])) == (sec, j)
        is_smooth = int(cr['smooth_genus2'])
        a0, a1, a2, a3, a4 = trits(code, 5)

        if is_smooth:
            smooth_host8 += 1
            A = int(cr['P1'])
            B = int(cr['P2'])
            tr, det, p_rk = hasse_witt_invariants(a1, a2, a4)
            p_ranks[p_rk] += 1
            exp_tr = (-A) % 3
            exp_det = B % 3
            match = int(tr == exp_tr and det == exp_det)
            if match:
                hw_matches += 1

            host8_rows.append({
                'sector': sec, 'sample': j, 'cell_index': cell, 'code243': code,
                'is_smooth': 1,
                'a0': a0, 'a1': a1, 'a2': a2, 'a3': a3, 'a4': a4,
                'P1': A, 'P2': B,
                'HW_trace': tr, 'HW_det': det, 'p_rank': p_rk,
                'expected_tr_mod3': exp_tr, 'expected_det_mod3': exp_det,
                'geometric_match': match
            })
        else:
            host8_rows.append({
                'sector': sec, 'sample': j, 'cell_index': cell, 'code243': code,
                'is_smooth': 0,
                'a0': a0, 'a1': a1, 'a2': a2, 'a3': a3, 'a4': a4,
                'P1': '', 'P2': '',
                'HW_trace': '', 'HW_det': '', 'p_rank': '',
                'expected_tr_mod3': '', 'expected_det_mod3': '',
                'geometric_match': 0
            })

    assert smooth_host8 == 194
    assert hw_matches == 194

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(host8_rows[0].keys()))
        writer.writeheader()
        writer.writerows(host8_rows)

    print(f"PASS: 194/194 Host8 smooth curves match Cartier-Manin operator invariants mod 3")
    print(f"      Host8 Jacobian p-ranks: ordinary (rank 2) = {p_ranks[2]}, 1-rank = {p_ranks[1]}, supersingular = {p_ranks[0]}")
    print(f"Exported geometric operator results to {args.output}")


if __name__ == '__main__':
    main()
