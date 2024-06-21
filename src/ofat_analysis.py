import numpy as np
import pandas as pd
from joblib import Parallel, delayed
import mesa
from model import EconomicModel, compute_gini
from agent import EconomicAgent, CopAgent

def run_simulation(params, max_steps, iteration):
    print(f"Iteration {iteration} with params: {params}")
    model = EconomicModel(
        num_econ_agents=params["num_econ_agents"],
        initial_cops=params["initial_cops"],
        width=params["width"],
        height=params["height"],
        election_frequency=params["election_frequency"],
        sentence_length=int(params["sentence_length"]),
        interaction_memory=int(params["interaction_memory"]),
        risk_aversion_std=params["risk_aversion_std"]
    )
    
    for _ in range(max_steps):
        model.step()
        
    results = model.datacollector.get_model_vars_dataframe()
    results["iteration"] = iteration
    results["sentence_length"] = params["sentence_length"]
    results["interaction_memory"] = params["interaction_memory"]
    results["risk_aversion_std"] = params["risk_aversion_std"]
    
    return results

def run():
    num_samples = 5
    num_iterations = 30
    max_steps = 1000
    
    bounds = {
        "sentence_length": (5, 25),
        "interaction_memory": (2, 22),
        "risk_aversion_std": (0.1, 0.5)
    }
    
    params_list = [
        {
            "num_econ_agents": 100, 
            "initial_cops": 2, 
            "width": 10, 
            "height": 10, 
            "election_frequency": 70, 
            "sentence_length": sl,
            "interaction_memory": im,
            "risk_aversion_std": ra
        }
        for sl in np.linspace(*bounds["sentence_length"], num=num_samples, dtype=int)
        for im in np.linspace(*bounds["interaction_memory"], num=num_samples, dtype=int)
        for ra in np.linspace(*bounds["risk_aversion_std"], num=num_samples)
    ]
    
    # -1 means use all available CPU
    results = Parallel(n_jobs=-1)(
        delayed(run_simulation)(params, max_steps, i)
        for i in range(num_iterations)
        for params in params_list
    )
    
    results_df = pd.concat(results, ignore_index=True)
    
    results_df.to_csv('results/ofat_results_30iterations_5samples.csv', index=False)
    print(results_df.head())

if __name__ == '__main__':
    run()

