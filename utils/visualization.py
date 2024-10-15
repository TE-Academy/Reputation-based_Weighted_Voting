"""
This module allows for visualization of data related to voter weights.
"""

import matplotlib.pyplot as plt
from typing import Dict

def comparison_bar_distributions(initial_weight_distribution, final_weight_distribution):
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

def comparison_hist_distributions(initial_weight_distribution, final_weight_distribution):
    """
    This function plots the initial and final weight distributions using histogram plots.
    
    Parameters:
    initial_weight_distribution (list): The initial weight distribution.
    final_weight_distribution (list): The final weight distribution.
    
    Returns:
    fig: The figure object containing the plots.
    """
    # Create a figure with two subplots
    fig, axs = plt.subplots(1, 2, figsize=(15, 5))

    # Plotting initial weight distribution
    axs[0].hist(initial_weight_distribution, bins=20, color='blue', alpha=0.7)
    axs[0].set_title('Initial Weight Distribution')
    axs[0].set_xlabel('Weight')
    axs[0].set_ylabel('Frequency')

    # Plotting final weight distribution
    axs[1].hist(final_weight_distribution, bins=20, color='red', alpha=0.7)
    axs[1].set_title('Final Weight Distribution')
    axs[1].set_xlabel('Weight')
    axs[1].set_ylabel('Frequency')

    # Adjust layout to make room for titles
    plt.tight_layout()

    # Show the plots
    plt.show()

    return fig

def calculate_percentile_weights(voter_weights: Dict[str, Dict[str, float]]) -> Dict[int, float]:
    """
    This function calculates the voting weight held by the percentile, for use in a Lorenz Curve.
    
    Args:
        voter_weights (Dict[str, Dict[str, float]]): A nested dictionary, where the keys of the outer dictionary are voter names and the inner dictionary consists of key "weight" and value float.
    
    Returns:
        Dict[int, float]: A dictionary, with p as the key and the weight as the value.
    """
    # Sort the voter weights by their values
    sorted_weights = sorted(voter_weights.items(), key=lambda x: x[1]['weight'])
    
    # Calculate the total weight
    total_weight = sum(weight['weight'] for voter, weight in sorted_weights)
    
    # Initialize the percentile weights dictionary
    percentile_weights = {}
    
    # Calculate the weight for each percentile
    for p in range(1, 101):
        # Calculate the number of voters in the "first" p percent
        num_voters = int(len(sorted_weights) * p / 100)
        
        # Calculate the weight for this percentile
        percentile_weight = sum(weight['weight'] for voter, weight in sorted_weights[:num_voters])
        
        # Add the weight to the percentile weights dictionary
        percentile_weights[p] = percentile_weight / total_weight
    
    return percentile_weights

def plot_lorenz_curve(percentile_weights: Dict[int, float]) -> None:
    """
    Plots the Lorenz Curve based on the given percentile weights.
    
    Args:
        percentile_weights (Dict[int, float]): A dictionary with percentiles as keys and their corresponding weight proportions as values.
    """
    # Prepare data for plotting
    percentiles = list(percentile_weights.keys())
    weights = list(percentile_weights.values())
    
    # Add (0,0) point for the Lorenz Curve
    percentiles = [0] + percentiles
    weights = [0] + weights
    
    # Plotting the Lorenz Curve
    plt.figure(figsize=(8, 8))
    plt.plot(percentiles, weights, label='Lorenz Curve', color='blue')
    plt.plot([0, 100], [0, 1], label='Line of Equality', color='red', linestyle='--')
    
    # Shade the area between the Lorenz Curve and the Line of Equality
    plt.fill_between(percentiles, weights, color='blue', alpha=0.3)
    plt.fill_between([0, 100], [0, 1], color='red', alpha=0.1)
    
    plt.title('Lorenz Curve')
    plt.xlabel('Cumulative Percentage of Population (%)')
    plt.ylabel('Cumulative Percentage of Total Weight (%)')
    plt.legend()
    plt.grid()
    plt.show()

