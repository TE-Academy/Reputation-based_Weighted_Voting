# TODO: Decide between existing overall reweighting mechanism, or just rewrite.

#TODO: Re-work this to use types. 
# TODO: OrderedReweightingMechanism, where the groups are placed in an ordered list, and the groups cweights are calculated so as to enforce this order. 
# TODO: BondingCurveReweightingMechanism, where we use Bonding Curves. 

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



        





    
    # def calc_new_cred_weights(self,
    #                          group_name: str,
    #                          group_rules: Dict,
    #                          target_cweight: float) -> Dict[str, float]:
    #     """
    #     Calculate the new weights for credentials in a group.
    #     """
    #     scaling_factor = self.calc_scaling_factor(group_name = group_name, 
    #                                               target_cweight = target_cweight)
    #     # TODO: Double-check this, but I think it's correct now. 
    #     reweighted_credentials = {}

    #     credentials_to_reweight_list = group_rules.get(group_name).get("credentials_to_reweight")

    #     for rule_name in credentials_to_reweight_list:
    #         initial_credential_weight = self.initial_credential_weights.get(rule_name)
    #         new_credential_weight = scaling_factor * initial_credential_weight
    #         reweighted_credentials[rule_name] = new_credential_weight

    #     return reweighted_credentials 


    # def add_new_cred_weights(self,
    #                          cred_weights_to_add: Dict[str, float]) -> bool:
    #     """
    #     Add new credential weights to the current weights.
    #     """
    #     disjoint_condition_check = not set(self.current_cred_weights.keys()).intersection(cred_weights_to_add.keys()) 
    #     msg_if_not_disjoint = "It appears a credential is being updated more than once."
    #     assert disjoint_condition_check, msg_if_not_disjoint
        
    #     self.current_credential_weights.update(cred_weights_to_add)
    #     return True

    
    # def calc_target_cweights(self, 
    #                          group_proportions: Dict[str, float]):
    #     """
    #     Calculate the target weights for each group.
    #     """
    #     # Check to make sure that there is more than one group.
    #     correct_group_proportions_length_check = len(group_proportions) > 1
    #     incorrect_group_proportions_msg = "There must be more than one group."
    #     assert correct_group_proportions_length_check, incorrect_group_proportions_msg

    #     #TODO: Refactor so things are in a specific order? (Decreasing/increasing, etc. )
        
    #     ######################################################
    #     ## We calculate the target_cweight for each group   ##
    #     ## This is set as a dictionary that is returned     ##
    #     ## for use in a different function.                 ##
    #     ######################################################

    #     group_proportions_key_list = list(group_proportions.keys())
    #     group_proportions_values_list = list(group_proportions.values())
    #     base_group = group_proportions_key_list[0]
    #     base_group_cweight = self.calc_group_cweight(voter_data = self.initial_voter_data,
    #                                            group_name = base_group,
    #                                            group_masks = self.group_masks,
    #                                            weights_dict = self.initial_cweights)

    #     target_cweights = Dict()

    #     for group_name in group_proportions_key_list:
    #         group_target_proportion = group_proportions.get(group_name)
    #         group_target_cweight = (group_target_proportion/base_group_proportion) * base_group_cweight
    #         target_cweights[group_name] = group_target_cweight

    #     return target_cweights

    # TODO: Compare to reweight all credentials, which is better? 
    # def reweight_all_credentials(self) -> bool:
    #     """
    #     Reweight all credentials so that groups have their intended weight proportions. 

    #     #TODO: Double-check everything called here, and write relevant tests. 
    #     """
    #     # Reweighting all credentials starts over, resetting current_credential_weights
    #     self.current_credential_weights = {}

    #     target_cweight_dict = self.calc_target_cweights()

    #     # For each group
    #     for group_name in self.group_proportions:
    #         # Find the intended target weights
    #         target_cweight = target_cweight_dict.get(group_name)
    #         # Calculate the scaling factor. 
    #         scaling_factor = self.calc_scaling_factor(group_name = group_name,
    #                                                   target_cweight = target_cweight)
    #         # Get list of credentials to reweight
    #         credentials_to_reweight_list = self.group_rules.get(group_name)

    #          # For each credential to be reweighted, multiply by the scaling factor. 
    #         for cred in credentials_to_reweight_list:
    #             self.current_credential_weights[cred] = scaling_factor * self.initial_credential_weights.get(cred)


    #     return True


        


def main():
    # Example usage of the ProportionalReweightingMechanism class
    initial_voter_data = pd.DataFrame({
        'Voter1': [1, 0, 1],
        'Voter2': [0, 1, 1],
        'Voter3': [1, 1, 0]
    })

    new_credentials = {
        "cred1": lambda row: row.sum() > 1,
        "cred2": lambda row: row['Voter1'] == 1
    }

    group_rules = {
        "group1": {
            "selection_rule": lambda row: row['Voter1'] == 1,
            "credentials_to_sum": ["cred1", "cred2"],
            "credentials_to_reweight": ["cred_2"]
        },
        "group2": {
            "selection_rule": lambda row: row['Voter2'] == 1,
            "credentials_to_sum": ["cred2"],
            "credentials_to_reweight": ["cred_3"]
        }
    }

    group_proportions = {
        "group1": 0.6,
        "group2": 0.4
    }

    initial_credential_weights = {
        "cred1": 1.5,
        "cred2": 2.0
    }

    pr_mechanism = ProportionalReweightingMechanism(
        initial_voter_data=initial_voter_data,
        new_credentials=new_credentials,
        group_rules=group_rules,
        group_proportions=group_proportions,
        initial_credential_weights=initial_credential_weights
    )

    # Create the modified voter data with new columns
    modified_voter_data = pr_mechanism.create_modified_voter_data()
    print("Modified Voter Data:")
    print(modified_voter_data)

    # Process the group rules and create group DataFrames
    group_masks = pr_mechanism.process_group_rules_to_masks()
    print("\nGroup Masks:")
    for group_name, group_df in group_masks.items():
        print(f"{group_name}:")
        print(group_df)

if __name__ == "__main__":
    main()