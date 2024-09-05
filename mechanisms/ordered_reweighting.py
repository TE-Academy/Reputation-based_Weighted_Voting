import pandas as pd

from mechanisms.reweighting import ReweightingMechanism
from mechanisms.reweighting_types import *

class OrderedReweightingMechanism(ReweightingMechanism):
    """
    A Reweighting Mechanism that takes in an order in which group_cweights should go. 

    """

    def __init__(self, 
                 initial_voter_data: pd.DataFrame = None, 
                 new_credentials: NewCredentialRulesDict = None, 
                 group_rules: GroupRulesDict = None, 
                 initial_credential_weights: Dict[str, float] = None,
                 group_order: List[GroupName] = None):
        """
        Initialize the ProportionalReweightingMechanism.
        """
        super().__init__(initial_voter_data = initial_voter_data,
                         new_credentials = new_credentials,
                         group_rules = group_rules,
                         initial_credential_weights = initial_credential_weights)

        self.group_order = group_order 
        self.target_cweights = self.calc_target_cweights()

    def calc_target_cweights(self) -> Dict[str, float]:
        """
        Calculate the target cweight for each group. 
        """
        # Create a blank dictionary
        target_cweights = {}
        
        # Calculate the first group's cweight
        first_group_name = self.group_order[0]
        first_group_mask = self.group_masks.get(first_group_name)
        first_group_cweight = self.calc_masked_cweight(voter_data = self.current_voter_data, 
                                                        mask_to_use = first_group_mask,
                                                        weights_dict = self.current_credential_weights)

        target_cweights[first_group_name] = first_group_cweight

        for k in range(1, len(self.group_order)):
            prev_group_name = self.group_order[k - 1]
            prev_group_target_cweight = target_cweights.get(prev_group_name)

            current_group_name = self.group_order[k]
            current_group_mask = self.group_masks.get(current_group_name)
            current_group_current_cweight = self.calc_masked_cweight(voter_data = self.current_voter_data, 
                                                            mask_to_use = current_group_mask,
                                                            weights_dict = self.current_credential_weights)

            current_group_target_cweight = max(prev_group_target_cweight, current_group_current_cweight)
            target_cweights[current_group_name] = current_group_target_cweight

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



                

            

    # TODO: Update all current credential weights. 




    
    # def calc_scaling_factor(self, 
    #                         group_name: str,
    #                         target_cweight: float) -> float:
    #     """
    #     Calculate the scaling factor for a group.
    #     """
    #     current_cweight = self.calc_group_cweight(voter_data = self.modified_voter_data,
    #                                               group_name = group_name,
    #                                               group_masks = self.group_masks,
    #                                               weights_dict = self.current_credential_weights)
        
    #     credentials_to_add = self.group_rules.get(group_name).get("credentials_to_add")
    #     credentials_to_reweight = self.group_rules.get(group_name).get("credentials_to_reweight")
    #     credentials_to_subtract = [cred_name for cred_name in credentials_to_add if not(cred_name in credentials_to_reweight)]
        
    #     # Create a blank copy of a dataframe
    #     already_weighted_df = 0 * self.modified_voter_data 
    #     # TODO: Have already_weighted_df be built here. 

    #     return scaling_factor

