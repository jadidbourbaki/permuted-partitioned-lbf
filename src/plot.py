import pandas as pd
import matplotlib.pyplot as plt

def plot_from_csv():
    df = pd.read_csv("bin/experiment_results.csv")
    classifiers = df['classifier'].unique()

    for clf in classifiers:
        subset = df[df['classifier'] == clf]
        mem_mb = subset['memory_budget_bytes'] / (1024 * 1024)

        plt.plot(mem_mb, subset['fpr_classical'], 'kx--', label='Secure Classical Bloom Filter')
        plt.plot(mem_mb, subset['fpr_bodega'], 'ko-', label=f'Downtown Bodega Filter ({clf})')

        plt.xlabel('Memory Budget (MBits)')
        plt.ylabel('False Positive Rate')
        plt.yscale('log')
        plt.title(f'FPR vs Memory for {clf}')
        plt.legend(loc='best')
        plt.savefig(f"bin/plot_{clf}.pdf")
        plt.clf()

if __name__ == '__main__':
    plot_from_csv()
