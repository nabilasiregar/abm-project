import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from itertools import combinations
from SALib.analyze import sobol

def plot_index(ax, s, params, index, title, title_fontsize, label_fontsize, tick_fontsize):
    """
    Creates a plot for Sobol sensitivity analysis that shows the contributions
    of each parameter to the global sensitivity.

    Args:
        ax (Axes): Matplotlib Axes object to plot on
        s (dict): dictionary {'S1': array, 'S1_conf': array, 'ST': array, 'ST_conf': array} of dicts that hold
            the values for a set of parameters
        params (list): the parameters taken from s
        index (str): string that indicates what order the sensitivity is ('S1' or 'ST').
        title (str): title for the plot
        title_fontsize (int): font size for the title
        label_fontsize (int): font size for the labels
        tick_fontsize (int): font size for the tick labels
    """
    indices = s[index] 
    errors = s[index + '_conf']  
    
    ax.set_title(title, fontsize=title_fontsize)
    ax.set_ylim([-0.2, len(indices) - 1 + 0.2])
    ax.set_yticks(range(len(indices)))
    ax.set_yticklabels(params, fontsize=label_fontsize) 
    ax.errorbar(indices, range(len(indices)), xerr=errors, linestyle='None', marker='o')  
    ax.axvline(0, c='k')
    ax.set_xlabel('Sensitivity Index', fontsize=label_fontsize)
    ax.set_ylabel('Parameters', fontsize=label_fontsize)  
    ax.tick_params(axis='both', which='major', labelsize=tick_fontsize)
    ax.tick_params(axis='both', which='minor', labelsize=tick_fontsize)

def plot_first_and_total_order(s, params, title, title_fontsize, label_fontsize, tick_fontsize):
    """
    Plots the first order and total order sensitivity indices side by side.

    Args:
        s (dict): dictionary {'S1': array, 'S1_conf': array, 'ST': array, 'ST_conf': array} of sensitivity indices
        params (list): list of parameter names
        title (str): title for the plots
        title_fontsize (int): font size for the title
        label_fontsize (int): font size for the labels
        tick_fontsize (int): font size for the tick labels
    """
    fig, axes = plt.subplots(1, 2, figsize=(20, 10))  
    
    plot_index(axes[0], s, params, 'S1', title + ' - First Order', title_fontsize, label_fontsize, tick_fontsize)
    plot_index(axes[1], s, params, 'ST', title + ' - Total Order', title_fontsize, label_fontsize, tick_fontsize)
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95]) 
    plt.show()