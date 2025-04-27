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
    "mathtext.default": "regular",
})


def plot_cuckoo_results():
    df = pd.read_csv("bin/cuckoo_experiment_results.csv")
    classifiers = df['classifier'].unique()

    for clf in classifiers:
        subset = df[df['classifier'] == clf]
        mem_mbits = subset['memory_budget_bytes'] * 8 / (1024 * 1024)

        # Get min/max FPR to set sensible y-limits
        all_fprs = pd.concat([
            subset['fp_permuted_cuckoo_lbf'],
            subset['fp_noy_cuckoo']
        ])
        ymin = max(all_fprs.min() * 0.5, 1e-6)  # clamp for log scale
        ymax = 1.0

        # Create two subplots: one for FPR, one for skipped items
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 8), sharex=True)

        # Plot FPR on first subplot
        ax1.plot(mem_mbits, subset['fp_permuted_cuckoo_lbf'], 's-', color='#ff7f0e', label='Permuted Cuckoo LBF')
        ax1.plot(mem_mbits, subset['fp_noy_cuckoo'], '^-', color='#2ca02c', label='NOY Cuckoo CBF')

        ax1.set_ylabel('False Positive Rate')
        ax1.set_yscale('log')
        ax1.set_ylim(ymin, ymax)

        # Only show yticks that are within the y-limit
        log_ticks = np.array([1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6])
        log_ticks = log_ticks[(log_ticks >= ymin) & (log_ticks <= ymax)]
        ax1.set_yticks(log_ticks)
        ax1.set_yticklabels([f'$10^{{{int(np.log10(t))}}}$' for t in log_ticks])

        ax1.grid(True, which='major', linestyle=':', linewidth=0.6, alpha=0.7)
        ax1.legend(loc='best', frameon=False)

        # Plot skipped items on second subplot
        ax2.plot(mem_mbits, subset['noy_skipped_items'], '^-', color='#2ca02c', label='NOY Cuckoo CBF')
        ax2.set_xlabel('Memory Budget (Mbits)')
        ax2.set_ylabel('Skipped Items')
        ax2.grid(True, which='major', linestyle=':', linewidth=0.6, alpha=0.7)
        ax2.legend(loc='best', frameon=False)

        # Set x-axis limits and ticks
        plt.xlim(0, 64)  # 8MB * 8 bits = 64 Mbits
        plt.xticks([0, 16, 32, 48, 64])

        plt.tight_layout()
        plt.savefig(f"bin/cuckoo_plot_{clf}.pdf", bbox_inches='tight')
        plt.close()

if __name__ == '__main__':
    plot_cuckoo_results() 