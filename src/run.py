import mesa
from model import EconomicModel

model = EconomicModel(num_econ_agents=3, initial_cops=1, width=3, height = 3, election_frequency=20, tax_rate=0.01)
for i in range(30):
    model.step()
