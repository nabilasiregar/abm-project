import mesa
from model import EconomicModel

model = EconomicModel(num_econ_agents=3, initial_cops=1, width=3, height = 3, election_frequency=20)
for i in range(30):
    model.step()

model_data = model.datacollector.get_model_vars_dataframe()
agent_data = model.datacollector.get_agent_vars_dataframe()

model_data.to_csv("../results/model_data.csv")
agent_data.to_csv("../results/agent_data.csv")
