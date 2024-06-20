import argparse
import pandas as pd
from mesa.datacollection import DataCollector
import numpy as np
from model import EconomicModel 

def run_varying_cops(cops_levels, fixed_sentence, num_steps, num_agents, width, height, election_frequency, interaction_memory, iterations):
    results = []
    for i in range(iterations):
        for cops in cops_levels:
            model = EconomicModel(num_econ_agents=num_agents, initial_cops=cops,
                                width=width, height=height, election_frequency=election_frequency,
                                sentence_length=fixed_sentence, interaction_memory=interaction_memory)
            for step in range(num_steps):
                model.step()
                step_data = model.datacollector.get_model_vars_dataframe().iloc[-1].to_dict()
                step_data.update({"Step": step, "iteration": i + 1, "param": "cops", "value": cops})
                results.append(step_data)
    return pd.DataFrame(results)

def run_varying_sentences(sentence_lengths, fixed_cops, num_steps, num_agents, width, height, election_frequency, interaction_memory, iterations):
    results = []
    for i in range(iterations):
        for length in sentence_lengths:
            model = EconomicModel(num_econ_agents=num_agents, initial_cops=fixed_cops,
                                width=width, height=height, election_frequency=election_frequency,
                                sentence_length=length, interaction_memory=interaction_memory)
            for step in range(num_steps):
                model.step()
                step_data = model.datacollector.get_model_vars_dataframe().iloc[-1].to_dict()
                step_data.update({"Step": step, "iteration": i + 1, "param": "sentence", "value": length})
                results.append(step_data)
    return pd.DataFrame(results)

def run_varying_election_frequencies(election_frequencies, fixed_cops, fixed_sentence, num_steps, num_agents, width, height, interaction_memory, iterations):
    results = []
    for i in range(iterations):
        for freq in election_frequencies:
            model = EconomicModel(num_econ_agents=num_agents, initial_cops=fixed_cops,
                                width=width, height=height, election_frequency=freq,
                                sentence_length=fixed_sentence, interaction_memory=interaction_memory)
            for step in range(num_steps):
                model.step()
                step_data = model.datacollector.get_model_vars_dataframe().iloc[-1].to_dict()
                step_data.update({"Step": step, "iteration": i + 1, "param": "elec_freq", "value": freq})
                results.append(step_data)
    return pd.DataFrame(results)

def run_varying_prosperity(prosperity_levels, fixed_cops, fixed_sentence, num_steps, num_agents, width, height, election_frequency, interaction_memory, iterations):
    results = []
    for i in range(iterations):
        for prosperity in prosperity_levels:
            model = EconomicModel(num_econ_agents=num_agents, initial_cops=fixed_cops,
                                width=width, height=height, election_frequency=election_frequency,
                                sentence_length=fixed_sentence, interaction_memory=interaction_memory)
            for step in range(num_steps):
                model.step()
                step_data = model.datacollector.get_model_vars_dataframe().iloc[-1].to_dict()
                step_data.update({"Step": step, "iteration": i + 1, "param": "prosperity", "value": prosperity})
                results.append(step_data)
    return pd.DataFrame(results)

def main():
    parser = argparse.ArgumentParser(description="Run ABM simulation")
    parser.add_argument("type", choices=['vary_cops', 'vary_sentence', 'vary_election_freq', 'vary_prosperity'], help="Type of simulation to run: 'vary_cops' or 'vary_sentence' or 'vary_election_freq' or 'vary_prosperity'")
    parser.add_argument("--steps", type=int, default=1000, help="Number of steps in the simulation")
    parser.add_argument("--num_agents", type=int, default=70, help="Number of economic agents")
    parser.add_argument("--width", type=int, default=10, help="Grid width")
    parser.add_argument("--height", type=int, default=10, help="Grid height")
    parser.add_argument("--election_frequency", type=int, default=70, help="Election frequency")
    parser.add_argument("--interaction_memory", type=int, default=5, help="Interaction memory length")
    parser.add_argument("--iterations", type=int, default=50, help="Number of iterations to run each simulation setup")
    args = parser.parse_args()

    if args.type == 'vary_cops':
        results = run_varying_cops([1, 3, 5, 7, 10], 15, args.steps, args.num_agents, args.width, args.height, args.election_frequency, args.interaction_memory, args.iterations)
    elif args.type == 'vary_sentence':
        results = run_varying_sentences([5, 10, 15, 20, 25], 2, args.steps, args.num_agents, args.width, args.height, args.election_frequency, args.interaction_memory, args.iterations)
    elif args.type == 'vary_election_freq':
        results = run_varying_election_frequencies([10, 20, 30, 40, 50, 60, 70], 2, 15, args.steps, args.num_agents, args.width, args.height, args.interaction_memory, args.iterations)
    elif args.type == 'vary_prosperity':
        results = run_varying_prosperity([0.1, 0.2, 0.3, 0.4, 0.5, 1], 2, 15, args.steps, args.num_agents, args.width, args.height, args.election_frequency, args.interaction_memory, args.iterations)
    results.to_csv(f"../results/{args.type}_results.csv", index=False)
    print(f"Saved simulation results to {args.type}_results.csv")

if __name__ == "__main__":
    main()
