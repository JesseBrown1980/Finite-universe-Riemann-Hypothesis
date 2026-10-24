"""Regression tests for the exact formal characteristic-three Frobenius lift."""
import csv
from pathlib import Path
import unittest
from verify_formal_frobenius_lift_mod9 import delta_polynomial,check_frobenius,multiply

ROOT=Path(__file__).resolve().parent

class FormalLiftTests(unittest.TestCase):
    def test_all_coefficients_frobenius_delta_divisible_by3(self):
        for code in range(243):
            c=tuple((code//3**i)%3 for i in range(5))
            delta=delta_polynomial(c)
            self.assertEqual(len(delta),16)
            self.assertTrue(all(a%3==0 for a in delta))

    def test_exact_mod9_curve_relation(self):
        with (ROOT/'results'/'all_quintics.csv').open(newline='') as f:
            rows=[r for r in csv.DictReader(f) if r['smooth_genus2']=='1']
        self.assertEqual(len(rows),162)
        for row in rows:
            coeff=tuple(int(row['a'+str(i)]) for i in range(5))
            t=check_frobenius(coeff)
            self.assertEqual(t['formal_lift_relation_pass'],1)
            self.assertEqual(t['frobenius_mod3_pass'],1)
            self.assertEqual(t['nontrivial_delta_mod9'],1)
            delta=delta_polynomial(coeff)
            correction=[5*a%9 for a in delta]
            self.assertTrue(all((2*b-a)%9==0 for b,a in zip(correction,delta)))
            self.assertTrue(all(x%9==0 for x in multiply(correction,correction)))

    def test_host8_linkage(self):
        with (ROOT/'results'/'host8_formal_frobenius_mod9_checks.csv').open(newline='') as f:
            rows=list(csv.DictReader(f))
        self.assertEqual(len(rows),288)
        self.assertEqual(sum(int(r['smooth_genus2']) for r in rows),194)
        self.assertEqual(sum(int(r['formal_lift_relation_pass']) for r in rows if r['smooth_genus2']=='1'),194)

if __name__=='__main__':
    unittest.main()
