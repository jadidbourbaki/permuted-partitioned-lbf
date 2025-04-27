from permuted_partitioned_lbf import *
from bloomfilter import *
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

def run_all_experiments():
    df = pd.read_csv(get_global_dataset())
    encode_df = df[df['type'] == 1]
    test_df = df[df['type'] == 0]

    classifiers = {
        "GaussianNB": GaussianNB(),
        "LinearSVC": LinearSVC()
    }

    memory_budgets = [52424, 104856, 262144, 524288]  # in bytes
    security_parameter = 16  # 128 bits
    results = []

    for clf_name, clf in classifiers.items():
        for mem in memory_budgets:
            print(f"Running {clf_name} with memory {mem} bytes")

            pplbf = permuted_partitioned_lbf(mem - 2 * security_parameter, clf)

            n = (mem - security_parameter) * 8
            set_size = len(encode_df)
            k = int(math.ceil(math.log(2) * (n / set_size)))
            sbf = secure_bloomfilter(n, k, get_random_bytes(16))
            sbf.construct([url for url in encode_df['url']])

            counter = 0
            fp_permuted_partitioned_lbf = 0
            fp_classical = 0
            fp_learning = 0

            for url in tqdm.tqdm(test_df['url']):
                if random.randint(1, 10) != 1:
                    continue
                counter += 1
                if pplbf.query(url): fp_permuted_partitioned_lbf += 1
                if pplbf.lm.query(url): fp_learning += 1
                if sbf.query(url): fp_classical += 1

            model_size_bytes = pplbf.lm.memory_used()
            results.append({
                "classifier": clf_name,
                "memory_budget_bytes": mem,
                "model_size_bytes": model_size_bytes,
                "entries_tested": counter,
                "fpr_classical": fp_classical / counter,
                "fpr_learning": fp_learning / counter,
                "fp_permuted_partitioned_lbf": fp_permuted_partitioned_lbf / counter
            })

    # Save to CSV
    with open("bin/experiment_results.csv", "w", newline='') as csvfile:
        fieldnames = ["classifier", "memory_budget_bytes", "model_size_bytes",
                      "entries_tested", "fpr_classical", "fpr_learning", 
                      "fp_permuted_partitioned_lbf"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)

    print("Saved experiment results to bin/experiment_results.csv")

if __name__ == '__main__':
    run_all_experiments()