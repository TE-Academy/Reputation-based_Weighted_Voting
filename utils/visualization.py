"""
This module allows for visualization of data related to voter weights.
"""

import matplotlib.pyplot as plt


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


