#!/usr/bin/env python3
import matplotlib.pyplot as plt
import matplotlib as mpl
import csv
import os

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

def styled_plot(x, y1, y2, xlabel, ylabel, ylim, filename):
    plt.figure(figsize=(3.5, 2.5))
    plt.plot(x, y1, 'o-', color='black', label='Permuted-Partitioned LBF')
    plt.plot(x, y2, 'x--', color='gray', label='Secure CBF')

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xlim(0, 1)
    if ylim:
        plt.ylim(0, ylim)
    plt.grid(True, linestyle=':', linewidth=0.6, alpha=0.7)
    plt.legend(loc='best', frameon=False)
    plt.tight_layout()
    plt.savefig(filename, bbox_inches='tight')
    plt.close()

def _experiment_1(dataset, ymax):
    alpha_range = []
    downtown_bodega_y = []
    classical_y = []

    with open(f"bin/experiment_1_{dataset}.csv", "r") as f:
        r = csv.DictReader(f)
        for row in r:
            alpha_range.append(float(row['alpha']))
            downtown_bodega_y.append(float(row['downtown_fpr']))
            classical_y.append(float(row['classical_fpr']))

    styled_plot(
        alpha_range,
        downtown_bodega_y,
        classical_y,
        r'Value of $\alpha$',
        r'False Positive Rate',
        ymax,
        f"bin/experiment_1_{dataset}.pdf"
    )

def experiment_1():
    _experiment_1("google_transparency", 0.2)
    _experiment_1("malicious_urls", 0.05)
    _experiment_1("ember", 0.05)

def experiment_2():
    alphas = ["0p2", "0p3", "0p5", "1p0"]
    for alpha in alphas:
        q_n_range = []
        downtown_bodega_y = []
        classical_y = []

        with open(f"bin/experiment_2_google_transparency_alpha_{alpha}.csv", "r") as f:
            r = csv.DictReader(f)
            for row in r:
                q_n_range.append(float(row['q_n']))
                downtown_bodega_y.append(float(row['downtown_fpr']))
                classical_y.append(float(row['classical_fpr']))

        styled_plot(
            q_n_range,
            downtown_bodega_y,
            classical_y,
            r'Value of $Q_{N}$',
            r'False Positive Rate',
            0.2,
            f"bin/experiment_2_google_transparency_alpha_{alpha}.pdf"
        )

def experiment_3():
    alpha_range = []
    downtown_bodega_y = []
    classical_y = []

    with open("bin/experiment_3_google_transparency_alpha_0p2.csv", "r") as f:
        r = csv.DictReader(f)
        for row in r:
            alpha_range.append(float(row['p_weight']))
            downtown_bodega_y.append(float(row['downtown_fpr']))
            classical_y.append(float(row['classical_fpr']))

    styled_plot(
        alpha_range,
        downtown_bodega_y,
        classical_y,
        r'Value of $\frac{\alpha_{P}}{\alpha}$',
        r'False Positive Rate',
        0.15,
        "bin/experiment_3_google_transparency_alpha_0p2.pdf"
    )

if __name__ == '__main__':
    experiment_1()
    experiment_2()
    experiment_3()
