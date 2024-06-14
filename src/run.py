import mesa
from model import EconomicModel

model = EconomicModel(num_econ_agents=5, initial_cops=1, width=3, height = 3, election_frequency=20)
for i in range(400):
    model.step()

data = model.datacollector.get_model_vars_dataframe()

print(data)
