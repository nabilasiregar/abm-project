import numpy as np
import pandas as pd
import mesa

from model import EconomicModel
from agent import EconomicAgent, CopAgent

params = {"num_econ_agents": 50, "initial_cops": 2, "width": 10, "height": 10, "election_frequency": range(30, 90, 4), "sentence_length": 15,
          "interaction_memory": range(2, 50, 4), "risk_aversion_std": 0.1}

results = mesa.batch_run(
    EconomicModel,
    parameters=params,
    iterations=10,
    max_steps=1000,
    data_collection_period=1,
    display_progress=True
)

results_df = pd.DataFrame(results)
results_df.head()
# save the csv to the results folder
# results_df.to_csv('results/results.csv')