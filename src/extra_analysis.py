import numpy as np
import pandas as pd
import mesa
from model import EconomicModel, compute_gini
from agent import EconomicAgent, CopAgent
import matplotlib.pyplot as plt

def trading_skill_tests():
    #Seeing if trading skill impacts total amount made by trading and if lower trading skill results in more stealing
    model = EconomicModel(
            num_econ_agents=70,
            initial_cops=2,
            width=10,
            height=10,
            election_frequency=70,
            sentence_length=15,
            interaction_memory=20,
            risk_aversion_std=0.1,
            trading_skill_std= 0.3
        )

    for step in range(1000):
        model.step()

    agent_results = model.datacollector.get_agent_vars_dataframe()

    last_step = agent_results.index.get_level_values('Step').max()
    last_step_data = agent_results.xs(last_step, level='Step')



    plt.figure()
    plt.scatter(last_step_data['trading_skill'], last_step_data['total_trading_gain'])
    plt.xlabel('trading skill')
    plt.ylabel('total wealth accumulated trading')
    plt.show()

    plt.figure()
    plt.scatter(last_step_data['trading_skill'], last_step_data['wealth'])
    plt.xlabel('trading skill')
    plt.ylabel('final wealth')
    plt.show()

    fig, ax1 = plt.subplots()
    scatter1 = ax1.scatter(last_step_data['trading_skill'], last_step_data['total_trading_gain'], color='g', label='total_trading_gain')
    ax1.set_xlabel('trading_skill')
    ax1.set_ylabel('total_trading_gain')
    ax2 = ax1.twinx()
    scatter2 = ax2.scatter(last_step_data['trading_skill'], last_step_data['total_stealing_gain'], color='r', label='total_stealing_gain')
    ax2.set_ylabel('total stealing gain')
    ax2.set_ylim(ax1.get_ylim())
    plt.show()

    plt.figure()
    plt.scatter(last_step_data['trading_skill'], last_step_data['crimes_committed_agent'])
    plt.xlabel('trading skill')
    plt.ylabel('amount of crimes committed')
    plt.show()



def starting_wealth():
        #Seeing if starting wealth impacts the final wealth at all
        model = EconomicModel(
            num_econ_agents=70,
            initial_cops=2,
            width=10,
            height=10,
            election_frequency=70,
            sentence_length=15,
            interaction_memory=20,
            risk_aversion_std=0.1,
            trading_skill_std= 0.1
        )

        for step in range(1000):
            model.step()

        agent_results = model.datacollector.get_agent_vars_dataframe()

        last_step = agent_results.index.get_level_values('Step').max()
        last_step_data = agent_results.xs(last_step, level='Step')

        plt.figure()
        plt.scatter(last_step_data['starting_wealth'], last_step_data['wealth'])
        plt.xlabel('starting_wealth')
        plt.ylabel('final wealth')
        plt.show()


def risk_check():
    #Increasing risk aversion sd to see impact on amount of times arrested
    model = EconomicModel(
        num_econ_agents=70,
        initial_cops=2,
        width=10,
        height=10,
        election_frequency=70,
        sentence_length=15,
        interaction_memory=20,
        risk_aversion_std=0.3,
        trading_skill_std= 0.1
    )
     
    for step in range(1000):
        model.step()

    agent_results = model.datacollector.get_agent_vars_dataframe()

    last_step = agent_results.index.get_level_values('Step').max()
    last_step_data = agent_results.xs(last_step, level='Step')

    plt.figure()
    plt.scatter(last_step_data['risk_aversion'], last_step_data['amount_arrested'])
    plt.xlabel('risk_aversion')
    plt.ylabel('amount_arrested')
    plt.show()




trading_skill_tests()
starting_wealth()
risk_check()