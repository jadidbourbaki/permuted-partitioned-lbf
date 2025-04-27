import unittest
import random
from utils import random_string
from Crypto.Random import get_random_bytes
from noy_cuckoo_filter import naor_oved_yogev_cuckoo_filter

# Note that these tests will often fail when the fingerprints collide, this is OK.

class test_naor_oved_yogev_cuckoo_filter(unittest.TestCase):
    def test_correctness(self):
        real_set = set()
        for i in range(1, 256):
            x = random_string(256)
            real_set.add(x)

        def test_with_random_n():
            key = get_random_bytes(16)  # AES-128 key
            n = random.randint(300, 5000)  # Make n large enough
            noy_filter = naor_oved_yogev_cuckoo_filter(n, key)

            noy_filter.construct(real_set)

            for s in real_set:
                self.assertTrue(noy_filter.query(s))

            false_positives = 0
            for i in range(1000):
                x = random_string(256)
                while x in real_set:
                    x = random_string(256)

                if noy_filter.query(x):
                    false_positives += 1

            fpr = false_positives / 1000
            print(f"For NOY Cuckoo Filter: m={noy_filter.m}, lambda={len(key)}, FPR={fpr}")

        for i in range(10):
            test_with_random_n()

if __name__ == '__main__':
    unittest.main()
