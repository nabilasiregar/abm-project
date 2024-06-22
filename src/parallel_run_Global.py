import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from SALib.sample import saltelli
from SALib.analyze import sobol
from model import EconomicModel, compute_gini
from agent import EconomicAgent, CopAgent

def run_simulation(params, max_steps, iteration):
    print(f"Iteration {iteration + 1} with params: {params}")
    model = EconomicModel(
        num_econ_agents=int(params["num_econ_agents"]),
        initial_cops=int(params["initial_cops"]),
        width=int(params["width"]),
        height=int(params["height"]),
        election_frequency=params["election_frequency"],
        sentence_length=int(params["sentence_length"]),
        interaction_memory=int(params["interaction_memory"]),
        risk_aversion_std=params["risk_aversion_std"]
    )
    
    for _ in range(max_steps):
        model.step()

    # Collect model-level data
    model_results = model.datacollector.get_model_vars_dataframe()
    model_results["iteration"] = iteration + 1
    model_results["num_econ_agents"] = params["num_econ_agents"]
    model_results["initial_cops"] = params["initial_cops"]
    model_results["election_frequency"] = params["election_frequency"]
    model_results["sentence_length"] = params["sentence_length"]
    model_results["interaction_memory"] = params["interaction_memory"]
    model_results["risk_aversion_std"] = params["risk_aversion_std"]
    
    return model_results

def run():
    max_steps = 1000
    num_samples = 16  # Number of samples for Saltelli (must be a power of 2 for better convergence)
    num_iterations = 20  # Number of iterations for each sample
    
    # Define the problem for SALib
    problem = {
        'num_vars': 3,
        'names': ['sentence_length', 'interaction_memory', 'risk_aversion_std'],
        'bounds': [[5, 25], [10, 100], [0.1, 0.99]]
    }
    
    # Generate samples using Saltelli's method for the defined problem
    param_values = saltelli.sample(problem, num_samples)

    # Generate a list of dictionaries, each representing a unique set of parameters for running the economicModel
    params_list = [
        {
            "num_econ_agents": 150, 
            "initial_cops": 2, 
            "width": 10, 
            "height": 10, 
            "election_frequency": 70, #values drawn from the sample generated from saltelli.sample
            "sentence_length": param_values[i, 0],
            "interaction_memory": param_values[i, 1],
            "risk_aversion_std": param_values[i, 2]
        }
        for i in range(len(param_values))
    ]
    
    # Generate a list of (params, iteration) tuples.
    # This will be used to run the model for each set of parameters for the specified number of iterations
    param_iteration_list = [(params, iteration) for iteration in range(num_iterations) for params in params_list]   ## example: [ (params_list[0], 0), (params_list[1], 0),(params_list[0], 1), (params_list[1], 1),(params_list[0], 2), (params_list[1], 2)]
    
    # Run simulations in parallel using joblib
    results = Parallel(n_jobs=-1)(
        delayed(run_simulation)(params, max_steps, iteration)
        for params, iteration in param_iteration_list
    )
    
    model_results = []
    
    for model_df in results:
        model_results.append(model_df)
    
    model_results_df = pd.concat(model_results, ignore_index=True)
    
    # Save results to CSV
    model_results_df.to_csv('results/global_sensitivity_analysis_model_results.csv', index=False)
    
    # Perform Sobol sensitivity analysis
    # Y = model_results_df['total_wealth'].values  # Adjust 'total_wealth' to your output variable of interest
    # Si = sobol.analyze(problem, Y, calc_second_order=False)
    
    # # Display results
    # print(model_results_df.head())
    # print(Si)

if __name__ == '__main__':
    run()


