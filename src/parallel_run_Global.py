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
    
    # Collect model-level data across all steps
    model_results = model.datacollector.get_model_vars_dataframe().copy()
    model_results["iteration"] = iteration + 1
    model_results["num_econ_agents"] = params["num_econ_agents"]
    model_results["initial_cops"] = params["initial_cops"]
    model_results["election_frequency"] = params["election_frequency"]
    model_results["sentence_length"] = params["sentence_length"]
    model_results["interaction_memory"] = params["interaction_memory"]
    model_results["risk_aversion_std"] = params["risk_aversion_std"]
    
    return model_results

def run():
    max_steps = 500
    num_samples = 16
    num_iterations = 20
    
    problem = {
        'num_vars': 3,
        'names': ['sentence_length', 'interaction_memory', 'risk_aversion_std'],
        'bounds': [[5, 25], [10, 100], [0.1, 0.99]]
    }
    
    param_values = saltelli.sample(problem, num_samples)
    
    params_list = [
        {
            "num_econ_agents": 150,
            "initial_cops": 2,
            "width": 10,
            "height": 10,
            "election_frequency": 70,
            "sentence_length": param_values[i, 0],
            "interaction_memory": param_values[i, 1],
            "risk_aversion_std": param_values[i, 2]
        }
        for i in range(len(param_values))
    ]
    
    param_iteration_list = [(params, iteration) for iteration in range(num_iterations) for params in params_list]
    
    results = Parallel(n_jobs=-1)(
        delayed(run_simulation)(params, max_steps, iteration)
        for params, iteration in param_iteration_list
    )
    
    model_results = []
    
    for model_df in results:
        model_results.append(model_df)
    
    model_results_df = pd.concat(model_results, ignore_index=True)

    # Task 1: Last step
    # Take the last step from each iteration and group them by unique parameter sets
    last_step_df = model_results_df[model_results_df['Step'] == max_steps - 1]
    last_step_avg_df = last_step_df.groupby(['num_econ_agents', 'initial_cops', 'election_frequency', 
                                              'sentence_length', 'interaction_memory', 'risk_aversion_std']).mean().reset_index()

    last_step_avg_df.to_csv('results/global_sensitivity_analysis_model_results_last_step.csv', index=False)

    # Task 2: Across steps
    # Take all steps from each iteration and group them by unique parameter sets and Step
    across_steps_df = model_results_df.groupby(['Step', 'num_econ_agents', 'initial_cops', 'election_frequency', 
                                                'sentence_length', 'interaction_memory', 'risk_aversion_std']).mean().reset_index()
    across_steps_df.to_csv('results/global_sensitivity_analysis_model_results_all_steps.csv', index=False)

    return across_steps_df, last_step_avg_df

if __name__ == '__main__':
    run()