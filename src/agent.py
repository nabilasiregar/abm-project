import mesa
import numpy as np
from statistics import mean
from collections import deque

class EconomicAgent(mesa.Agent):
    'wealth-maximising agent'
    def __init__(self, unique_id, model, trading_skill):
        super().__init__(unique_id, model)
        
        #agent's attributes:
        self.starting_wealth = np.random.uniform(1, 10) #mutable
        self.wealth = self.starting_wealth
        self.prosperity = 1 #fixed
        self.trading_skill = trading_skill

        self.criminality = 0 #mutable

        self.num_interactions = 0
        self.num_crimes_witnessed = 0 # how many crimes has this agent seen happen
        self.num_punishments_witnessed = 0 # how many crimes have been punished
        self.num_been_crimed = 0 # how many times has this agent been stolen from
        self.total_trading_gain = 0
        self.total_stealing_gain = 0
        self.crimes_committed_agent = 0
        self.amount_arrested = 0

        self.q_incomes = deque([0], maxlen=model.interaction_memory) # a queue of incomes from interactions 
        self.q_crime_perception = deque([], maxlen=model.interaction_memory) # a queue of crimes witnessed, 1 if punished, 0 if not
        self.q_interactions = deque([], maxlen=model.interaction_memory) # a queue of interactions, 0 if trade, 1 if theft

        self.has_traded_this_turn = False # only keep true for 1 step of the scheduler
        self.has_committed_crime_this_turn = False # only keep true for 1 step of the scheduler, allows cops to arrest
        self.is_arrested = False

        self.time_until_released = 0 # countdown of jail sentence

        risk_av = np.random.normal(1, self.model.risk_aversion_std)
        if risk_av <= 0:
            risk_av = 0.1
        self.risk_aversion = risk_av

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def choose_partner(self):
        # TODO here we can do the logic of choosing a trading partner
        # Possibly also add logic here that calculates the EU of trade/steal for each cellmate and returns best candidate
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            cellmates = [x for x in cellmates if isinstance(x, EconomicAgent)]
            cellmates = [x for x in cellmates if not x.is_arrested and not x is self]
            try:
                other = self.random.choice(cellmates)

            except: other = None 
             # TODO here we can have some wealth prefernces if we want
            return other
        
    def make_trade(self, other):
            if other is not None: #redundant?
                trade_value = (other.wealth + self.wealth)* self.model.prosperity
                # TODO add some scaling that will make the poorer person benefit less
                # print('own and other wealth before trade: ' ,self.wealth, other.wealth)
                other.wealth += trade_value * other.trading_skill
                self.wealth += trade_value * self.trading_skill

                self.total_trading_gain += trade_value * self.trading_skill
                other.total_trading_gain += trade_value * other.trading_skill
                # print('own and other wealth after: ' ,self.wealth, other.wealth)
                
                self.num_interactions +=1
                other.num_interactions +=1
                self.has_traded_this_turn = True
                other.has_traded_this_turn = True
                other.q_interactions.append(0)

                self.q_incomes.append(trade_value)
                if len(self.q_incomes) > self.model.interaction_memory:
                    self.q_incomes.pop(0)   
                # remove the first element of the queue if it's too long
                if len(other.q_interactions) > other.model.interaction_memory:
                    other.q_interactions.pop(0)
                self.model.total_trade_income += 2*trade_value
    def steal(self, other):
        theft_value = other.wealth/2
        self.wealth += theft_value
        other.wealth -= theft_value
        self.total_stealing_gain += theft_value
        self.crimes_committed_agent += 1

        self.q_incomes.append(theft_value)
        if len(self.q_incomes) > self.model.interaction_memory:
            self.q_incomes.pop(0)   

        self.model.total_stolen += theft_value
        self.model.num_crimes_committed += 1

        self.has_committed_crime_this_turn = True  
        other.num_been_crimed += 1     
        self.num_interactions +=1
        other.num_interactions +=1
        other.q_interactions.append(1)
        # remove the first element of the queue if it's too long
        if len(other.q_interactions) > other.model.interaction_memory:
            other.q_interactions.pop(0)
        self.model.num_crimes_committed += 1
        self.model.total_stolen += theft_value

    def decide_action(self, other):
        '''Decide whether to steal or trade'''
        # TODO calculations of expected value to determine action
        if len(self.q_crime_perception) > 0:
            # use self.q_crime_perception to calculate arrest chance
            arrest_chance = sum(self.q_crime_perception)/len(self.q_crime_perception)
        else: arrest_chance = 0

        alpha = -1.2 # shape parameter for the pareto distribution
        sp = 1 # scale parameter for the pareto distribution
        transformed_sentence_length = sp / (self.model.sentence_length ** (1 / alpha))
        expected_punishment_pain = self.wealth + self.risk_aversion * (transformed_sentence_length * mean(self.q_incomes))

        theft_EU = other.wealth/2 - expected_punishment_pain*arrest_chance
        trade_EU = (other.wealth + self.wealth)* self.model.prosperity * self.trading_skill

        # print('agents wealth is:' ,self.wealth, ' expected pun pain is ', expected_punishment_pain, 'which results in theft EUof ', theft_EU)

        # print('expected trade utility', trade_EU)
        # print('expected theft EU', theft_EU)

        if trade_EU >= theft_EU:
            return 'trade'
        else:
            return 'steal'
        
    def vote(self):
        #calculate value of the threat of being robbed using the interactions queue
        # if that value is greater than current tax rate then vote to increase
        if len(self.q_interactions) >0:
            crime_rate = sum(self.q_interactions)/self.model.interaction_memory
            # print('interaction queue', self.q_interactions)
            # print('crime rate', crime_rate)
        else: crime_rate = 0
        theft_threat = crime_rate* self.wealth* self.risk_aversion* 0.5 #TODO this is hard coded at .5     
        tax_burden = self.wealth*self.model.tax_rate
        if theft_threat > tax_burden:
            return 1
        else:
            return -1
        
    def pay_tax(self):
        #wealth tax, could use income tax instead? then the EU calculations are a bit harder
        self.wealth -= self.wealth * self.model.tax_rate
        self.model.total_tax_paid += self.wealth * self.model.tax_rate

    def check_for_crimes(self):
        neighbors = self.model.grid.get_neighbors(
            self.pos,
            moore=True,
            include_center=True,
            radius=1  # Vision radius
        )
        for neighbor in neighbors:
            if isinstance(neighbor, EconomicAgent) and neighbor.has_committed_crime_this_turn:
                self.q_crime_perception.append(0)
                self.num_crimes_witnessed += 1

    def step(self):
        self.has_traded_this_turn = False
        self.has_committed_crime_this_turn = False
        #if they're in jail they don't do anything
        if self.is_arrested:
            self.time_until_released -=1
            if self.time_until_released == 0:
                self.is_arrested = False
        else:
            self.move()
            other = self.choose_partner()
            if other is not None:
                if self.decide_action(other=other) == 'steal':
                    self.steal(other)
                else: 
                    self.make_trade(other)
            self.check_for_crimes()
        self.pay_tax() # or maybe you should only pay tax when you make a trade? idk
        
        if (self.model.steps)%self.model.election_frequency == 0:
            vote = self.vote() #returns +/- 1
            self.model.votes += vote

class CopAgent(mesa.Agent):
    'crime-fighting agent'
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=True)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        
    def look_for_crimes(self):
        neighbors = self.model.grid.get_neighbors(
            self.pos,
            moore=True,
            include_center=True,
            radius=1  # Vision radius
        )
        for neighbor in neighbors:
            if isinstance(neighbor, EconomicAgent) and neighbor.has_committed_crime_this_turn:
                self.arrest(neighbor)

    def arrest(self, criminal_agent):
        criminal_agent.wealth = 1 #TODO
        criminal_agent.is_arrested = True
        criminal_agent.time_until_released = self.model.sentence_length 
        criminal_agent.amount_arrested += 1
        #not sure if this is gonna work right, the idea is that once they're arrested and in jail, ppl are no longer observing the crime being committed
        criminal_agent.has_committed_crime_this_turn = False
        self.model.num_arrests_made += 1

        # make the arrest announcement
        neighbors = self.model.grid.get_neighbors(
            self.pos,
            moore=True,
            include_center=True,
            radius=1  # Vision radius
        )
        for neighbor in neighbors:
            if isinstance(neighbor, EconomicAgent):
                neighbor.q_crime_perception.append(1)
                # remove the first element of the queue if it's too long
                if len(neighbor.q_crime_perception) > neighbor.model.interaction_memory:
                    neighbor.q_crime_perception.pop(0)

    def step(self):
        self.move()
        self.look_for_crimes()
        