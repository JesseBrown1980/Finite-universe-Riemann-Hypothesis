"""Regression tests: Hasse-Witt matrix rank is NOT the Jacobian stable p-rank."""
import csv
from pathlib import Path
import unittest
from verify_geometric_hasse_witt import hasse_witt_invariants, hasse_witt_matrix, rank_2x2_mod3

ROOT = Path(__file__).resolve().parent


def product_mod3(m):
    return tuple(tuple(sum(m[i][k] * m[k][j] for k in range(2)) % 3
                       for j in range(2)) for i in range(2))


class StablePRankTests(unittest.TestCase):
    def test_nilpotent_matrix_rank_one_prank_zero(self):
        m = hasse_witt_matrix(0,0,0)
        self.assertEqual(rank_2x2_mod3(m),1)
        self.assertEqual(product_mod3(m),((0,0),(0,0)))
        self.assertEqual(hasse_witt_invariants(0,0,0), (0,0,0))

    def test_matrix_rank_one_prank_one(self):
        m = hasse_witt_matrix(0,0,1)
        self.assertEqual(rank_2x2_mod3(m),1)
        self.assertEqual(rank_2x2_mod3(product_mod3(m)),1)
        self.assertEqual(hasse_witt_invariants(0,0,1)[2],1)

    def test_exhaustive_162_curves(self):
        with (ROOT/'results'/'all_quintics.csv').open(newline='') as f:
            rows=[r for r in csv.DictReader(f) if r['smooth_genus2']=='1']
        counts={0:0,1:0,2:0}
        for r in rows:
            a1,a2,a4=(int(r['a'+str(j)]) for j in (1,2,4))
            m=hasse_witt_matrix(a1,a2,a4)
            tr,det,prank=hasse_witt_invariants(a1,a2,a4)
            self.assertEqual(prank,rank_2x2_mod3(product_mod3(m)))
            self.assertEqual(tr,(-int(r['P1']))%3)
            self.assertEqual(det,int(r['P2'])%3)
            counts[prank]+=1
        self.assertEqual(counts,{0:18,1:24,2:120})

    def test_host8_194_observations(self):
        with (ROOT/'results'/'host8_geometric_hasse_witt_results.csv').open(newline='') as f:
            rows=[r for r in csv.DictReader(f) if r['is_smooth']=='1']
        counts={0:0,1:0,2:0}
        for r in rows:
            a1,a2,a4=(int(r['a'+str(j)]) for j in (1,2,4))
            m=hasse_witt_matrix(a1,a2,a4)
            _,_,prank=hasse_witt_invariants(a1,a2,a4)
            matrix_rank=rank_2x2_mod3(m)
            self.assertEqual(prank,int(r['p_rank']))
            self.assertEqual(prank,rank_2x2_mod3(product_mod3(m)))
            self.assertEqual(matrix_rank,int(r['HW_matrix_rank']))
            self.assertEqual(int(r['a_number']),2-matrix_rank)
            counts[prank]+=1
        self.assertEqual(counts,{0:26,1:35,2:133})


if __name__=='__main__':
    unittest.main()
