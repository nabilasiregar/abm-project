import matplotlib.pyplot as plt
import pandas as pd

def plot_ofat_analysis(data, parameter, x_label, title):
    """
    Plots the results of a One Factor at a Time (OFAT) analysis.

    This function aggregates the specified model output over steps and iterations,
    then plots the mean value of the metric against the specified parameter.
    It also includes a fill between area representing ±1 standard deviation
    to show the variability due to stochasticity in the simulations.

    Parameters:
    - data (pd.DataFrame): The DataFrame containing the results.
    - parameter (str): The model parameter to vary (e.g., 'sentence_length', 'risk_aversion_std').
    - x_label (str): Label for the x-axis.
    - title (str): Title of the plot.
    """
    data = data.reset_index(drop=True)

    metrics = {
        'gini_coeff': 'Gini Coefficient',
        'total_wealth': 'Population Wealth',
        'num_crimes_committed': 'Number of Crimes Committed'
    }
    
    fig, axs = plt.subplots(3, 1, figsize=(8, 12))

    for ax, (metric, y_label) in zip(axs, metrics.items()):
        # Aggregate data across all steps and iterations
        metric_per_step = data.groupby([parameter, 'iteration', 'Step'])[metric].mean().reset_index()
        metric_per_iteration = metric_per_step.groupby([parameter, 'iteration'])[metric].mean().reset_index()
        metric_summary = metric_per_iteration.groupby(parameter)[metric].agg(['mean', 'std']).reset_index()
        
        # Calculate from the last step of each iteration
        last_step_data = data.groupby([parameter, 'iteration']).apply(lambda df: df[df['Step'] == df['Step'].max()]).reset_index(drop=True)
        last_step_metric_summary = last_step_data.groupby(parameter)[metric].agg(['mean', 'std']).reset_index()

        # Plotting the average of all steps
        ax.plot(metric_summary[parameter], metric_summary['mean'], marker='o', linestyle='-', label=f'Average {y_label}')
        ax.fill_between(metric_summary[parameter], 
                        metric_summary['mean'] - metric_summary['std'],
                        metric_summary['mean'] + metric_summary['std'],
                        color='b', alpha=0.2, label='±1 Std. Dev. All Steps')

        # Plotting the average from the last step of each iteration
        ax.plot(last_step_metric_summary[parameter], last_step_metric_summary['mean'], marker='x', linestyle='--', label=f'Last Step {y_label}')
        ax.fill_between(last_step_metric_summary[parameter], 
                        last_step_metric_summary['mean'] - last_step_metric_summary['std'],
                        last_step_metric_summary['mean'] + last_step_metric_summary['std'],
                        color='r', alpha=0.2, label='±1 Std. Dev. Final Step')

        ax.set_title(f'{title} - {y_label}')
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.legend()

    plt.tight_layout()
    plt.show()
