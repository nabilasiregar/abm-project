# Agent-Based Modelling
This repository contains the source code for an agent-based model simulation using the Mesa framework. The simulation includes various aspects such as economic and cop agent interactions, crime dynamics, and policy effects through taxation and policing.

## Installation
1. Clone the repository
2. Install the required Python packages:
`pip install -r requirements.txt`

## Directory structure
```bash
   ├── README.md

   ├── **notebooks**

   │ └── analysis.ipynb

   ├── requirements.txt

   ├── **results**

   ├── **src**

   │ ├── agent.py

   │ ├── batch_run.py

   │ ├── extra_analysis.py

   │ ├── model.py

   │ ├── parallel_run.py

   │ ├── plot.py

   │ └── run.py

   └── **static**

   ├── **extra_graphs**

   ├── **icons**

   └── **plot**
```
- **/notebooks**: Contains Jupyter notebooks for analysis and to generate plots in our report 
- **/results**: Stores simulation output results, which include various metrics and states captured during the simulation runs. 
- **agent.py**: Defines the `EconomicAgent` and `CopAgent` classes. 
- **model.py**: Contains the `EconomicModel` class which setups the simulation environment and agents. 
- **run.py**: Utilizes Mesa's server to visualize simulation runs. It is the entry point for running the visualization interface. 
- **parallel_run.py**: Script for executing local sensitivity analysis of the model parameters. 
- **plot.py**: Provides functions used for plotting within the notebooks. 
- **batch_run.py, extra_analysis.py**: Additional scripts for batch processing and analysis of model data. 
- **/static**: Contains static resources used in the project, such as icons used in the simulation's GUI and plots generated from analysis notebooks.

## Running the simulation
To visualize the agent-based model via a web interface, run the following command from the root of the repository: : `mesa runserver src`

## Sensitivity Analysis
TODO

## Notebooks
To generate figures in our report, run all `analysis.ipynb`	

### Authors
Adrian Ruesink, Kenia Lopez, Milo Vollmuller, Nabila Siregar, Tad Price