import mesa
from model import EconomicModel
import seaborn as sns
from matplotlib import pyplot as plt

model = EconomicModel(num_econ_agents=10, initial_cops=0, width=10, height = 10, election_frequency=20, interaction_memory=100)
for i in range(300):
    model.step()

# agent_wealth = model.datacollector.get_agent_vars_dataframe()
# agent_list = [3, 4, 5, 6, 7]

# # Get the wealth of multiple agents over time
# multiple_agents_wealth = agent_wealth[
#     agent_wealth.index.get_level_values("AgentID").isin(agent_list)
# ]
# print(multiple_agents_wealth)
# # Plot the wealth of multiple agents over time
# g = sns.lineplot(data=multiple_agents_wealth, x="Step", y="wealth", hue="AgentID")
# g.set(title="Wealth of agents 3, 14 and 25 over time");

# plt.show()

# # Step 1: Extract the data from datacollector
# model_data = model.datacollector.get_model_vars_dataframe()
# agent_data = model.datacollector.get_agent_vars_dataframe()

# print(agent_data['wealth'])

# # Step 2: Calculate mean agent's wealth and mean num_been_crimed
# mean_wealth = agent_data['wealth'].mean()
# mean_num_been_crimed = agent_data['num_been_crimed'].mean()

# # Step 3: Plotting
# fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(10, 8))

# # Plot mean agent's wealth
# ax1.plot(model_data.index, mean_wealth, label='Mean Agent Wealth', color='blue')
# ax1.set_xlabel('Steps')
# ax1.set_ylabel('Mean Agent Wealth')
# ax1.legend()

# Plot mean num_been_crimed
# ax2.plot(model_data.index, model_data['num_been_crimed'], label='Mean Num Been Crimed', color='green')
# ax2.set_xlabel('Steps')
# ax2.set_ylabel('Mean Num Been Crimed')
# ax2.legend()

# plt.tight_layout()
# plt.show()
