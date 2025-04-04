import learning_model
import bloomfilter
import pandas as pd
import math
import tqdm
import random
from Crypto.Random import get_random_bytes

def bytes_to_mb(bytes_value):
    """Converts bytes to megabytes."""
    return bytes_value / (1024 * 1024)

class permuted_partitioned_lbf:
    # memory budget in bytes
    def __init__(self, memory_budget: int, classifier = None):
        self.memory_budget = memory_budget

        self.lm = learning_model.learning_model(classifier=classifier)
        
        m_learned = self.lm.memory_used()
        m_a = int((self.memory_budget - m_learned) / 2)
        m_b = m_a

        print(f"m_learned: {bytes_to_mb(m_learned)} MB, m_a: {bytes_to_mb(m_a)} MB, m_b: {bytes_to_mb(m_b)} MB")

        n_a = m_a * 8 # bytes to bits
        n_b = m_b * 8

        set_a = []
        set_b = []

        df = pd.read_csv("/tmp/malicious_urls_tiny.csv")
        print("Original df:", len(df))
        df = df[df['type'] != 0]
        print("Filtered df:", len(df))

        for url in tqdm.tqdm(df['url']):
            # if random.randint(1, 50) != 1:
            #     continue

            if self.lm.query(url):
                set_a.append(url)
            else:
                set_b.append(url)

        print("Cardinality of set a:", len(set_a))
        print("Cardinality of set b:", len(set_b))

        # optimal hash counts
        k_a = int(math.ceil(math.log(2) * (n_a / len(set_a))))
        k_b = int(math.ceil(math.log(2) * (n_b / len(set_b))))

        print(f"Info on backup bloom A: n={n_a}, k={k_a}")
        print(f"Info on backup bloom B: n={n_b}, k={k_b}")

        key_a = get_random_bytes(16)
        key_b = get_random_bytes(16)

        self.backup_a = bloomfilter.secure_bloomfilter(n_a, k_a, key_a)
        for element in set_a:
            self.backup_a.add(element)

        self.backup_b = bloomfilter.secure_bloomfilter(n_b, k_b, key_b)
        for element in set_b:
            self.backup_b.add(element)
    
    def query(self, element: any) -> bool:
        if self.lm.query(element):
            return self.backup_a.test(element)
        else:
            return self.backup_b.test(element)