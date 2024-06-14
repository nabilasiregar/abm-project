import mesa
from model import EconomicModel

model = EconomicModel(num_econ_agents=50, initial_cops=1, width=30, height = 30, election_frequency=20)
for i in range(400):
    model.step()

data = model.datacollector.get_model_vars_dataframe()

print(data)
