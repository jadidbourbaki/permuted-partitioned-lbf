import unittest
from bodega import *
from bloomfilter import *
import prp
import math
import random
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import LinearSVC

class test_bodega(unittest.TestCase):
    def test_bodega(self):
        df = pd.read_csv("/tmp/malicious_urls_tiny.csv")
        encode_df = df[df['type'] == 1]
        test_df = df[df['type'] == 0]

        security_parameter = 16 # 128 bits
        memory_budget = int(0.5 * 0.125 * 1024 * 1024)
        lm = downtown_bodega(memory_budget - 2 * security_parameter, LinearSVC())

        set_size = len(encode_df)
        n = int(memory_budget - security_parameter) * 8
        k = int(math.ceil(math.log(2) * (n / set_size)))

        print(f"For secure classical bloom filter: n={n}, k={k}")

        sbf = secure_bloomfilter(n, k, prp.generate_key())

        print("Adding to secure classical bloom filter")
        for url in tqdm.tqdm(encode_df['url']):
            sbf.add(url)

        counter = 0
        fp_bodega = 0
        fp_classical = 0
        fp_learning = 0

        for url in tqdm.tqdm(test_df['url']):
            # Some random sampling to speed this up
            if random.randint(1, 10) != 1:
                continue

            counter += 1

            if lm.test(url):
                fp_bodega += 1

            if lm.lm.test(url):
                fp_learning += 1

            if sbf.test(url):
                fp_classical += 1

        print("Entries evaluated:", counter)
        print("Memory budget, in bits:", memory_budget * 8)
        print("Memory taken by learning model:", learning_model.model_size(lm.lm.model) * 8)
        print("FPR Classical:", fp_classical / counter)
        print("FPR Learning Model", fp_learning / counter)
        print("FPR Downtown Bodega", fp_bodega / counter)

if __name__ == '__main__':
    unittest.main()