"""Independent tests for the Host8 ternary finite-field zeta experiment."""
from collections import Counter
from pathlib import Path
import unittest
import host8_ternary_weil as f

class FiniteTernaryWeilTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fields=[f.Field(n,p) for n,p in enumerate(f.MODULI,start=1)]

    def test_field_tables(self):
        for F in self.fields:
            n=F.q
            for x in range(n):
                for y in range(n):
                    self.assertEqual(F.mul[x][y],F.mul[y][x])
                    if n<=9:
                        for z in range(n):
                            self.assertEqual(F.mul[F.mul[x][y]][z],F.mul[x][F.mul[y][z]])
                if x:
                    self.assertEqual(F.power(x,n-1),1)
            self.assertEqual(len({F.mul[y][y] for y in range(1,n)}),(n-1)//2)

    def test_bruteforce_points_in_all_extension_fields(self):
        # Enumerate every (x,y) directly: independent of the quadratic
        # character point-counting method in the experiment.
        for code in range(243):
            a=f.trits(code,5)
            if not f.nonsingular(a):
                continue
            for F in self.fields:
                count=1  # unique point at infinity
                for x in range(F.q):
                    v=F.power(x,5)
                    for k,c in enumerate(a):
                        if c:
                            term=F.power(x,k)
                            if c==2:term=F.add[term][term]
                            v=F.add[v][term]
                    for y in range(F.q):
                        count+=(F.mul[y][y]==v)
                self.assertEqual(count,F.points(a),(code,F.q))

    def test_every_quintic_and_exact_RH_condition(self):
        valid=0
        zetas=set()
        for code in range(243):
            result=f.zeta(code,self.fields)
            if result is not None:
                valid+=1
                N,A,B,passes=result
                self.assertTrue(passes)
                self.assertEqual(N[0],4+A)
                self.assertEqual(N[1],10-A*A+2*B)
                zetas.add((A,B))
        self.assertEqual(valid,162)
        self.assertEqual(len(zetas),32)

    def test_host8_manifest_and_results(self):
        path=Path(__file__).parent/'data'/'host8_seed_manifest.csv'
        records=f.read_manifest(path)
        self.assertEqual(len(records),288)
        self.assertEqual([(s,code) for s,_,_,code in records[::96]],
                         [('000',4),('187',121),('374',156)])
        self.assertEqual(records[2],('000',2,2328,91))
        counts=Counter(sec for sec,_,_,code in records
                       if f.zeta(code,self.fields) is not None)
        self.assertEqual(dict(counts),{'000':66,'187':67,'374':61})

if __name__=='__main__':
    unittest.main(verbosity=2)
