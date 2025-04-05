import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

mpl.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Times", "Computer Modern Roman"],
    "font.size": 10,
    "axes.labelsize": 10,
    "axes.titlesize": 11,
    "legend.fontsize": 9,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "lines.linewidth": 1.3,
    "lines.markersize": 5.5,
    "figure.dpi": 300,
    "pdf.fonttype": 42,
})

def plot_from_csv():
    df = pd.read_csv("bin/experiment_results.csv")
    classifiers = df['classifier'].unique()

    for clf in classifiers:
        subset = df[df['classifier'] == clf]
        mem_mbits = subset['memory_budget_bytes'] * 8 / (1024 * 1024)

        # Get min/max FPR to set sensible y-limits
        all_fprs = pd.concat([
            subset['fpr_classical'],
            subset['fp_permuted_partitioned_lbf']
        ])
        ymin = max(all_fprs.min() * 0.5, 1e-6)  # clamp for log scale
        # ymax = min(all_fprs.max() * 1.2, 1.0)
        ymax = 1.0

        plt.figure(figsize=(3.5, 2.5))
        plt.plot(mem_mbits, subset['fpr_classical'], 'x--', color='black', label='Secure CBF')
        plt.plot(mem_mbits, subset['fp_permuted_partitioned_lbf'], 'o-', color='black', label=f'Permuted-Partitioned LBF')

        plt.xlabel('Memory Budget (Mbits)')
        plt.ylabel('False Positive Rate')
        plt.yscale('log')
        plt.ylim(ymin, ymax)

        plt.xlim(0, 4.1)
        plt.xticks([0, 1, 2, 3, 4])

        # Only show yticks that are within the y-limit
        log_ticks = np.array([1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6])
        log_ticks = log_ticks[(log_ticks >= ymin) & (log_ticks <= ymax)]
        plt.yticks(log_ticks, [f'$10^{{{int(np.log10(t))}}}$' for t in log_ticks])

        plt.grid(True, which='major', linestyle=':', linewidth=0.6, alpha=0.7)
        plt.legend(loc='best', frameon=False)
        plt.tight_layout()
        plt.savefig(f"bin/plot_{clf}.pdf", bbox_inches='tight')
        plt.close()

if __name__ == '__main__':
    plot_from_csv()
