import math
import mmh3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import random
import string

class bloomfilter:
    def __init__(self, n : int, k : int):
        self.num_bits = n
        self.num_hashes = k
        self.bit_array = [0] * self.num_bits
    
    def construct(self, input_set: list[bytes | str]) -> None:
        for element in input_set:
            self._add(element)
        
    def _add(self, element : bytes | str) -> None:
        for i in range(self.num_hashes):
            hash_val = mmh3.hash(element, i) % self.num_bits
            self.bit_array[hash_val] = 1
        
    def query(self, element: bytes | str) -> bool:
        for i in range(self.num_hashes):
            hash_val = mmh3.hash(element, i) % self.num_bits
            if self.bit_array[hash_val] == 0:
                return False
        return True
    
class secure_bloomfilter:
    def __init__(self, n: int, k: int, key: any):
        self.key = key
        self.bloomfilter = bloomfilter(n, k)

    def _apply_prp(self, item: any) -> bytes:
        """
        Apply a pseudorandom permutation (PRP) to the input
        
        In this implementation, we use AES as our PRP
        """
        # Convert item to bytes if it isn't already
        if not isinstance(item, bytes):
            item_bytes = str(item).encode('utf-8')
        else:
            item_bytes = item
        
        # Pad to AES block size
        padded = pad(item_bytes, AES.block_size)
        
        # Use AES in ECB mode as a simple PRP
        # ECB is likely sufficient since we are using it as a 
        # pseudorandom permutation rather than for confidentiality
        cipher = AES.new(self.key, AES.MODE_ECB)
        return cipher.encrypt(padded)
    
    def construct(self, input_set: set[bytes | str]) -> None:
        permuted_set = [self._apply_prp(element) for element in input_set]
        self.bloomfilter.construct(permuted_set)

    def query(self, element: bytes | str) -> bool:
        permuted = self._apply_prp(element)
        return self.bloomfilter.query(permuted)