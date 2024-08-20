from math import ceil, floor
import random


def sample_dict_keys_values(input_dict: dict, sample_size: int):
    """
    Samples a specific number of keys and values from a dictionary and creates a new dictionary.
    
    Parameters:
    input_dict (dict): The input dictionary from which to sample.
    sample_size (int): The number of keys and values to sample.
    
    Returns:
    dict: A new dictionary with the sampled keys and values.
    """
    if sample_size > len(input_dict):
        raise ValueError("Sample size cannot be greater than the size of the input dictionary.")
    
    if sample_size < 0:
        raise ValueError("The sample size must be positive.")

    sampled_keys = random.sample(list(input_dict.keys()), sample_size)
    sampled_dict = {key: input_dict[key] for key in sampled_keys}
    
    return sampled_dict

def sample_voting_population_by_size(input_dict: dict, sample_size: int):
    sampled_dict = sample_dict_keys_values(input_dict = input_dict, sample_size = sample_size)
    return sampled_dict

def samples_voting_population_by_pct_range(input_dict: dict, 
                                          num_samples: int, 
                                          min_pct: float = 0.0,
                                          max_pct: float = 1.0):
    """
    Returns a smaller dictionary whose number of entries is between min_pct and max_pct.s 
    """
    dict_size = len(input_dict.keys())
    sample_size_min = ceil(min_pct * dict_size)
    sample_size_max = floor(max_pct * dict_size)
    
    #Pre-allocating list for efficiency in later loop
    voting_sample = [None] * num_samples

    for k in range(num_samples):
        voting_sample_size = random.randint(sample_size_min, sample_size_max)
        voting_sample[k] = sample_voting_population_by_size(input_dict = input_dict,
                                                            sample_size = voting_sample_size)
        
    assert not(any([entry is None for entry in voting_sample]))
    assert len(voting_sample) == num_samples

    return voting_sample








