# Adversary Resilient Learned Bloom Filters

To work with the model, go to the `model/` directory and run

```
make plot
```

To work with the permuted partitioned lbfs on the Malicious URLs dataset, go to `src/` and run

```
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
python3 test_learning_model.py # does pre-processing
python3 experiments.py
python3 plot.py
```

To run the cuckoo filter experiments (which use larger memory budgets), run

```
python3 cuckoo_experiments.py
python3 cuckoo_plot.py
```

The experiments will generate the following files in the `bin/` directory:
- `experiment_results.csv` and `plot_{classifier}.pdf` for the original experiments
- `cuckoo_experiment_results.csv` and `cuckoo_plot_{classifier}.pdf` for the cuckoo filter experiments