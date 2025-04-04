#!/usr/bin/env python3
import matplotlib.pyplot as plt
import csv

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

    plt.plot(alpha_range, downtown_bodega_y, 'ko-', label='Downtown Bodega Filter')
    plt.plot(alpha_range, classical_y, 'kx--', label='Classical Secure Bloom Filter')
    plt.xlabel(r'Value of $\alpha$')
    plt.ylabel(r'False Positive Rate')
    plt.legend(loc='best')
    plt.xlim(0, 1)
    plt.ylim(0, ymax)
    plt.savefig(f"bin/experiment_1_{dataset}.pdf")
    plt.clf()


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

        plt.plot(q_n_range, downtown_bodega_y, 'ko-', label='Downtown Bodega Filter')
        plt.plot(q_n_range, classical_y, 'kx--', label='Classical Secure Bloom Filter')
        plt.xlabel(r'Value of $Q_{N}$')
        plt.ylabel(r'False Positive Rate')
        plt.legend(loc='best')
        plt.xlim(0, 1)
        plt.ylim(0, 0.2)
        plt.savefig(f"bin/experiment_2_google_transparency_alpha_{alpha}.pdf")
        plt.clf()

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

    plt.plot(alpha_range, downtown_bodega_y, 'ko-', label='Downtown Bodega Filter')
    plt.plot(alpha_range, classical_y, 'kx--', label='Classical Secure Bloom Filter')
    plt.xlabel(r'Value of $\frac{\alpha_{P}}{\alpha}$')
    plt.ylabel(r'False Positive Rate')
    plt.legend(loc='best')
    plt.xlim(0, 1)
    plt.ylim(0, 0.15)
    plt.savefig("bin/experiment_3_google_transparency_alpha_0p2.pdf")
    plt.clf()

if __name__ == '__main__':
    experiment_1()
    experiment_2()
    experiment_3()