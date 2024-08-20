from typing import Dict

def calc_nakamoto_coefficient_additive(weighted_voters: Dict[str, Dict[str, float]],
                        winning_pct: float = 0.5,
                         verbose: bool = False):
    """
    Calculates the smallest number of voters necessary to form an invincible plutocracy
    under an additive voting mechanism. Notice that this wi
    """
    # Do checking on format
    for voter, info in weighted_voters.items():
        assert isinstance(info, dict), f"Expected a dictionary for voter {voter}, got {type(info)}"
        assert "weight" in info, f"Expected key 'weight' for voter {voter}, got {info.keys()}"

    sorted_voter_copy = {k: v 
                         for k, v
                         in sorted(weighted_voters.items(),
                                   key=lambda item: item[1]['weight'], reverse=True)}
    # Print if desired
    if verbose:
        print(sorted_voter_copy)
    
    # Calculate the total weight 
    total_weight = 0
    for _, info in sorted_voter_copy.items():
        total_weight += info.get("weight", 0)
    
    if verbose:
        print(f"The total weight is {total_weight}.")
    
    # Calculate the nakamoto coefficient
    winning_weight = winning_pct * total_weight
    voter_number = 0
    cumulative_weight = 0
    for _, info in sorted_voter_copy.items():
        voter_number += 1
        cumulative_weight += info.get("weight", 0)
        if cumulative_weight > winning_weight:
            nakamoto_coefficient = voter_number
            break

    if verbose:
        print(f"The Nakamoto Coefficient is {nakamoto_coefficient}.")

    return nakamoto_coefficient

def calc_swifty_number_additive(weighted_voters: Dict[str, Dict[str, float]],
                        winning_pct: float = 0.5,
                        nft_weight_dict: Dict[str, float] = None,
                        verbose: bool = False):
    """
    Calculate the swifty number. 
    """