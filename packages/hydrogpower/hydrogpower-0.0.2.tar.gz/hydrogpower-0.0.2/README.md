# HydroGPower

HydroGPower is a Python package that utilizes Gaussian Process (GP) models for predicting time-series hydro-resources.

## Installation

To use the HydroGPower tool, install the hydrogpower package:
```bash
pip install hydrogpower
```
## Example of usage

We created a ```dataset_example.xlsx``` file containing the time-series data at the script's path.
```bash
from hydrogpower import main

hydrogpower = main.HydroGPower(
    filename="dataset_example",
    horizont=5,
    M=2,
    seed=1234
)
hydrogpower.train_model()
hydrogpower.predict()