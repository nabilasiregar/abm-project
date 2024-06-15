from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
import nest_asyncio
# nest_asyncio.apply()

from model import EconomicModel
from agent import EconomicAgent, CopAgent

# model = EconomicModel(num_econ_agents=30, initial_cops=0, width=10, height = 10)
# for i in range(200):
#     print('step ' + str(i))
#     # print the amount of agents where has_committed_crime_this_turn is True
#     print('crimes: ' + str(len([x for x in model.schedule.agents if isinstance(x, EconomicAgent) and x.has_committed_crime_this_turn])))
#     print('trades: ' + str(len([x for x in model.schedule.agents if isinstance(x, EconomicAgent) and x.has_traded_this_turn])))
#     print('cops: ' + str(len([x for x in model.schedule.agents if isinstance(x, CopAgent)])))
#     model.step()

gridsize = 10
num_econ_agents = 30
initial_cops = 0

# Define a function to draw the agents
def agent_portrayal(agent):
    if isinstance(agent, EconomicAgent):
        # if has_committed_crime_this_turn is True, color red
        if agent.has_committed_crime_this_turn:
            portrayal = {
                "Shape": "circle",
                "Color": "red",
                "Filled": "true",
                "Layer": 0,
                "r": 0.5
            }
        # if has_traded_this_turn is True, color green
        elif agent.has_traded_this_turn:
            portrayal = {
                "Shape": "circle",
                "Color": "green",
                "Filled": "true",
                "Layer": 0,
                "r": 0.5
            }
        else:
            portrayal = {
                "Shape": "circle",
                "Color": "black",
                "Filled": "true",
                "Layer": 0,
                "r": 0.5
            }

    elif isinstance(agent, CopAgent):
        portrayal = {
            "Shape": "circle",
            "Color": "blue",
            "Filled": "true",
            "Layer": 0,
            "r": 0.5
        }
    return portrayal

# Create a grid visualization
grid = CanvasGrid(agent_portrayal, gridsize, gridsize, 500, 500)

chart = ChartModule([{"Label": "num_arrests_made",
                      "Color": "Black"}],
                    data_collector_name='datacollector')
 
# Create the server
server = ModularServer(EconomicModel,
                       [grid, chart],
                       "EconomicModel",
                       {"num_econ_agents": num_econ_agents, "initial_cops": initial_cops, "width": gridsize, "height": gridsize})

# Run the server
server.port = 8545
server.launch()