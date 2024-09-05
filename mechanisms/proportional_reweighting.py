"""
Implements a proportional reweighting mechanism.
"""

from typing import Callable, Dict
import pandas as pd

from mechanisms.reweighting import ReweightingMechanism
from mechanisms.reweighting_types import *

class ProportionalReweightingMechanism(ReweightingMechanism):
    """
    A class to implement the Proportional Reweighting Mechanism.
    """
    def __init__(self, 
                 initial_voter_data: pd.DataFrame = None, 
                 new_credentials: NewCredentialRulesDict = None, 
                 group_rules: GroupRulesDict = None, 
                 initial_credential_weights: Dict[str, float] = None,
                 group_proportions: Dict[str, float] = None):
        """
        Initialize the ProportionalReweightingMechanism.
        """
        super().__init__(initial_voter_data = initial_voter_data,
                         new_credentials = new_credentials,
                         group_rules = group_rules,
                         initial_credential_weights = initial_credential_weights)

        self.group_proportions = group_proportions
        self.target_cweights = self.calc_target_cweights()

    ################################$
    ## Begin methods to re-weight  ##
    ################################$ 
    
    def calc_target_cweights(self) -> Dict[str, float]:
        """
        Calculate the target cweight for each group. 
        """
        min_proportion_group_name = min(self.group_proportions, key=self.group_proportions.get)
        min_proportion = self.group_proportions.get(min_proportion_group_name) 
        min_proportion_group_mask = self.group_masks.get(min_proportion_group_name)
        min_proportion_group_cweight = self.calc_masked_cweight(voter_data = self.current_voter_data,
                                                                mask_to_use = min_proportion_group_mask,
                                                                weights_dict = self.current_credential_weights)
        target_cweights = {}

        for group_name, group_proportion in self.group_proportions.items():
            ratio = group_proportion/min_proportion
            group_target_cweight = ratio * min_proportion_group_cweight
            target_cweights[group_name] = group_target_cweight

        return target_cweights


    def update_all_current_credential_weights(self) -> bool:
        """
        Update all current credential weights to achieve the desired group proportions (if possible).
        """
        # Iterate over 
        for group_name, target_cweight in self.target_cweights.items():

            # Calculate the scaling factor for the group, based on the target_cweight dictionary.
            scaling_factor = self.calc_scaling_factor_for_target_cweight(group_name = group_name,
                                                                        target_cweight = target_cweight)
            
            # Calculate reweighted creds for the group, using the just-calculated scaling factor
            reweighted_credentials = self.reweighted_creds_by_scaling_factor(group_name = group_name,
                                                                            group_rules = self.group_rules,
                                                                            current_cred_weights = self.current_credential_weights,
                                                                            scaling_factor = scaling_factor)

            # Update the current_credential_weights dictionary, using the reweighted_creds
            self.current_credential_weights.update(reweighted_credentials)

        return True, self.current_credential_weights

