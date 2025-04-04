import unittest
import random
import bloomfilter
import prp

class test_secure_bloom_filter(unittest.TestCase):
    def test_correctness(self):
        real_set = set()
        for i in range(1, 256):
            x = bloomfilter.random_string(256)
            real_set.add(x)

        def test_with_random_n_k():
            key = prp.generate_key()
            n = random.randint(10, 5000)
            k = random.randint(1, 20)
            sbf = bloomfilter.secure_bloomfilter(n, k, key)
            
            for s in real_set:
                sbf.add(s)

            for s in real_set:
                self.assertTrue(sbf.test(s))

            false_positives = 0
            for i in range(1000):
                x = bloomfilter.random_string(256)
                while x in real_set:
                    x = bloomfilter.random_string(256)

                if sbf.test(x):
                    false_positives += 1
            
            fpr = false_positives / 1000
            print(f"For secure bloom filter: n={sbf.bloomfilter.num_bits}, k={sbf.bloomfilter.num_hashes}, lambda={len(key)}, FPR={fpr}")

        for i in range(10):
            test_with_random_n_k()

if __name__ == '__main__':
    unittest.main()
                    


            