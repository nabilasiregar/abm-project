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
    plt.savefig('src/extra_graphs/trading skill vs total trading income.png')

    plt.figure()
    plt.scatter(last_step_data['trading_skill'], last_step_data['wealth'])
    plt.xlabel('trading skill')
    plt.ylabel('final wealth')
    plt.savefig('src/extra_graphs/trading skill vs final wealth.png')

    fig, ax1 = plt.subplots()
    scatter1 = ax1.scatter(last_step_data['trading_skill'], last_step_data['total_trading_gain'], color='g', label='total_trading_gain')
    ax1.set_xlabel('trading_skill')
    ax1.set_ylabel('total_trading_gain')
    ax2 = ax1.twinx()
    scatter2 = ax2.scatter(last_step_data['trading_skill'], last_step_data['total_stealing_gain'], color='r', label='total_stealing_gain')
    ax2.set_ylabel('total stealing gain')
    ax2.set_ylim(ax1.get_ylim())
    plt.savefig('src/extra_graphs/total stealing gain and trading gain.png')

    plt.figure()
    plt.scatter(last_step_data['trading_skill'], last_step_data['crimes_committed_agent'])
    plt.xlabel('trading skill')
    plt.ylabel('amount of crimes committed')
    plt.savefig('src/extra_graphs/trading_skill_vs_crimes_committed')



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
        plt.savefig('src/extra_graphs/Starting_wealth_on_final_wealth')


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
    plt.savefig('src/extra_graphs/Risk aversion vs times arrested.png')

# def memory_vs_election():
    
#     results = []
#     for frequency in range(10,110,10):
        
#         for memory in range(5,105,5):
             
#             model = EconomicModel(
#                 num_econ_agents=70,
#                 initial_cops=2,
#                 width=10,
#                 height=10,
#                 election_frequency=frequency,
#                 sentence_length=15,
#                 interaction_memory=memory,
#                 risk_aversion_std=0.1,
#                 trading_skill_std= 0.1
#             )

#             for step in range(1000):
#                 model.step()

#             step_data = model.datacollector.get_model_vars_dataframe().iloc[-1].to_dict()
#             results.append(step_data)

#             print(results)



def varying_trading_std():

    StandardD = []
    results_crime = []
    
    for sd in np.linspace(0, 1, 11):

        results_this_sd = []

        for repeats in range(40):
             
            model = EconomicModel(
                num_econ_agents=70,
                initial_cops=2,
                width=10,
                height=10,
                election_frequency=70,
                sentence_length=15,
                interaction_memory=20,
                risk_aversion_std=0.1,
                trading_skill_std= sd
            )

            for step in range(1000):
                model.step()

            step_data = model.datacollector.get_model_vars_dataframe().iloc[-1].to_dict()
            results_this_sd.append(step_data['num_crimes_committed'])
        
        
        average_crime = np.mean(results_this_sd)
        print(average_crime, sd)
        
        StandardD.append(sd)
        results_crime.append(average_crime)

    plt.scatter(StandardD, results_crime)
    plt.xlabel('Standard deviation of trading skill')
    plt.ylabel('average_amount_arrested')
    plt.savefig('src/extra_graphs/Increase in trading skill gap vs amount of crimes commited 2.png')
    plt.close()


def varying_risk_std():

    StandardD = []
    results_crime = []
    
    for sd in np.linspace(0, 1, 11):

        results_this_sd = []

        for repeats in range(40):
             
            model = EconomicModel(
                num_econ_agents=70,
                initial_cops=2,
                width=10,
                height=10,
                election_frequency=70,
                sentence_length=15,
                interaction_memory=20,
                risk_aversion_std= sd,
                trading_skill_std= 0.1
            )

            for step in range(1000):
                model.step()

            step_data = model.datacollector.get_model_vars_dataframe().iloc[-1].to_dict()
            results_this_sd.append(step_data['num_crimes_committed'])
        
        
        average_crime = np.mean(results_this_sd)
        print(average_crime, sd)
        
        StandardD.append(sd)
        results_crime.append(average_crime)

    plt.scatter(StandardD, results_crime)
    plt.xlabel('Standard deviation of risk aversion')
    plt.ylabel('average_amount_arrested')
    plt.savefig('src/extra_graphs/Increase in SD risk aversion vs amount of crimes commited 2.png')
    plt.close()


def wide_trade_police():


    starting_cops = []
    results_crime = []
    
    for cops in range(0, 20, 2):

        results_this_sd = []

        for repeats in range(40):
             
            model = EconomicModel(
                num_econ_agents=70,
                initial_cops=cops,
                width=10,
                height=10,
                election_frequency=70,
                sentence_length=15,
                interaction_memory=20,
                risk_aversion_std= 0.1,
                trading_skill_std= 0.6
            )

            for step in range(1000):
                model.step()

            step_data = model.datacollector.get_model_vars_dataframe().iloc[-1].to_dict()
            results_this_sd.append(step_data['num_crimes_committed'])
        
        
        average_crime = np.mean(results_this_sd)
        print(average_crime, cops)
        
        starting_cops.append(cops)
        results_crime.append(average_crime)

    plt.scatter(starting_cops, results_crime)
    plt.xlabel('Amount of starting police')
    plt.ylabel('average_amount_arrested')
    plt.savefig('src/extra_graphs/Change in starting cops for a wide trade skill.png')
    plt.close()

def wide_risk_police():


    starting_cops = []
    results_crime = []
    
    for cops in range(0, 20, 2):

        results_this_sd = []

        for repeats in range(40):
             
            model = EconomicModel(
                num_econ_agents=70,
                initial_cops=cops,
                width=10,
                height=10,
                election_frequency=70,
                sentence_length=15,
                interaction_memory=20,
                risk_aversion_std= 0.6,
                trading_skill_std= 0.1
            )

            for step in range(1000):
                model.step()

            step_data = model.datacollector.get_model_vars_dataframe().iloc[-1].to_dict()
            results_this_sd.append(step_data['num_crimes_committed'])
        
        
        average_crime = np.mean(results_this_sd)
        print(average_crime, cops)
        
        starting_cops.append(cops)
        results_crime.append(average_crime)

    plt.scatter(starting_cops, results_crime)
    plt.xlabel('Amount of starting police')
    plt.ylabel('average_amount_arrested')
    plt.savefig('src/extra_graphs/Change in starting cops for a wide risk aversion.png')
    plt.close()

def wide_trade_sentence():

    sentence_length = []
    results_crime = []
    
    for length in range(5,50,5):

        results_this_sd = []

        for repeats in range(40):
             
            model = EconomicModel(
                num_econ_agents=70,
                initial_cops=2,
                width=10,
                height=10,
                election_frequency=70,
                sentence_length=length,
                interaction_memory=20,
                risk_aversion_std= 0.1,
                trading_skill_std= 0.6
            )

            for step in range(1000):
                model.step()

            step_data = model.datacollector.get_model_vars_dataframe().iloc[-1].to_dict()
            results_this_sd.append(step_data['num_crimes_committed'])
        
        
        average_crime = np.mean(results_this_sd)
        print(average_crime, length)
        
        sentence_length.append(length)
        results_crime.append(average_crime)

    plt.scatter(sentence_length, results_crime)
    plt.xlabel('Sentence Length')
    plt.ylabel('average_amount_arrested')
    plt.savefig('src/extra_graphs/Change in sentence length for a wide trade skill.png')
    plt.close()

def wide_aversion_sentence():

    sentence_length = []
    results_crime = []
    
    for length in range(5,50,5):

        results_this_sd = []

        for repeats in range(40):
             
            model = EconomicModel(
                num_econ_agents=70,
                initial_cops=2,
                width=10,
                height=10,
                election_frequency=70,
                sentence_length=length,
                interaction_memory=20,
                risk_aversion_std= 0.6,
                trading_skill_std= 0.1
            )

            for step in range(1000):
                model.step()

            step_data = model.datacollector.get_model_vars_dataframe().iloc[-1].to_dict()
            results_this_sd.append(step_data['num_crimes_committed'])
        
        
        average_crime = np.mean(results_this_sd)
        print(average_crime, length)
        
        sentence_length.append(length)
        results_crime.append(average_crime)

    plt.scatter(sentence_length, results_crime)
    plt.xlabel('Sentence Length')
    plt.ylabel('average_amount_arrested')
    plt.savefig('src/extra_graphs/Change in sentence length for a wide risk aversion.png')
    plt.close()

def changing_sentence():

    sentence_length = []
    results_crime = []
    
    for length in range(5,50,5):

        results_this_sd = []

        for repeats in range(40):
             
            model = EconomicModel(
                num_econ_agents=70,
                initial_cops=2,
                width=10,
                height=10,
                election_frequency=70,
                sentence_length=length,
                interaction_memory=20,
                risk_aversion_std= 0.1,
                trading_skill_std= 0.1
            )

            for step in range(1000):
                model.step()

            step_data = model.datacollector.get_model_vars_dataframe().iloc[-1].to_dict()
            results_this_sd.append(step_data['num_crimes_committed'])
        
        
        average_crime = np.mean(results_this_sd)
        print(average_crime, length)
        
        sentence_length.append(length)
        results_crime.append(average_crime)

    plt.scatter(sentence_length, results_crime)
    plt.xlabel('Sentence length')
    plt.ylabel('average_amount_arrested')
    plt.savefig('src/extra_graphs/Change in sentence length vs crime rate.png')
    plt.close()
    
            
def change_starting_police():

    starting_cops = []
    results_crime = []
    
    for cops in range(0, 20, 2):

        results_this_sd = []

        for repeats in range(40):
             
            model = EconomicModel(
                num_econ_agents=70,
                initial_cops=cops,
                width=10,
                height=10,
                election_frequency=70,
                sentence_length=15,
                interaction_memory=20,
                risk_aversion_std= 0.6,
                trading_skill_std= 0.1
            )

            for step in range(1000):
                model.step()

            step_data = model.datacollector.get_model_vars_dataframe().iloc[-1].to_dict()
            results_this_sd.append(step_data['num_crimes_committed'])
        
        
        average_crime = np.mean(results_this_sd)
        print(average_crime, cops)
        
        starting_cops.append(cops)
        results_crime.append(average_crime)

    plt.scatter(starting_cops, results_crime)
    plt.xlabel('Amount of starting police')
    plt.ylabel('average_amount_arrested')
    plt.savefig('src/extra_graphs/Change in starting cops for a wide risk aversion.png')
    plt.close()


def change_tax_rate():

    starting_taxx = []
    results_crime = []
    
    for taxx in np.linspace(0.01,0.1,10):

        results_this_sd = []

        for repeats in range(40):
             
            model = EconomicModel(
                num_econ_agents=70,
                initial_cops=2,
                width=10,
                height=10,
                election_frequency=70,
                sentence_length=15,
                interaction_memory=20,
                risk_aversion_std= 0.1,
                trading_skill_std= 0.1,
                tax_per_cop = taxx
            )

            for step in range(1000):
                model.step()

            step_data = model.datacollector.get_model_vars_dataframe().iloc[-1].to_dict()
            results_this_sd.append(step_data['num_crimes_committed'])
        
        
        average_crime = np.mean(results_this_sd)
        print(average_crime, taxx)
        
        starting_taxx.append(taxx)
        results_crime.append(average_crime)

    plt.scatter(starting_taxx, results_crime)
    plt.xlabel('Amount of starting taxx')
    plt.ylabel('average_amount_arrested')
    plt.savefig('src/extra_graphs/Change in tax rate on crime.png')
    plt.close()


# varying_trading_std()
# varying_risk_std()

# changing_sentence()
# change_starting_police()


# wide_aversion_sentence()
# wide_trade_sentence()
# wide_risk_police()
# wide_trade_police()

change_tax_rate()

# trading_skill_tests()
# starting_wealth()
# risk_check()
#memory_vs_election()