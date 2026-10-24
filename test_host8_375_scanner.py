"""Scanner acceptance tests on synthetic sectors; no physical 300 GB disk needed."""
from pathlib import Path
import hashlib
import struct
import tempfile
import unittest
from scan_host8_375_sectors import (
    build_codebook, sample_offsets, scan, SECTOR_BYTES, SAMPLES_PER_GRID
)

class ScannerTests(unittest.TestCase):
    def test_default_geometry(self):
        self.assertEqual(SECTOR_BYTES, 800_000_000)
        self.assertEqual(SAMPLES_PER_GRID,96)
        self.assertEqual(sample_offsets(110592,96)[-1],110591)
        self.assertEqual(sample_offsets(100000000,96)[-1],99999999)
        self.assertEqual(len(set(sample_offsets(100000000,96))),96)

    def test_codebook(self):
        c=build_codebook()
        self.assertEqual(len(c),243)
        self.assertEqual(sum(v is not None for v in c.values()),162)
        self.assertEqual(sum(c[i] == 2 for i in c if c[i] is not None),120)
        self.assertEqual(sum(c[i] == 1 for i in c if c[i] is not None),24)
        self.assertEqual(sum(c[i] == 0 for i in c if c[i] is not None),18)

    def test_synthetic_sector_modes(self):
        with tempfile.TemporaryDirectory() as p:
            d=Path(p)
            for sec in (10,11):
                payload=b''.join(struct.pack('<Q',sec*103+i*179) for i in range(16))
                (d/f'sector-{sec:03d}.rooms').write_bytes(payload)
            r,s,m=scan(d,(10,11),128,16,16,8,False,False)
            self.assertEqual(len(r),4)
            self.assertEqual(s[-1]['rooms'],32)
            self.assertEqual(s[-1]['smooth'],sum(s[-1]['p_rank_'+str(i)] for i in range(3)))
            self.assertEqual(m['full_volume_bytes_hashed'],0)
            r,s,m=scan(d,(10,11),128,16,16,8,True,False)
            self.assertEqual(m['full_volume_bytes_hashed'],256)
            for row in r:
                src=(d/f"sector-{row['sector']}.rooms").read_bytes()
                self.assertEqual(row['full_sector_sha256'],hashlib.sha256(src).hexdigest())
            # Fail-closed on truncated / missing sector.
            (d/'sector-010.rooms').write_bytes(b'bad')
            with self.assertRaises(ValueError):
                scan(d,(10,11),128,16,16,8,False,False)
            (d/'sector-010.rooms').unlink()
            with self.assertRaises(FileNotFoundError):
                scan(d,(10,11),128,16,16,8,False,False)

if __name__=='__main__':
    unittest.main()
