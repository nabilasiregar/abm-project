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
        'total_wealth': ['mean', 'std'],
        'gini_coeff': ['mean', 'std'],
        'num_cops': ['mean', 'std']
    })

    # Calculate the min and max across averaged iterations
    iteration_avg_data = data.groupby([param_column, 'iteration']).mean().reset_index()
    min_max_data = iteration_avg_data.groupby(param_column).agg({
        'num_crimes_committed': ['min', 'max'],
        'total_wealth': ['min', 'max'],
        'gini_coeff': ['min', 'max'],
        'num_cops': ['min', 'max']
    })
    
    mean_std_data.columns = ['_'.join(col).rstrip('_') for col in mean_std_data.columns.values]
    min_max_data.columns = ['_'.join(col).rstrip('_') for col in min_max_data.columns.values]

    fig, axs = plt.subplots(2, 2, figsize=(10, 8))
    outputs = ['num_crimes_committed', 'total_wealth', 'gini_coeff', 'num_cops']
    labels = ['Number of Crimes Committed', 'Population Wealth', 'Gini Coefficient', 'Number of Cops']

    for i, output in enumerate(outputs):
        ax = axs[i // 2, i % 2]
        ax.errorbar(mean_std_data.index, mean_std_data[output + '_mean'], yerr=mean_std_data[output + '_std'], 
                    fmt='o', color='green', label='Mean ± SD')
        ax.scatter(min_max_data.index, min_max_data[output + '_min'], color='pink', marker='x', label='Min')
        ax.scatter(min_max_data.index, min_max_data[output + '_max'], color='blue', marker='+', label='Max')

        ax.set_xlabel(param_column.replace('_', ' ').title())
        ax.set_ylabel(labels[i])
        ax.legend()

    plt.tight_layout()
    plt.show()
