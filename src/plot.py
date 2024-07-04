import matplotlib.pyplot as plt
import pandas as pd

def plot_ofat(data, param_column):
    """
    Plots statistical summaries (mean and standard deviation) and min-max from individual runs
    for several model outputs against a specified parameter from a simulation dataset.

    Args:
    data (pd.DataFrame): The DataFrame containing the simulation data.
    param_column (str): The name of the column in `data` that will be used as the parameter
                        for grouping the data (e.g., 'election_frequency'). This parameter
                        should reflect a simulation variable you want to analyze.

    Plots:
    Creates a 2x2 grid of subplots where each subplot represents one of the following outputs:
    - Number of Crimes Committed
    - Total Wealth
    - Gini Coefficient
    - Number of Cops

    Each subplot shows:
    - Mean values with error bars representing the standard deviation.
    - Scatter points for the minimum and maximum input values.

    The function adjusts the layout and displays the plot.
    """
    # Calculate mean and standard deviation across steps and iterations
    avg_data_per_step = data.groupby([param_column, 'iteration', 'Step']).mean().reset_index()
    mean_std_data = avg_data_per_step.groupby([param_column, 'iteration']).mean().groupby(param_column).agg({
        'num_crimes_committed': ['mean', 'std'],
        'num_arrests_made': ['mean', 'std'],
        'gini_coeff': ['mean', 'std'],
        'num_cops': ['mean', 'std']
    })

    mean_std_data.columns = ['_'.join(col).rstrip('_') for col in mean_std_data.columns.values]

    fig, axs = plt.subplots(2, 2, figsize=(10, 8))
    outputs = ['num_crimes_committed', 'num_arrests_made', 'gini_coeff', 'num_cops']
    labels = ['Number of Crimes Committed', 'Number of Arrests', 'Gini Coefficient', 'Number of Cops']

    for i, output in enumerate(outputs):
        ax = axs[i // 2, i % 2]
        ax.errorbar(mean_std_data.index, mean_std_data[output + '_mean'], yerr=mean_std_data[output + '_std'], 
                    fmt='o', color='#2667FF')
        ax.set_xlabel(param_column.replace('_', ' ').title())
        ax.set_ylabel(labels[i])

    plt.tight_layout()
    plt.show()

def plot_ofat_final_step(data, param_column, last_step_num):
    last_step_data = data[data['Step'] == last_step_num]

    # Calculate mean and standard deviation for the last step across iterations
    mean_std_data = last_step_data.groupby([param_column, 'iteration']).mean().groupby(param_column).agg({
        'num_crimes_committed': ['mean', 'std'],
        'gini_coeff': ['mean', 'std'],
        'avg_crime_perception': ['mean', 'std'],
        'num_cops': ['mean', 'std']
    })

    mean_std_data.columns = ['_'.join(col).rstrip('_') for col in mean_std_data.columns.values]

    fig, axs = plt.subplots(2, 2, figsize=(10, 8))
    outputs = ['num_crimes_committed', 'gini_coeff', 'avg_crime_perception', 'num_cops']
    labels = ['Number of Crimes Committed', 'Gini Coeff', 'Average Crime Perception', 'Number of Cops']

    for i, output in enumerate(outputs):
        ax = axs[i // 2, i % 2]
        ax.errorbar(mean_std_data.index, mean_std_data[output + '_mean'], yerr=mean_std_data[output + '_std'], 
                    fmt='o', color='#2667FF')

        ax.set_xlabel(param_column.replace('_', ' ').title())
        ax.set_ylabel(labels[i])

    plt.tight_layout()
    plt.show()