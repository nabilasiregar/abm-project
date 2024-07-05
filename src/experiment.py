import argparse
import toml
import numpy as np
import pandas as pd
from joblib import Parallel, delayed
import mesa
from model import EconomicModel
from agent import EconomicAgent, CopAgent


def run_simulation(params, max_steps, iteration, save_agent_data):
    print(f"Iteration {iteration + 1} with params: {params}")
    model = EconomicModel(**params)
    for i in range(max_steps):
        model.step()

    model_results = model.datacollector.get_model_vars_dataframe()
    model_results["iteration"] = iteration + 1
    for key, value in params.items():
        model_results[key] = value

    agent_results = None
    if save_agent_data:
        agent_results = model.datacollector.get_agent_vars_dataframe()
        agent_results["iteration"] = iteration + 1
    
    return model_results, agent_results

def generate_params(bounds, num_samples, vary_param, default_params):
    params_list = []
    if vary_param:
        is_integer = vary_param in ['num_econ_agents', 'initial_cops', 'width', 'height', 'election_frequency', 'sentence_length', 'interaction_memory']

        dtype = int if is_integer else float
        values = np.linspace(*bounds[vary_param], num=num_samples, dtype=dtype)

        for value in values:
            params = default_params.copy()
            params[vary_param] = value
            params_list.append(params)
    else:
        params_list = [default_params] * num_samples
    return params_list


def run(config_path, vary_param=None):
    config = toml.load(config_path)
    bounds = config['bounds']
    default_params = config['defaults']
    sim_settings = config['simulation']

    num_samples = sim_settings['num_samples']
    num_iterations = sim_settings['num_iterations']
    max_steps = sim_settings['max_steps']
    save_agent_data = sim_settings['save_agent_data']

    params_list = generate_params(bounds, num_samples, vary_param, default_params)

    results = Parallel(n_jobs=-1)(
        delayed(run_simulation)(params, max_steps, i, save_agent_data)
        for i in range(num_iterations)
        for params in params_list
    )

    model_results = [model_df for model_df, _ in results]
    model_results_df = pd.concat(model_results, ignore_index=True)
    model_results_df.to_csv('results/model_results.csv', index=False)
    
    if save_agent_data:
        agent_results = [agent_df for _, agent_df in results if agent_df is not None]
        agent_results_df = pd.concat(agent_results, ignore_index=True)
        agent_results_df.to_csv('results/agent_results.csv', index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run simulation:")
    parser.add_argument('-c', '--config', type=str, default='config.toml', help='Path to the configuration file.')
    parser.add_argument('-v', '--vary', type=str, help='Specify which parameter to vary. If not set, use default values for all parameters.')
    
    args = parser.parse_args()
    run(args.config, args.vary)
