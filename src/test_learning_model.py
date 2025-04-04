import unittest
from learning_model import *
from sklearn.ensemble import RandomForestClassifier

class test_learning_model(unittest.TestCase):
    def test_model(self):
        lm = learning_model(RandomForestClassifier(max_depth=6), clear_cache=True)
        url = "google.com"
        print(lm.query(url))

if __name__ == '__main__':
    unittest.main()