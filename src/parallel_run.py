import numpy as np
import pandas as pd
from joblib import Parallel, delayed
import mesa
from model import EconomicModel, compute_gini
from agent import EconomicAgent, CopAgent

def run_simulation(params, max_steps, iteration):
    print(f"Iteration {iteration + 1} with params: {params}")
    model = EconomicModel(
        num_econ_agents=params["num_econ_agents"],
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
    # model_results["election_frequency"] = params["election_frequency"]
    # model_results["sentence_length"] = params["sentence_length"]
    # model_results["interaction_memory"] = params["interaction_memory"]
    # model_results["risk_aversion_std"] = params["risk_aversion_std"]
    for key, value in params.items():
        model_results[key] = value
    
    # Collect agent-level data
    agent_results = model.datacollector.get_agent_vars_dataframe()
    agent_results["iteration"] = iteration + 1
    
    return model_results

def run():
    num_samples = 10
    num_iterations = 200
    max_steps = 500
    
    bounds = {
        "election_frequency": (10, 100),
        "sentence_length": (5, 90),
        "interaction_memory": (10, 100),
        "risk_aversion_std": (0.1, 0.99)
    }
    
    params_list = [
        {
            "num_econ_agents": 200, 
            "initial_cops": 8, 
            "width": 20, 
            "height": 20, 
            "election_frequency": 50, 
            "sentence_length": 20,
            "interaction_memory": 50,
            "risk_aversion_std": 0.3
        }
        # for elect in np.linspace(*bounds["election_frequency"], num=num_samples, dtype=int)
        # for sl in np.linspace(*bounds["sentence_length"], num=num_samples, dtype=int)
        # for im in np.linspace(*bounds["interaction_memory"], num=num_samples, dtype=int)
        # for ra in np.linspace(*bounds["risk_aversion_std"], num=num_samples)
    ]
    
    # -1 means use all available CPU
    results = Parallel(n_jobs=-1)(
        delayed(run_simulation)(params, max_steps, i)
        for i in range(num_iterations)
        for params in params_list
    )
    
    model_results = []
    # agent_results = []
    
    for model_df in results:
        model_results.append(model_df)
        # agent_results.append(agent_df)
    
    model_results_df = pd.concat(model_results, ignore_index=True)
    # agent_results_df = pd.concat(agent_results, ignore_index=True)
    
    model_results_df.to_csv('results/default_results_200iterations_200agents_8cops_20gridsize.csv', index=False)
    # agent_results_df.to_csv('results/ofat_agent_results.csv', index=False)

if __name__ == '__main__':
    run()
