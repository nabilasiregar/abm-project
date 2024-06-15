from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import Slider
from mesa.visualization.ModularVisualization import VisualizationElement

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
        # if the agent is a cop, color blue

        if agent.pos is not None:
            portrayal = {
                "Shape": "circle",
                "Color": "blue",
                "Filled": "true",
                "Layer": 0,
                "r": 0.5
            }
        else:
            portrayal = {
                "Shape": "circle",
                "Color": "rgba(0, 0, 0, 0.001)",
                "Filled": "true",
                "Layer": 0,
                "r": 0.5
            }
    return portrayal

# Create a grid visualization
grid = CanvasGrid(agent_portrayal, gridsize, gridsize, 500, 500)

# # Create a chart visualization
# chart = ChartModule([{"Label": "num_arrests_made",
#                       "Color": "Black"}],
#                     data_collector_name='datacollector')

# create a chart of the amount of cops
cop_chart = ChartModule([{"Label": "num_cops",
                      "Color": "Black"}],
                    data_collector_name='datacollector')

class LegendElement(VisualizationElement):
    package_includes = []
    local_includes = []

    def __init__(self):
        new_element = """
        var legendElement = document.createElement('div');
        legendElement.innerHTML = `
        <div id="legend" style="position:fixed; z-index:1000; right:10%; top:20%; background:white; padding:10px; border:1px solid black; border-radius:10px;">
            <ul style="list-style: none; padding: 0; margin: 0;">
                <li><span style="background-color: red; display: inline-block; width: 20px; height: 20px; border-radius: 50%;"></span> Committed Crime</li>
                <li><span style="background-color: green; display: inline-block; width: 20px; height: 20px; border-radius: 50%;"></span> Traded</li>
                <li><span style="background-color: black; display: inline-block; width: 20px; height: 20px; border-radius: 50%;"></span> Economic Agent</li>
                <li><span style="background-color: blue; display: inline-block; width: 20px; height: 20px; border-radius: 50%;"></span> Cop</li>
            </ul>
        </div>`;
        document.body.appendChild(legendElement);
        """
        self.js_code = new_element

legend = LegendElement()
 
# Create the server
server = ModularServer(EconomicModel,
                       [grid, cop_chart, legend],
                       "EconomicModel",
                       {"num_econ_agents": Slider("num_econ_agents", 30, 2, 100, 1), "initial_cops": Slider("num_cops", 2, 0, 10, 1), 
                        "interaction_memory": Slider("interaction_memory", 20, 1, 100, 1), 
                        "sentence_length": Slider("sentence_length", 15, 1, 50, 2), "width": gridsize, "height": gridsize})

# Run the server
server.port = 8545
server.launch()