import pandas as pd
import math
import tqdm
import random
from Crypto.Random import get_random_bytes
from utils import bytes_to_mb
from learning_model import *
from noy_cuckoo_filter import naor_oved_yogev_cuckoo_filter

class permuted_cuckoo_lbf:
    # memory budget in bytes
    def __init__(self, memory_budget: int, classifier = None, intelligent_split: bool = False):
        self.memory_budget = memory_budget

        self.lm = learning_model(classifier=classifier)

        set_a = []
        set_b = []

        df = pd.read_csv(get_global_dataset())
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

        m_learned = self.lm.memory_used()
        if intelligent_split:
            m_total = self.memory_budget - m_learned
            total_items = len(set_a) + len(set_b)
            m_a = int(m_total * (len(set_a) / total_items))
            m_b = m_total - m_a
        else:
            m_a = int((self.memory_budget - m_learned) / 2)
            m_b = m_a

        print(f"m_learned: {bytes_to_mb(m_learned)} MB, m_a: {bytes_to_mb(m_a)} MB, m_b: {bytes_to_mb(m_b)} MB")

        # Calculate number of items for each filter based on memory budget
        # Each item takes fingerprint_size bytes (default 16) in the table
        # The table size is 1.1 * n to provide headroom for insertions
        fingerprint_size = 1  # bytes per fingerprint
        n_a = int(m_a / fingerprint_size)
        n_b = int(m_b / fingerprint_size)

        print(f"Info on backup cuckoo filter A: n={n_a}, m={n_a * fingerprint_size}")
        print(f"Info on backup cuckoo filter B: n={n_b}, m={n_b * fingerprint_size}")

        assert n_a > 0 and n_b > 0

        key_a = get_random_bytes(16)
        key_b = get_random_bytes(16)

        self.backup_a = naor_oved_yogev_cuckoo_filter(n=n_a, key=key_a, fingerprint_size=fingerprint_size)
        self.backup_a.construct(set_a)

        self.backup_b = naor_oved_yogev_cuckoo_filter(n=n_b, key=key_b, fingerprint_size=fingerprint_size)
        self.backup_b.construct(set_b)
    
    def query(self, element: any) -> bool:
        if self.lm.query(element):
            return self.backup_a.query(element)
        else:
            return self.backup_b.query(element)