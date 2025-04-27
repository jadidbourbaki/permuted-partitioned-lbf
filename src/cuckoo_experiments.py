from permuted_cuckoo_filter import *
from noy_cuckoo_filter import *
from learning_model import *
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import GaussianNB
from Crypto.Random import get_random_bytes
import pandas as pd
import math
import random
import tqdm
import matplotlib.pyplot as plt
import csv

def run_cuckoo_experiments():
    df = pd.read_csv(get_global_dataset())
    encode_df = df[df['type'] == 1]
    test_df = df[df['type'] == 0]

    classifiers = {
        "GaussianNB": GaussianNB(),
        "LinearSVC": LinearSVC()
    }

    # Larger memory budgets for cuckoo filters (in bytes)
    memory_budgets = [4194304, 8388608, 12582912, 16777216]  # 4MB to 16MB
    security_parameter = 16  # 128 bits
    results = []

    for clf_name, clf in classifiers.items():
        for mem in memory_budgets:
            print(f"Running {clf_name} with memory {mem} bytes")

            pclbf = permuted_cuckoo_lbf(mem - 2 * security_parameter, clf)

            # Create NOY cuckoo filter with 4-byte fingerprints
            fingerprint_size = 8  # 4 byte fingerprints
            table_size_factor = 1.1  # NOY filter uses 1.1 * n for table size
            noy_n = int(mem / (fingerprint_size * table_size_factor))
            noy_filter = naor_oved_yogev_cuckoo_filter(n=noy_n, key=get_random_bytes(16), fingerprint_size=fingerprint_size)
            noy_filter.construct([url for url in encode_df['url']])

            counter = 0
            fp_permuted_cuckoo_lbf = 0
            fp_noy_cuckoo = 0
            fp_learning = 0

            for url in tqdm.tqdm(test_df['url']):
                if random.randint(1, 10) != 1:
                    continue
                counter += 1
                if pclbf.query(url): fp_permuted_cuckoo_lbf += 1
                if noy_filter.query(url): fp_noy_cuckoo += 1
                if pclbf.lm.query(url): fp_learning += 1

            model_size_bytes = pclbf.lm.memory_used()
            results.append({
                "classifier": clf_name,
                "memory_budget_bytes": mem,
                "model_size_bytes": model_size_bytes,
                "entries_tested": counter,
                "fpr_learning": fp_learning / counter,
                "fp_permuted_cuckoo_lbf": fp_permuted_cuckoo_lbf / counter,
                "fp_noy_cuckoo": fp_noy_cuckoo / counter,
                "noy_skipped_items": noy_filter.skipped_items
            })

    # Save to CSV
    with open("bin/cuckoo_experiment_results.csv", "w", newline='') as csvfile:
        fieldnames = ["classifier", "memory_budget_bytes", "model_size_bytes",
                      "entries_tested", "fpr_learning", 
                      "fp_permuted_cuckoo_lbf", "fp_noy_cuckoo",
                      "noy_skipped_items"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)

    print("Saved cuckoo experiment results to bin/cuckoo_experiment_results.csv")

if __name__ == '__main__':
    run_cuckoo_experiments() 