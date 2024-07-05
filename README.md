# Agent-Based Modelling
This repository contains the source code for an agent-based model simulation using the Mesa framework. The simulation includes various aspects such as economic and cop agent interactions, crime dynamics, and policy effects through taxation and policing.
<p align="center">
  <img src="static/simulation.gif" alt="Simulation" width="300" height="300"/>
</p>


## Installation
1. Clone the repository
2. Install the required Python packages:
```bash
   pip install -r requirements.txt
```

## Demo
To visualize the agent-based model via a web interface, run the following command from the root of the repository: 
```bash
   mesa runserver src
```

## Running the experiment
From the project directory run
```bash
  python src/experiment.py
```
it will run the experiment with the default parameter settings as specified in the configuration file (config.toml) in parallel.

If you want to run the experiment while varying 1 parameter at a time (e.g. vary trading skill but keep other params constant), run
```bash
   python src/experiment.py --vary 'trading_skill_std'
```

## Notebooks
To generate figures in our report, run all `analysis.ipynb`	and `global_sensitivity_analysis.ipynb`

## Directory structure
```bash
   ├── README.md
   ├── notebooks
   │   ├── analysis.ipynb
   │   └── global_sensitivity_analysis.ipynb
   ├── requirements.txt
   ├── results
   ├── src
   │   ├── agent.py
   │   ├── experiment.py
   │   ├── extra_analysis.py
   │   ├── model.py
   │   ├── parallel_run_global.py
   │   ├── plot.py
   │   └── run.py
   └── static
      ├── extra_graphs
      ├── icons
      └── plot
```
- **/notebooks**: Contains Jupyter notebooks for analysis and to generate plots in our report 
- **/results**: Stores simulation output results, currently ignored from being committed due to large file size
- **agent.py**: Defines the `EconomicAgent` and `CopAgent` classes. 
- **model.py**: Contains the `EconomicModel` class which setups the simulation environment and agents. 
- **run.py**: Utilizes Mesa's server to visualize simulation runs. It is the entry point for running the visualization interface. 
- **experiment.py**: Script for executing local sensitivity analysis and experiments of the model parameters. 
- **parallel_run_global.py**: Script for executing global sensitivity analysis. 
- **plot.py**: Provides functions used for plotting within the notebooks. 
- **extra_analysis.py**: Additional scripts for experiments and analysis of model data. 
- **/static**: Contains static resources used in the project, such as icons used in the simulation's GUI and plots generated from analysis notebooks.

### Authors
Adrian Ruesink, Kenia Lopez, Milo Vollmuller, Nabila Siregar, Tad Price