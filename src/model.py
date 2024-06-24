import mesa
from mesa.datacollection import DataCollector
import numpy as np
from agent import EconomicAgent, CopAgent

def compute_gini(model):
    agent_wealths = [agent.wealth for agent in model.schedule.agents if isinstance(agent, EconomicAgent)]
    x = sorted(agent_wealths)
    N = model.num_agents
    B = sum(xi * (N - i) for i, xi in enumerate(x)) / (N * sum(x))
    return 1 + (1 / N) - 2 * B

class EconomicModel(mesa.Model):
    def __init__(self, num_econ_agents, initial_cops=0, width=10, height=10, election_frequency = 20, sentence_length = 15, interaction_memory = 5, risk_aversion_std = 0.1, trading_skill_std = 0.1):
        super().__init__()
        self.num_agents = num_econ_agents
        self.num_cops = int(initial_cops)

        #create scheduler for movement and voting
        self.schedule = mesa.time.RandomActivation(self)
        #space
        self.grid = mesa.space.MultiGrid(width, height, torus = True)

        #parameters
        self.sentence_length = sentence_length
        self.prosperity = 0.05 #global prosperity if we want to model a dynamic economy, use as a multiplier for trade
        self.tax_rate = initial_cops*0.01
        self.election_frequency = election_frequency
        self.interaction_memory = interaction_memory
        self.risk_aversion_std = risk_aversion_std

        #vars
        self.votes = 0
        
        #counters for data collection
        self.num_crimes_committed = 0
        self.num_arrests_made = 0
        self.total_stolen = 0
        self.total_trade_income = 0
        self.steps = 0
        self.total_tax_paid = 0
        
        # create agents
        for i in range(self.num_agents):
            trade = np.random.normal(1, trading_skill_std)
            if trade < 0.1: 
                trade = 0.1
            a = EconomicAgent(i, self, trade)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.schedule.add(a)
            self.grid.place_agent(a, (x, y))
        for i in range(self.num_cops):
            c = CopAgent(i, self)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.schedule.add(c)
            self.grid.place_agent(c, (x, y))

        # add data collecor
        self.datacollector = mesa.DataCollector(
            model_reporters = {
                'Step': 'steps',
                'num_cops': 'num_cops',
                'num_crimes_committed': 'num_crimes_committed',
                'num_arrests_made': 'num_arrests_made',
                'tax_rate': 'tax_rate',
                'total_stolen': 'total_stolen',
                'total_trade_income': 'total_trade_income',
                'avg_wealth': lambda m: np.mean([agent.wealth for agent in m.schedule.agents if isinstance(agent, EconomicAgent)]),
                'total_wealth': lambda m: sum(agent.wealth for agent in m.schedule.agents if isinstance(agent, EconomicAgent)),
                'avg_crime_perception': lambda m: np.mean([sum(agent.q_crime_perception) / len(agent.q_crime_perception) if len(agent.q_crime_perception) > 0 else 0 for agent in m.schedule.agents if isinstance(agent, EconomicAgent)]),
                'vote_outcome': 'votes',
                'gini_coeff': compute_gini
            },
            agent_reporters = {'wealth': 'wealth', 'num_been_crimed': 'num_been_crimed',
                               'trading_skill': 'trading_skill', 'risk_aversion': 'risk_aversion',
                               'num_interactions': 'num_interactions', 'trading_skill': 'trading_skill',
                                'total_trading_gain': 'total_trading_gain',
                                'starting_wealth': 'starting_wealth', 'amount_arrested': 'amount_arrested',
                                'risk_aversion': 'risk_aversion', 'total_stealing_gain': 'total_stealing_gain'
                               
            })

    def step(self):
        self.steps += 1
        self.schedule.step()
        if (self.steps - 1) % self.election_frequency == 0 and self.steps != 1:
            if self.votes > 0:
                # print('The people have voted to increase taxes because votes were', self.votes, 'and the tax rate is', self.tax_rate, 'and the number of cops is', self.num_cops, 'and the number of agents is', self.num_agents)
                self.tax_rate += 0.01
            elif self.tax_rate > 0:
                # print('The people have voted to decrease taxes because votes were', self.votes, 'and the tax rate is', self.tax_rate, 'and the number of cops is', self.num_cops, 'and the number of agents is', self.num_agents)
                self.tax_rate -= 0.01
        
            # Adjusting the number of cops to voting results
            self.num_cops = int(self.tax_rate / 0.01)
            cops = [x for x in self.agents if isinstance(x, CopAgent)]

            if len(cops) < self.num_cops:
                c = CopAgent(self.next_id(), model = self)
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                self.schedule.add(c)
                self.grid.place_agent(c, (x, y))
            elif len(cops) > self.num_cops and len(cops) > 0: # ensure there is at least one cop to remove
                cops[0].pos = None
                cops[0].remove()
                self.schedule.remove(cops[0])
            # reset the votes
            self.votes = 0

        self.datacollector.collect(self)