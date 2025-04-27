import math
import mmh3
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

class naor_oved_yogev_cuckoo_filter:
    def __init__(self, n: int, key: bytes, fingerprint_size: int = 16, max_relocations: int = 5000):
        self.n = n  # Expected number of items
        self.m = int(2 * n)  # Table size, could adjust constant factor
        self.T1 = [None] * self.m
        self.T2 = [None] * self.m
        self.key = key  # AES key
        self.fingerprint_size = fingerprint_size  # in bytes
        self.max_relocations = max_relocations  # to avoid infinite loops
        self.skipped_items = 0

    def _prf(self, item: any) -> bytes:
        if not isinstance(item, bytes):
            item_bytes = str(item).encode('utf-8')
        else:
            item_bytes = item
        padded = pad(item_bytes, AES.block_size)
        cipher = AES.new(self.key, AES.MODE_ECB)
        prf_output = cipher.encrypt(padded)
        return prf_output[:self.fingerprint_size]

    def _h1(self, item: any) -> int:
        return mmh3.hash(str(item), 0) % self.m

    def _h2(self, item: any) -> int:
        return mmh3.hash(str(item), 1) % self.m
    
    def construct(self, input_set: list[bytes | str]) -> None:
        for element in input_set:
            self._insert(element)
        print(f"Skipped {self.skipped_items} items")

    def _insert(self, element: bytes | str) -> None:
        fingerprint = self._prf(element)
        i1 = self._h1(element)
        i2 = self._h2(element)

        # Try to insert into T1
        if self.T1[i1] is None:
            self.T1[i1] = fingerprint
            return

        # Try to insert into T2
        if self.T2[i2] is None:
            self.T2[i2] = fingerprint
            return

        # Need to evict
        idx = random.choice([i1, i2])
        table_choice = random.choice([1, 2])

        for _ in range(self.max_relocations):
            if table_choice == 1:
                evicted_fingerprint = self.T1[idx]
                self.T1[idx] = fingerprint
                idx = self._h2(evicted_fingerprint)
                table_choice = 2
            else:
                evicted_fingerprint = self.T2[idx]
                self.T2[idx] = fingerprint
                idx = self._h1(evicted_fingerprint)
                table_choice = 1

            if table_choice == 1 and self.T1[idx] is None:
                self.T1[idx] = evicted_fingerprint
                return
            if table_choice == 2 and self.T2[idx] is None:
                self.T2[idx] = evicted_fingerprint
                return

        # If we reach here, we couldn't insert the item
        # Instead of raising an error, we'll just add it to the skipped item count
        self.skipped_items += 1
        return

    def query(self, element: bytes | str) -> bool:
        fingerprint = self._prf(element)
        i1 = self._h1(element)
        i2 = self._h2(element)

        return (self.T1[i1] == fingerprint) or (self.T2[i2] == fingerprint)
