"""Finite exact reduction, independent counted-zeta controls, and guarded stability."""
import csv
from pathlib import Path
import unittest
from finite_frobenius_mod9 import compute,Q,mod9,v3
from host8_ternary_weil import trits,nonsingular
from verify_finite_frobenius_mod9 import curves,SCALE

ROOT=Path(__file__).resolve().parent

class FiniteFrobeniusTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.coeffs=[trits(c,5) for c in range(243) if nonsingular(trits(c,5))]
        with (ROOT/'results'/'all_quintics.csv').open(newline='') as f:
            cls.reference={int(r['code243']):r for r in csv.DictReader(f) if r['smooth_genus2']=='1'}

    def test_exact_162_integral_matrices_and_independent_zeta_mod9(self):
        self.assertEqual(len(self.coeffs),162)
        self.assertEqual(len(self.reference),162)
        results=curves()
        for code, row in results.items():
            c=trits(code,5)
            self.assertEqual(tuple(row['a'+str(i)] for i in range(5)),c)
            a,b=int(self.reference[code]['P1']),int(self.reference[code]['P2'])
            expected=[a%9,b%9,(3*a)%9,0]
            self.assertEqual([row['P'+str(i)+'_mod9'] for i in range(1,5)],expected)
            self.assertTrue(all(0<=row['F'+str(j)+str(i)]<=8 for i in range(4) for j in range(4)))

    def test_first_correction_is_necessary(self):
        incorrect=0
        for code,row in self.reference.items():
            _, cp=compute(trits(code,5),1)
            a,b=int(row['P1']),int(row['P2'])
            if [mod9(v) for v in cp[1:]]!=[a%9,b%9,(3*a)%9,0]:incorrect+=1
        self.assertEqual(incorrect,145)

    def test_next_omitted_term_zero_mod9_on_every_curve(self):
        # Empirical finite validation, not a bound for all future terms.
        for c in self.coeffs:
            m2,cp2=compute(c,2)
            m3,cp3=compute(c,3)
            self.assertEqual([mod9(v) for v in cp2],[mod9(v) for v in cp3])
            for j in range(4):
                for i in range(4):
                    self.assertGreaterEqual(v3((m3[j][i]-m2[j][i])*Q(SCALE[i],SCALE[j])),2)

    def test_one_more_omitted_term_on_sample_curves(self):
        # Includes different curve coefficient patterns; no infinite-tail claim.
        for code in (1, 2, 5, 10, 40, 91, 121, 161, 200, 242):
            c=trits(code,5)
            if not nonsingular(c):continue
            m3,cp3=compute(c,3)
            m4,cp4=compute(c,4)
            self.assertEqual([mod9(v) for v in cp3],[mod9(v) for v in cp4])
            for j in range(4):
                for i in range(4):
                    self.assertGreaterEqual(v3((m4[j][i]-m3[j][i])*Q(SCALE[i],SCALE[j])),2)

    def test_finite_host8_manifest_linkage(self):
        with (ROOT/'data'/'host8_seed_manifest.csv').open(newline='') as f:
            rows=list(csv.DictReader(f))
        self.assertEqual(len(rows),288)
        self.assertEqual(sum(nonsingular(trits(int(r['code243']),5)) for r in rows),194)

if __name__=='__main__':unittest.main()
