import mesa
from agent import EconomicAgent, CopAgent
from mesa.datacollection import DataCollector

class EconomicModel(mesa.Model):
    def __init__(self, num_econ_agents, initial_cops=0, width=10, height=10, election_frequency = 20, sentence_length = 15, interaction_memory = 5):
        super().__init__()
        self.num_agents = num_econ_agents
        self.num_cops = initial_cops

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

        #vars
        self.votes = 0
        
        #counters, this will have to be replaced with a datacollector
        self.num_crimes_committed_turn = 0
        self.num_arrests_made = 0
        self.total_stolen = 0
        self.total_trade_income = 0
        self.trades_made_turn = 0
        self.arrested_agents = 0
        self.steps = 0
        
        # create agents
        for i in range(self.num_agents):
            a = EconomicAgent(i, self)
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


        #For Data collection
        self.datacollector = DataCollector(
            {"No. crimes committed this turn": lambda m: self.num_crimes_committed_turn,
            "Total trades made this turn": lambda m: self.trades_made_turn,
            "Arrested agents": lambda m: self.arrested_agents}
        )

        self.running = True
        self.datacollector.collect(self)

    def collect_data(self):

        self.num_crimes_committed_turn = 0
        self.trades_made_turn = 0
        self.arrested_agents = 0



        for agent in self.agents:

            if isinstance(agent, EconomicAgent):
                if agent.has_committed_crime_this_turn:
                    self.num_crimes_committed_turn += 1
                if agent.has_traded_this_turn:
                    self.trades_made_turn += 1
                if agent.is_arrested:
                    self.arrested_agents += 1
                


    def step(self):


        self.steps += 1
        self.schedule.step()
        if (self.steps-1)%self.election_frequency == 0 and self.steps != 1:
            if self.votes >0:
                print('The people have voted to increase taxes because votes were', self.votes, 'and the tax rate is', self.tax_rate, 'and the number of cops is', self.num_cops, 'and the number of agents is', self.num_agents)
                self.tax_rate += 0.01
            else:
                print('The people have voted to decrease taxes because votes were', self.votes, 'and the tax rate is', self.tax_rate, 'and the number of cops is', self.num_cops, 'and the number of agents is', self.num_agents)
                self.tax_rate -= 0.01
        
            # Adjusting the number of cops to voting results  
            self.num_cops = self.tax_rate/0.01
            cops = [x for x in self.agents if isinstance(x, CopAgent)]

            if len(cops) < self.num_cops:
                c = CopAgent(self.next_id(), model = self)
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                self.schedule.add(c)        
                self.grid.place_agent(c, (x, y))
            elif len(cops) > 0:
                cops[0].remove()
                self.schedule.remove(cops[0])
            # reset the votes
            self.votes = 0


        self.collect_data()

        
        self.datacollector.collect(self)