# FutuRaM Recovery Model

This repository contains:

- `doc/`: model documentation
- `src/`: model source code
- `data_folder/`: mock data for testing the model

An explanation of the goals and general structure of the model can be found here: https://doi.org/10.5281/zenodo.23342083


## Using the model

Create a folder under `data_folder/` with an `input_data/` subfolder containing three files:

- `inputs.csv`: inflows per resource
- `composition.csv`: resource compositions
- `TCs.csv`: transfer coefficients

Set `data_folder` in `run_model.py` and execute the file; results are written to the dataset's `output_data/` folder. The optimized implementation is intended for systems without feedback loops, while the linear-algebra implementation can represent feedback loops when the system has a solution. Input formats are defined in the [user guide](doc/User%20guide.md).
