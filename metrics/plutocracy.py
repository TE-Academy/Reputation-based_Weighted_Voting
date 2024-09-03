from typing import Dict

import math

def get_all_weights(weighted_voters: Dict[str, Dict[str, float]]) -> List[float]:
    """
    Get a list of all the weights for a dictionary of voters with weights. 
    """
    weights = [weighted_voters.get(voter).get("weight")
               for voter in list(weighted_voters.keys())]
    return weights

def calc_total_weight(weighted_voters: Dict[str, Dict[str, float]]):
    """
    Get the total combined weight for a dictionary of voters with weights. 
    """
    weights = get_all_weights(weighted_voters)
    total_weight = sum(weights)
    return total_weight

def calc_average_weight(weighted_voters: Dict[str, Dict[str, float]]):
    """
    Calculate the average weight for a dictionary of voters with weights. 
    """ 
    num_voters = len(weighted_voters)
    total_weight = calc_total_weight(weighted_voters)
    average_weight = total_weight/num_voters
    return average_weight
    
def calc_nakamoto_coefficient_additive(weighted_voters: Dict[str, Dict[str, float]],
                        winning_pct: float = 0.5,
                         verbose: bool = False):
    """
    Calculates the smallest number of voters necessary to form an invincible plutocracy
    under an additive voting mechanism. Notice that this assumes the voting mechanism used is monotonic. 
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

def calc_swifty_cancellation_number_additive(all_weighted_voters: Dict[str, Dict[str, float]],
                        voters_to_cancel: List[str],
                        nft_weight_dict: Dict[str, float] = None,
                        verbose: bool = False):
    """
    Calculate the swifty cancellation number for a group of voters: the number of lowest-weight votes necessary to cancel this specific group. 

    
    """

    weight_to_cancel = {voter: all_weighted_voters.get(voter).get("weight") 
                                 for voter in voters_to_cancel}
    minimum_weight_possible = min(nft_weight_dict.values())
    swifty_cancellation_number = weight_to_cancel/minimum_weight_possible

    if verbose:
        print(f"The swifty cancellation number is {swifty_cancellation_number}")
    return swifty_cancellation_number

def calc_gini_coefficient(all_weighted_voters: Dict[str, Dict[str, float]]):
    """
    Calculate the gini coefficient for the weighted voters population. 
    """
    weights = [info.get("weight", 0) for _, info in all_weighted_voters.items()]
    average_weight = calc_average_weight(all_weighted_voters)
    num_voters = len(weights)
    pairwise_diffs = [abs(weights[i] - weights[j])
                      for i in range(num_voters) 
                      for j in range(i+1, n)]
    sum_pairwise_diffs = sum(pairwise_diffs)
    gini_coefficient = sum_pairwise_diffs/(2 * num_voters * num_voters * average_weight)

    if verbose:
        print(f"The gini coefficient is {gini_coefficient}")

    return gini_coefficient


def calc_theil_T_index(all_weighted_voters: Dict[str, Dict[str, float]]):
    """
    Calculate the Theil t-index for the weight distribution. 
    """
    weights = [info.get("weight", 0) for _, info in all_weighted_voters.items()]
    num_voters = len(weights)
    average_weight = calc_average_weight(all_weighted_voters)
    proportion_entropy = sum([(weight / average_weight) * math.log(weight / average_weight) for weight in weights])
    theil_T_index = proportion_entropy/num_voters
    
    return theil_T_index

def calc_theil_L_index(all_weighted_voters: Dict[str, Dict[str, float]]):
    """
    Calculate the Theil t-index for the weight distribution. 
    """
    weights = [info.get("weight", 0) for _, info in all_weighted_voters.items()]
    num_voters = len(weights)
    average_weight = calc_average_weight(all_weighted_voters)
    sum_log_proportion = sum([math.log(weight / average_weight) for weight in weights])
    theil_L_index = sum_log_proportion/num_voters
    
    return theil_L_index
    


    