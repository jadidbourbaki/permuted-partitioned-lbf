# Adversary Resilient Learned Bloom Filters

To work with the model, go to the `model/` directory and run

```
make plot
```

To work with the Downtown Bodega Implementation on the Malicious URLs dataset, go to `src/` and run

```
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
python3 test_learning_model.py # does pre-processing
python3 experiments.py
```