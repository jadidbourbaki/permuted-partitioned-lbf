import matplotlib.pyplot as plt

# make sure you have a bin directory

# global data
def experiment_1():
    memory_budget = [52424, 104856, 262144, 524288]
    memory_taken_by_learning_model = [15544, 15544, 15544, 15544]
    fpr_bodega_gaussian_nb = [0.5997436494989513, 0.2868984572875892, 0.034633054541170924, 0.0007058823529411765]
    fpr_secure_classical = [0.5716616173386158, 0.32385447847110294, 0.057603958063376134, 0.0029411764705882353]

    memory_budget_mb = [x / (1024 * 1024) for x in memory_budget]
    plt.plot(memory_budget_mb, fpr_secure_classical, 'kx--', label='Secure Classical Bloom Filter')
    plt.plot(memory_budget_mb, fpr_bodega_gaussian_nb, 'ko-', label='Downtown Bodega Filter (Gaussian NB)')
    plt.xlabel('Memory Budget (Mbits)')
    plt.ylabel('False Positive Rate')
    plt.yscale("log")
    plt.legend(loc='best')
    plt.savefig(f"bin/impl_experiment_1.pdf")
    plt.clf()

def experiment_2():
    memory_budget = [52424, 104856, 262144, 524288]
    memory_taken_by_learning_model = [11352, 11352, 11352, 11352]
    fpr_bodega_linear_svc = [0.5343332552144364, 0.24944786702313146, 0.02102067032582039, 0.0005864414731409805]
    fpr_secure_classical = [0.5658542301382704, 0.3162850168545856, 0.05990891042858811, 0.0038705137227304713]

    memory_budget_mb = [x / (1024 * 1024) for x in memory_budget]
    plt.plot(memory_budget_mb, fpr_secure_classical, 'kx--', label='Secure Classical Bloom Filter')
    plt.plot(memory_budget_mb, fpr_bodega_linear_svc, 'ko-', label='Downtown Bodega Filter (Linear SVC)')
    plt.xlabel('Memory Budget (Mbits)')
    plt.ylabel('False Positive Rate')
    plt.yscale("log")
    plt.legend(loc='best')
    plt.savefig(f"bin/impl_experiment_2.pdf")
    plt.clf()

if __name__ == '__main__':
    experiment_1()
    experiment_2()