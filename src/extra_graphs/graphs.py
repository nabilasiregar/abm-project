import numpy as np
import pandas as pd
import mesa
from model import EconomicModel, compute_gini
from agent import EconomicAgent, CopAgent
import matplotlib.pyplot as plt

def change_tax_rate_wide_risk():

    starting_taxx = []
    results_crime = []
    max_crime = []
    min_crime = []

    
    for taxx in np.linspace(0.01,0.1,10):

        results_this_sd = []

        for repeats in range(50):
             
            model = EconomicModel(
                num_econ_agents=70,
                initial_cops=2,
                width=10,
                height=10,
                election_frequency=70,
                sentence_length=15,
                interaction_memory=20,
                risk_aversion_std= 0.9,
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
        max_crime.append(max(results_this_sd) - average_crime)
        min_crime.append(average_crime - min(results_this_sd))


    return starting_taxx, results_crime, min_crime, max_crime

def change_tax_rate_wide_trading():

    starting_taxx = []
    results_crime = []
    max_crime = []
    min_crime = []

    
    for taxx in np.linspace(0.01,0.1,10):

        results_this_sd = []

        for repeats in range(50):
             
            model = EconomicModel(
                num_econ_agents=70,
                initial_cops=2,
                width=10,
                height=10,
                election_frequency=70,
                sentence_length=15,
                interaction_memory=20,
                risk_aversion_std= 0.1,
                trading_skill_std= 0.9,
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
        max_crime.append(max(results_this_sd) - average_crime)
        min_crime.append(average_crime - min(results_this_sd))


    return starting_taxx, results_crime, min_crime, max_crime

def change_tax_rate():

    starting_taxx = []
    results_crime = []
    max_crime = []
    min_crime = []

    
    for taxx in np.linspace(0.01,0.1,10):

        results_this_sd = []

        for repeats in range(50):
             
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
        max_crime.append(max(results_this_sd) - average_crime)
        min_crime.append(average_crime - min(results_this_sd))


    return starting_taxx, results_crime, min_crime, max_crime


change_tax = change_tax_rate()
change_tax_risk = change_tax_rate_wide_risk()
change_tax_trading = change_tax_rate_wide_trading()


plt.plot(change_tax[0], change_tax[1],'ro', label = 'normal')
plt.plot(change_tax_risk[0], change_tax_risk[1],'go', label = 'wide risk aversion distribution')
plt.plot(change_tax_trading[0], change_tax_trading[1],'bo', label = 'wide trading skill distribution')

plt.xlabel('Tax rate')
plt.ylabel('Number of Crimes Committed')
plt.legend()
plt.savefig('src/extra_graphs/final/Tax changing all compared.png')
plt.close()


y_error_tax =[change_tax[2], change_tax[3]]
y_error_tax_risk = [change_tax_risk[2], change_tax_risk[3]]
y_error_tax_trading = [change_tax_trading[2], change_tax_trading[3]]

plt.plot(change_tax[0], change_tax[1],'ro', label = 'normal')

plt.errorbar(change_tax[0], change_tax[1],
        yerr = y_error_tax, 
        fmt ='o',
        ecolor = 'r')
plt.plot(change_tax_risk[0], change_tax_risk[1],'go', label = 'wide risk aversion distribution')

plt.errorbar(change_tax_risk[0], change_tax_risk[1],
        yerr = y_error_tax_risk, 
        fmt ='o',
        ecolor = 'g')
plt.plot(change_tax_trading[0], change_tax_trading[1],'bo', label = 'wide trading skill distribution')

plt.errorbar(change_tax_trading[0], change_tax_trading[1],
        yerr = y_error_tax_trading, 
        fmt ='o',
        ecolor = 'b')

plt.xlabel('Tax rate')
plt.ylabel('Number of Crimes Committed')
plt.legend()
plt.savefig('src/extra_graphs/final/Tax changing all compared with error.png')
plt.close()

def wide_risk_sentence():

    sentence_length = []
    results_crime = []
    max_crime = []
    min_crime = []

    
    for length in range(5,50,5):

        results_this_sd = []

        for repeats in range(50):
             
            model = EconomicModel(
                num_econ_agents=70,
                initial_cops=2,
                width=10,
                height=10,
                election_frequency=70,
                sentence_length=length,
                interaction_memory=20,
                risk_aversion_std= 0.9,
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
        max_crime.append(max(results_this_sd) - average_crime)
        min_crime.append(average_crime - min(results_this_sd))

    return sentence_length, results_crime, min_crime, max_crime

def wide_trading_sentence():

    sentence_length = []
    results_crime = []
    max_crime = []
    min_crime = []

    
    for length in range(5,50,5):

        results_this_sd = []

        for repeats in range(50):
             
            model = EconomicModel(
                num_econ_agents=70,
                initial_cops=2,
                width=10,
                height=10,
                election_frequency=70,
                sentence_length=length,
                interaction_memory=20,
                risk_aversion_std= 0.1,
                trading_skill_std= 0.9
            )

            for step in range(1000):
                model.step()

            step_data = model.datacollector.get_model_vars_dataframe().iloc[-1].to_dict()
            results_this_sd.append(step_data['num_crimes_committed'])
        
        
        average_crime = np.mean(results_this_sd)
        print(average_crime, length)
        
        sentence_length.append(length)
        results_crime.append(average_crime)
        max_crime.append(max(results_this_sd) - average_crime)
        min_crime.append(average_crime - min(results_this_sd))

    return sentence_length, results_crime, min_crime, max_crime

def just_sentence():


    sentence_length = []
    results_crime = []
    max_crime = []
    min_crime = []

    
    for length in range(5,50,5):

        results_this_sd = []

        for repeats in range(50):
             
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
        max_crime.append(max(results_this_sd) - average_crime)
        min_crime.append(average_crime - min(results_this_sd))

    return sentence_length, results_crime, min_crime, max_crime

change_sentence = just_sentence()
change_sentence_risk = wide_risk_sentence()
change_sentence_trading = wide_trading_sentence()


plt.plot(change_sentence[0], change_sentence[1],'ro', label = 'normal')
plt.plot(change_sentence_risk[0], change_sentence_risk[1],'go', label = 'wide risk aversion distribution')
plt.plot(change_sentence_trading[0], change_sentence_trading[1],'bo', label = 'wide trading skill distribution')

plt.xlabel('Sentence Length')
plt.ylabel('Number of Crimes Committed')
plt.legend()
plt.savefig('src/extra_graphs/final/Sentence length all compared.png')
plt.close()


y_error_sentence =[change_sentence[2], change_sentence[3]]
y_error_sentence_risk = [change_sentence_risk[2], change_sentence_risk[3]]
y_error_sentence_trading = [change_sentence_trading[2], change_sentence_trading[3]]

plt.plot(change_sentence[0], change_sentence[1],'ro', label = 'normal')

plt.errorbar(change_sentence[0], change_sentence[1],
        yerr = y_error_sentence, 
        fmt ='o',
        ecolor = 'r')
plt.plot(change_sentence_risk[0], change_sentence_risk[1],'go', label = 'wide risk aversion distribution')

plt.errorbar(change_sentence_risk[0], change_sentence_risk[1],
        yerr = y_error_sentence_risk, 
        fmt ='o',
        ecolor = 'g')
plt.plot(change_sentence_trading[0], change_sentence_trading[1],'bo', label = 'wide trading skill distribution')

plt.errorbar(change_sentence_trading[0], change_sentence_trading[1],
        yerr = y_error_sentence_trading, 
        fmt ='o',
        ecolor = 'b')

plt.xlabel('Sentence Length')
plt.ylabel('Number of Crimes Committed')
plt.legend()
plt.savefig('src/extra_graphs/final/Sentence length all compared with error.png')
plt.close()