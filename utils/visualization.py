"""
This module allows for visualization of data related to voter weights.
"""


from typing import Dict
import matplotlib.pyplot as plt
import pandas as pd


def compare_bars_voter_weights(initial_weight_distribution: Dict[str, Dict[str, float]], 
                              final_weight_distribution: Dict[str, Dict[str, float]]):
    """
    This function plots the initial and final weight distributions using bar plots.
    
    Parameters:
    initial_weight_distribution (list): The initial weight distribution.
    final_weight_distribution (list): The final weight distribution.
    
    Returns:
    fig: The figure object containing the plots.
    """
    # Create a figure with two subplots
    fig, axs = plt.subplots(1, 2, figsize=(15, 5))

    # Plotting initial weight distribution
    axs[0].bar(range(len(initial_weight_distribution)), initial_weight_distribution, color='blue')
    axs[0].set_title('Initial Weight Distribution')
    axs[0].set_xlabel('Voter Number')
    axs[0].set_ylabel('Weight')

    # Plotting final weight distribution
    axs[1].bar(range(len(final_weight_distribution)), final_weight_distribution, color='red')
    axs[1].set_title('Final Weight Distribution')
    axs[1].set_xlabel('Voter Number')
    axs[1].set_ylabel('Weight')

    # Adjust layout to make room for titles
    plt.tight_layout()

    # Show the plots
    plt.show()

    return fig

def compare_bar_voter_distributions(initial_voter_weights, final_voter_weights):
    fig, axs = plt.subplots(1, 2, figsize=(15, 5))

    initial_voters = initial_voter_weights.keys()

    # Plotting original weight distribution
    initial_weights = [initial_voter_weights.get(voter).get("weight") for voter in initial_voter_weights.keys()]
    axs[0].bar(range(len(initial_weights)), initial_weights, color='blue')
    axs[0].set_title('Original Weight Distribution')
    axs[0].set_ylabel('Weight')

    # Plotting proportional weight distribution
    final_weights = [final_voter_weights.get(voter).get("weight") for voter in final_voter_weights.keys()]
    axs[1].bar(range(len(final_weights)), final_weights, color='red')
    axs[1].set_title('Final Weight Distribution')
    axs[1].set_ylabel('Weight')

    # Force the two y-axes to be the same
    max_weight = max(max(initial_weights), max(final_weights))
    axs[0].set_ylim(0, max_weight)
    axs[1].set_ylim(0, max_weight)

    # Adjust layout to make room for titles
    plt.tight_layout()

    # Show the plots
    plt.show()

    return axs



