import math
import mmh3
import prp
import random
import string

class bloomfilter:
    def __init__(self, n, k):
        self.num_bits = n
        self.num_hashes = k
        self.bit_array = [0] * self.num_bits
        
    def add(self, element):
        for i in range(self.num_hashes):
            hash_val = mmh3.hash(element, i) % self.num_bits
            self.bit_array[hash_val] = 1
        
    def test(self, element):
        for i in range(self.num_hashes):
            hash_val = mmh3.hash(element, i) % self.num_bits
            if self.bit_array[hash_val] == 0:
                return False
        return True
    
class secure_bloomfilter:
    def __init__(self, n, k, key):
        self.key = key
        self.bloomfilter = bloomfilter(n, k)

    def add(self, element):
        self.bloomfilter.add(prp.encrypt(element, self.key))

    def test(self, element):
        return self.bloomfilter.test(prp.encrypt(element, self.key))

# NOT cryptographically random
def random_string(max_len):
    def generate_random_string(length):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for i in range(length))

    x_len = random.randint(1, max_len)
    x = generate_random_string(x_len)
    return x