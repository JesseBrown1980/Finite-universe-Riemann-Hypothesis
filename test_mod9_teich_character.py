"""Regression checks for the coefficient-only mod-9 character-sum baseline."""
import csv
import unittest
from pathlib import Path
from verify_mod9_teich_character import add9, mul9, pow9, f3, chi9, teich9, polynomial_only_invariants

ROOT=Path(__file__).resolve().parent

class Mod9TeichTests(unittest.TestCase):
    def test_field_F9(self):
        for a in range(9):
            for b in range(9):
                self.assertEqual(add9(a,b),add9(b,a))
                self.assertEqual(mul9(a,b),mul9(b,a))
                for c in range(9):
                    self.assertEqual(mul9(mul9(a,b),c),mul9(a,mul9(b,c)))
                    self.assertEqual(mul9(a,add9(b,c)),add9(mul9(a,b),mul9(a,c)))
            if a:
                self.assertEqual(pow9(a,8),1)
        self.assertEqual([chi9(i) for i in range(9)].count(0),1)

    def test_teich_characters(self):
        self.assertEqual([teich9(i) for i in range(3)],[0,1,8])
        self.assertEqual([f3((1,0,1,0,1),x) for x in range(3)],[1,1,2])
        r=polynomial_only_invariants(91)
        self.assertEqual((r['A_from_coeff'],r['B_from_coeff']),(1,1))
        self.assertEqual((r['A_mod9'],r['B_mod9']),(1,1))

    def test_all_162_and_naive_lift_failures(self):
        with (ROOT/'results'/'all_quintics.csv').open(newline='') as f:
            rows=[r for r in csv.DictReader(f) if r['smooth_genus2']=='1']
        self.assertEqual(len(rows),162)
        inv=[polynomial_only_invariants(int(r['code243'])) for r in rows]
        for i,r in enumerate(rows):
            self.assertEqual(inv[i]['A_from_coeff'],int(r['P1']))
            self.assertEqual(inv[i]['B_from_coeff'],int(r['P2']))
        self.assertEqual(sum(x['naive_A_match'] for x in inv),60)
        self.assertEqual(sum(x['naive_B_match'] for x in inv),47)
        Bs={x['B_from_coeff'] for x in inv}
        self.assertIn(7,Bs)
        self.assertIn(-2,Bs)
        self.assertEqual(7%9,(-2)%9)

if __name__=='__main__':
    unittest.main()
