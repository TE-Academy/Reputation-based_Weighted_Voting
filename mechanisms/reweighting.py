from typing import Union, List, Dict, Callable, NewType, TypedDict
import pandas as pd
from copy import deepcopy

from mechanisms.reweighting_types import *


class ReweightingMechanism:
    """
    A class for arbitrary reweighting mechanisms.
    """
    def __init__(self, 
                 initial_voter_data: VoterData = None, 
                 new_credentials: Dict[str, Callable[pd.Series, bool]] = None, 
                 group_rules: GroupRulesDict = None, 
                 initial_credential_weights: Dict[str, float] = None):
        self.initial_voter_data = initial_voter_data 
        self.new_credentials = new_credentials 
        self.group_rules = group_rules
        self.initial_credential_weights = initial_credential_weights

        self.target_cweights = self.calculate_target_cweights()
        self.current_voter_data = self.create_current_voter_data()
        self.group_masks = self.process_group_rules_to_masks()
        self.current_credential_weights = deepcopy(initial_credential_weights)

    def calculate_target_cweights(self) -> Dict:
        """
        Calculate the target cweight for each group. 

        This should be overridden by any subclass. 
        """
        return {}
         
    def create_current_voter_data(self) -> VoterData:
        """
        Create a modified voter data with new columns.

        This function uses the `new_credentials` and `group_rules` attributes to add new credentials. 
        """
        # Create a deep copy of the initial voter data
        current_voter_data = deepcopy(self.initial_voter_data)
        
        # Iterate over the new_credentials dictionary and apply the functions
        for cred_name, func in self.new_credentials.items():
            # Apply the function to each row and create a new column
            current_voter_data[cred_name] = current_voter_data.apply(func, axis=1)
       
        return current_voter_data

    def process_group_rules_to_masks(self) -> GroupMasksDict:
        """
        Process the group rules and create group masks.

        Group masks correspond to the entries in the DataFrame that should be added to give the group weight. 
        """
        group_dataframes = {}

        # Iterate over each group in the group_rules dictionary
        for group_name, rule in self.group_rules.items():
            # Initialize a DataFrame filled with zeros, with the same index and columns as the initial data
            group_df = pd.DataFrame(0, 
                                   index=self.current_voter_data.index, 
                                   columns=self.current_voter_data.columns)

            # Apply the selection rule to identify relevant rows
            row_data = self.current_voter_data.apply(rule['selection_rule'], axis=1)
            selected_rows = [row for row in group_df.index if row_data[row]]

            # Use the rules to get relevant credentials 
            selected_creds = rule.get("credentials_to_sum")
            
            # Set the relevant cells to 1 for the selected rows and specified credentials
            group_df.loc[selected_rows, selected_creds] = 1
            
            # Store the resulting DataFrame in the dictionary
            group_dataframes[group_name] = group_df

        return group_dataframes

        
    def check_valid_masks(self, 
                          voter_data, 
                          group_masks):
        """
        Check the validity of the group masks.
        """
        for group_name, mask in group_masks.items():
            if not mask.applymap(lambda x: x in [0,1]).all().all():
                raise ValueError(f"Mask for group '{group_name}' contains non-integer values.")

        num_rows = voter_data.shape[0]  # Number of rows
        num_columns = voter_data.shape[1]  # Number of columns
        all_masks_summed = sum(group_masks.values())

        if all_masks_summed.applymap(lambda x: x > 1).any().any():
            raise ValueError("There is an entry which is covered by more than one mask.")

        if all_masks_summed.applymap(lambda x: x < 1).any().any():
            raise ValueError("There is an entry which is not covered by any mask. ")

        return True


    def create_submask_by_creds(self, 
                       initial_mask: GroupMask,
                       cred_names: List[str]):
        """
        Create a submask based on specific credential names. 
        """
        submask_df = initial_mask * 0
        submask_df[cred_names] = 1
        submask_df = submask_df * initial_mask

        return submask_df


    def calc_masked_cweight(self,
                    voter_data: VoterData,
                    mask_to_use: GroupMask,
                    weights_dict: Dict[str, float]):
        """
        Calculate the weighted sum of the a subset of the VoterData, as determined by a mask. 
        """
        masked_voter_data = mask_to_use * voter_data
        weighted_masked_voter_info = masked_voter_data * pd.Series(weights_dict)
        masked_cweight = weighted_masked_voter_info.sum().sum()
        return masked_cweight

    def calc_group_cweight(self, 
                          group_name: str,
                          voter_data_to_use: VoterData = None,
                          group_masks_to_use: GroupMasksDict = None,
                          weights_to_use: Dict[str, float] = None):

        if voter_data_to_use is None:
            voter_data_to_use = self.current_voter_data
        if group_masks_to_use is None:
            group_masks_to_use = self.group_masks
        if weights_to_use is None:
            weights_to_use = self.current_credential_weights

        mask_to_use = group_masks_to_use.get(group_name)
        group_cweight = self.calc_masked_cweight(voter_data = voter_data_to_use,
                                                  mask_to_use = mask_to_use,
                                                  weights_dict = weights_to_use)
        return group_cweight


    # TODO: Test this function. 
    def calc_individual_voter_weight(self, 
                                    voter: str,
                                    voter_data_to_use: VoterData = None,
                                    weights_to_use: Dict[str, float] = None):
        """
        Calculate the current weight of an individual voter.
        """
        if voter_data_to_use is None:
            voter_data_to_use = self.current_voter_data
        if weights_to_use is None:
            weights_to_use = self.current_credential_weights

        voter_row = voter_data_to_use.loc[voter]
        voter_weight = sum(voter_row * pd.Series(weights_to_use))
        return voter_weight

    def calc_voter_weights(self,
                           voters: List[str],
                           voter_data_to_use: VoterData = None,
                           weights_to_use: Dict[str, float] = None):
        """
        Calculate voter-weight combinations for a specific group of voters. 
        """

        if voter_data_to_use is None:
            voter_data_to_use = self.current_voter_data
        if weights_to_use is None:
            weights_to_use = self.current_credential_weights

        voter_weights_dict = {}
        for voter_name in voters:
            voter_info = {}
            voter_weight = self.calc_individual_voter_weight(voter = voter_name,
                                            voter_data_to_use = voter_data_to_use,
                                            weights_to_use = weights_to_use)
            voter_info["weight"] = voter_weight
            voter_weights_dict[voter_name] = voter_info
                                                 
        return voter_weights_dict




    # TODO: Test this function. 
    def calc_all_voter_weights(self,
                                voter_data_to_use: VoterData = None,
                                weights_to_use: Dict[str, float] = None):
        """
        Return a dictionary of the voter weights, based on the current credential weights. 

        Note that this returns a special nested dictionary, where each voter has a dictionary whose only key is "weight".
        """
        
        if voter_data_to_use is None:
            voter_data_to_use = self.current_voter_data
        
        if weights_to_use is None:
            weights_to_use = self.current_credential_weights

        voters = [voter_name for voter_name in voter_data_to_use.index]

        voter_weights_dict = self.calc_voter_weights(voters = voters,
                                                     voter_data_to_use = voter_data_to_use,
                                                     weights_to_use = weights_to_use)
                                                 
        return voter_weights_dict

    def calc_all_group_cweights(self,
                                voter_data_to_use: VoterData = None,
                                group_masks_to_use: GroupRulesDict = None,
                                weights_to_use: Dict[str, float] = None):
        """ 
        Create a dictionary that calculates the current cweight of every group. 
        """ 
        if voter_data_to_use is None:
            voter_data_to_use =  self.current_voter_data
        if group_masks_to_use is None:
            group_masks_to_use = self.group_masks
        if weights_to_use is None:
            weights_to_use = self.current_credential_weights

        group_cweights = {}
        for group_name, group_mask in group_masks_to_use.items():
            group_cweight = self.calc_masked_cweight(voter_data = voter_data_to_use,
                                                     mask_to_use = group_mask,
                                                     weights_dict = weights_to_use)
            group_cweights[group_name] = group_cweight

        return group_cweights


    # TOOD: Test this function.
    def calc_scaling_factor_for_target_cweight(self, 
                        voter_data_to_use: VoterData = None,
                        group_name: str = None,
                        group_rules_to_use: GroupRulesDict = None, 
                        target_cweight: float = None) -> float:
        """
        Given a target_cweight, calculate the scaling_factor for a group. 
        """
        
        # Get the voter data and group rules. 
        if voter_data_to_use is None:
            voter_data_to_use = self.current_voter_data
        
        if group_rules_to_use is None:
            group_rules_to_use = self.group_rules 
        
        # Get the current group mask and curent group rule 
        current_group_mask = self.group_masks.get(group_name)
        current_group_rule = group_rules_to_use.get(group_name)
        
        # Figure out which credentials need to be reweighted, and which have all been reweighted
        credentials_to_reweight = current_group_rule.get("credentials_to_reweight")
        credentials_already_reweighted = [cred 
                                         for cred 
                                         in current_group_rule.get("credentials_to_sum") 
                                         if not (cred in credentials_to_reweight)
                                         ]

        # Calculate the established_group_cweight, corresponding to entries where the credential weights have been set previously. 
        if len(credentials_already_reweighted) > 0:
            established_group_mask = self.create_submask_by_creds(initial_mask = current_group_mask,
                                          cred_names = credentials_already_reweighted)
            established_group_cweight = self.calc_masked_cweight(voter_data = voter_data_to_use, 
                                                                mask_to_use = established_group_mask,
                                                                weights_dict = self.current_credential_weights)
        else: 
            established_group_cweight = 0

        if established_group_cweight > target_cweight:
            raise ValueError("Calculated a negative scaling value.")
        else:
            difference_in_cweight = target_cweight - established_group_cweight
            scale_creds_mask = self.create_submask_by_creds(initial_mask = current_group_mask,
                                                       cred_names = credentials_to_reweight)
            cweight_to_scale = self.calc_masked_cweight(voter_data = voter_data_to_use,
                                                        mask_to_use = scale_creds_mask,
                                                        weights_dict = self.current_credential_weights)
            scaling_factor = difference_in_cweight/cweight_to_scale
        
        return scaling_factor

    def reweighted_creds_by_scaling_factor(self,
                                           group_name: str = None,
                                           group_rules: GroupRulesDict = None,
                                           current_cred_weights = None,
                                           scaling_factor: float = None):
        """
        Reweight credentials, once the scaling factor is known. 
        """
        if current_cred_weights is None:
            current_cred_weights = deepcopy(self.current_credential_weights)

        if group_rules is None:
            group_rules = self.group_rules

        credentials_to_reweight = self.group_rules.get(group_name).get("credentials_to_reweight")

        reweighted_credentials = {}

        for credential in credentials_to_reweight:
            old_weight = current_cred_weights.get(credential)
            new_weight = old_weight * scaling_factor
            reweighted_credentials[credential] = new_weight

        return reweighted_credentials 


    
    def calc_new_cred_weights(self,
                             group_name: str,
                             group_rules: Dict,
                             target_cweight: float) -> Dict[str, float]:
        """
        Calculate the new weights for credentials in a group.

        This needs to be overridden in an implementation of the class. 
        """
        pass 

         
    def update_current_credential_weights(self,
                             cred_weights_to_update: Dict[str, float]) -> bool:
        """
        Add new credential weights to the current weights.
        """
        for name, weight in cred_weights_to_update.items():
            self.current_credential_weights[name] = weight

        return True, self.current_credential_weights

    def update_all_current_credential_weights(self) -> bool:
        """
        Update all current credential weights to achieve the desired group properties (if possible).

        This needs to be over-ridden by any subclass. 
        """
        pass 


    
    ################################
    ## End methods to re-weight  ##
    ################################ 


    



    