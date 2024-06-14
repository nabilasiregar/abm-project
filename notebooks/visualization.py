from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
import nest_asyncio
# nest_asyncio.apply()

model = EconomicModel(num_econ_agents=30, initial_cops=0, width=10, height = 10)
for i in range(500):
    # print('step ' + str(i))
    # print('cops: ' + str(len([x for x in model.schedule.agents if isinstance(x, CopAgent)])))
    model.step()

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
        else:
            portrayal = {
                "Shape": "circle",
                "Color": "black",
                "Filled": "true",
                "Layer": 0,
                "r": 0.5
            }

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
 
# Create the server
server = ModularServer(EconomicModel,
                       [grid],
                       "EconomicModel",
                       {"num_econ_agents": num_econ_agents, "initial_cops": initial_cops, "width": gridsize, "height": gridsize})

# Run the server
server.port = 8575
server.launch()