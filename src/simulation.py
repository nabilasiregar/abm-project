import argparse
import pandas as pd
from mesa.datacollection import DataCollector
import numpy as np
from model import EconomicModel 

def run_varying_cops(cops_levels, fixed_sentence, num_steps, num_agents, width, height, election_frequency, interaction_memory):
    results = []
    for cops in cops_levels:
        model = EconomicModel(num_econ_agents=num_agents, initial_cops=cops,
                              width=width, height=height, election_frequency=election_frequency,
                              sentence_length=fixed_sentence, interaction_memory=interaction_memory)
        for step in range(num_steps):
            model.step()
            step_data = model.datacollector.get_model_vars_dataframe().iloc[-1].to_dict()
            step_data.update({"Step": step, "param": "cops", "value": cops})
            results.append(step_data)
    return pd.DataFrame(results)

def run_varying_sentences(sentence_lengths, fixed_cops, num_steps, num_agents, width, height, election_frequency, interaction_memory):
    results = []
    for length in sentence_lengths:
        model = EconomicModel(num_econ_agents=num_agents, initial_cops=fixed_cops,
                              width=width, height=height, election_frequency=election_frequency,
                              sentence_length=length, interaction_memory=interaction_memory)
        for step in range(num_steps):
            model.step()
            step_data = model.datacollector.get_model_vars_dataframe().iloc[-1].to_dict()
            step_data.update({"Step": step, "param": "sentence length", "value": length})
            results.append(step_data)
    return pd.DataFrame(results)

def run_varying_election_frequencies(election_frequencies, fixed_cops, fixed_sentence, num_steps, num_agents, width, height, interaction_memory):
    results = []
    for freq in election_frequencies:
        model = EconomicModel(num_econ_agents=num_agents, initial_cops=fixed_cops,
                              width=width, height=height, election_frequency=freq,
                              sentence_length=fixed_sentence, interaction_memory=interaction_memory)
        for step in range(num_steps):
            model.step()
            step_data = model.datacollector.get_model_vars_dataframe().iloc[-1].to_dict()
            step_data.update({"Step": step, "param": "election frequency", "value": freq})
            results.append(step_data)
    return pd.DataFrame(results)


def run_varying_prosperity(prosperity_levels, fixed_cops, fixed_sentence, num_steps, num_agents, width, height, election_frequency, interaction_memory):
    results = []
    for prosperity in prosperity_levels:
        model = EconomicModel(num_econ_agents=num_agents, initial_cops=fixed_cops,
                              width=width, height=height, election_frequency=election_frequency,
                              sentence_length=fixed_sentence, interaction_memory=interaction_memory)
        for step in range(num_steps):
            model.step()
            step_data = model.datacollector.get_model_vars_dataframe().iloc[-1].to_dict()
            step_data.update({"Step": step, "param": "prosperity", "value": prosperity})
            results.append(step_data)
    return pd.DataFrame(results)

def main():
    parser = argparse.ArgumentParser(description="Run ABM simulation")
    parser.add_argument("type", choices=['vary_cops', 'vary_sentence'], help="Type of simulation to run: 'vary_cops' or 'vary_sentence'")
    parser.add_argument("--steps", type=int, default=200, help="Number of steps in the simulation")
    parser.add_argument("--num_agents", type=int, default=50, help="Number of economic agents")
    parser.add_argument("--width", type=int, default=10, help="Grid width")
    parser.add_argument("--height", type=int, default=10, help="Grid height")
    parser.add_argument("--election_frequency", type=int, default=20, help="Election frequency")
    parser.add_argument("--interaction_memory", type=int, default=5, help="Interaction memory length")
    args = parser.parse_args()

    if args.type == 'vary_cops':
        results = run_varying_cops([1, 3, 5, 7, 10], 15, args.steps, args.num_agents, args.width, args.height, args.election_frequency, args.interaction_memory)
    elif args.type == 'vary_sentence':
        results = run_varying_sentences([5, 10, 15, 20, 25], 5, args.steps, args.num_agents, args.width, args.height, args.election_frequency, args.interaction_memory)
    elif args.type == 'vary_election_freq':
        results = run_varying_election_frequencies([10, 20, 30, 40, 50], 5, 15, args.steps, args.num_agents, args.width, args.height, args.interaction_memory)
    elif args.type == 'vary_prosperity':
        results = run_varying_prosperity([0.01, 0.05, 1, 1.5, 2, 2.5, 3], 5, 15, args.steps, args.num_agents, args.width, args.height, args.election_frequency, args.interaction_memory)
    results.to_csv(f"../results/{args.type}_results.csv", index=False)
    print(f"Saved simulation results to {args.type}_results.csv")

if __name__ == "__main__":
    main()
