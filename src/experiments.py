from permuted_partitioned_lbf import *
from bloomfilter import *
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import GaussianNB
from Crypto.Random import get_random_bytes
import pandas as pd
import math
import random
import tqdm
import matplotlib.pyplot as plt

def run_experiment(classifier, memory_budget_bytes, security_parameter=16):
    df = pd.read_csv("/tmp/malicious_urls_tiny.csv")
    encode_df = df[df['type'] == 1]
    test_df = df[df['type'] == 0]

    lm = permuted_partitioned_lbf(memory_budget_bytes - 2 * security_parameter, classifier)
    set_size = len(encode_df)

    n = int(memory_budget_bytes - security_parameter) * 8  # bits
    k = int(math.ceil(math.log(2) * (n / set_size)))

    sbf = secure_bloomfilter(n, k, get_random_bytes(16))
    sbf.construct([url for url in encode_df['url']])

    counter = 0
    fp_bodega = 0
    fp_classical = 0
    fp_learning = 0

    for url in tqdm.tqdm(test_df['url'], desc="Evaluating on test set"):
        if random.randint(1, 10) != 1:
            continue

        counter += 1
        if lm.query(url): fp_bodega += 1
        if lm.lm.query(url): fp_learning += 1
        if sbf.query(url): fp_classical += 1

    fpr_bodega = fp_bodega / counter
    fpr_learning = fp_learning / counter
    fpr_classical = fp_classical / counter
    model_bits = learning_model.model_size(lm.lm.model) * 8

    return {
        "memory_budget": memory_budget_bytes,
        "model_bits": model_bits,
        "fpr_bodega": fpr_bodega,
        "fpr_learning": fpr_learning,
        "fpr_classical": fpr_classical
    }

def run_all_experiments():
    memory_budgets = [52424, 104856, 262144, 524288]
    
    experiments = [
        ("Gaussian NB", GaussianNB(), "impl_experiment_1.pdf"),
        ("Linear SVC", LinearSVC(), "impl_experiment_2.pdf"),
    ]
    
    for label, classifier, filename in experiments:
        fprs_bodega = []
        fprs_classical = []
        model_sizes = []
        memory_mb = []

        for mem in memory_budgets:
            print(f"\nRunning: {label} with memory {mem} bytes")
            result = run_experiment(classifier, mem)
            fprs_bodega.append(result["fpr_bodega"])
            fprs_classical.append(result["fpr_classical"])
            model_sizes.append(result["model_bits"])
            memory_mb.append(mem / (1024 * 1024))  # bytes to MB

        plt.plot(memory_mb, fprs_classical, 'kx--', label='Secure CBF')
        plt.plot(memory_mb, fprs_bodega, 'ko-', label=f'Permuted-Partitioned LBF ({label})')
        plt.xlabel('Memory Budget (Mbits)')
        plt.ylabel('False Positive Rate')
        plt.yscale("log")
        plt.legend(loc='best')
        plt.savefig(f"bin/{filename}")
        plt.clf()

if __name__ == '__main__':
    run_all_experiments()
