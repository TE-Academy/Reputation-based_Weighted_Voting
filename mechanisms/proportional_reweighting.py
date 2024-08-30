from typing import Callable, Dict, List
import pandas as pd
import copy

class ProportionalReweightingMechanism:
    def __init__(self, 
                 initial_voter_data: pd.DataFrame, 
                 new_credentials: Dict[str, Callable[[pd.Series], bool]], 
                 group_rules: Dict[str, Dict[str, object]], 
                 group_proportions: Dict[str, float],
                 initial_credential_weights: Dict[str, float]):
        self.initial_voter_data = initial_voter_data
        self.new_credentials = new_credentials
        self.group_rules = group_rules
        self.group_proportions = group_proportions
        self.initial_credential_weights = initial_credential_weights

        self.modified_voter_data = self.create_modified_voter_data()
        self.group_masks = self.process_group_rules_to_masks()
        self.current_credential_weights = {}
        
    def create_modified_voter_data(self) -> pd.DataFrame:
        # Create a deep copy of the initial voter data
        modified_voter_data = copy.deepcopy(self.initial_voter_data)
        
        # Iterate over the new_credentials dictionary and apply the functions
        for cred_name, func in self.new_credentials.items():
            # Apply the function to each row and create a new column
            modified_voter_data[cred_name] = modified_voter_data.apply(func, axis=1)
        
        return modified_voter_data

    def process_group_rules_to_masks(self) -> Dict[str, pd.DataFrame]:
        group_dataframes = {}

        # Iterate over each group in the group_rules dictionary
        for group_name, rules in self.group_rules.items():
            # Initialize a DataFrame filled with zeros, with the same index and columns as the initial data
            group_df = pd.DataFrame(0, index=self.initial_voter_data.index, columns=self.new_credentials.keys())

            # Apply the selection rule to identify relevant rows
            selected_rows = self.initial_voter_data.apply(rules['selection_rule'], axis=1)
            
            # Set the relevant cells to 1 for the selected rows and specified credentials
            for cred in rules['credentials_to_sum']:
                group_df.loc[selected_rows, cred] = 1
            
            # Store the resulting DataFrame in the dictionary
            group_dataframes[group_name] = group_df

        return group_dataframes

    # TODO: Look again at this logic. 

    ################################$
    ## Begin methods to re-weight  ##
    ################################$ 
    
    def calc_scaling_factor(self, 
                            group_name: str,
                            target_cweight: float) -> float:
        current_cweight = self.calc_group_cweight(voter_data = self.modified_voter_data,
                                                  group_name = group_name,
                                                  group_masks = self.group_masks,
                                                  weights_dict = self.current_credential_weights)
        scaling_factor = target_cweight/current_cweight

        return scaling_factor
    
    def calc_new_cred_weights(self,
                             group_name: str,
                             group_rules: Dict,
                             target_cweight: float) -> Dict[str, float]:
        scaling_factor = self.calc_scaling_factor(group_name = group_name, 
                                                  target_cweight = target_cweight)
        # TODO: Double-check this, but I think it's correct now. 
        reweighted_credentials = {}

        credentials_to_reweight_list = group_rules.get(group_name).get("credentials_to_reweight")

        for rule_name in credentials_to_reweight_list:
            initial_credential_weight = self.initial_credential_weights.get(rule_name)
            new_credential_weight = scaling_factor * initial_credential_weight
            reweighted_credentials[rule_name] = new_credential_weight

        return reweighted_credentials 




    def add_new_cred_weights(self,
                             cred_weights_to_add: Dict[str, float]) -> bool:
        disjoint_condition_check = not set(self.current_cred_weights.keys()).intersection(cred_weights_to_add.keys()) 
        msg_if_not_disjoint = "It appears a credential is being updated more than once."
        assert disjoint_condition_check, msg_if_not_disjoint
        
        self.current_cred_weights.update(cred_weights_to_add)
        return True
    
    def calc_target_cweights(self, 
                             group_proportions: Dict[str, float]):
        # Check to make sure that there is more than one group.
        correct_group_proportions_length_check = len(group_proportions) > 1
        incorrect_group_proportions_msg = "There must be more than one group."
        assert correct_group_proportions_length_check, incorrect_group_proportions_msg

        group_proportions_key_list = list(group_proportions.keys())
        group_proportions_values_list = list(group_proportions.values())
        base_group = group_proportions_key_list[0]
        base_value = group_proportions_values_list[0] 
        base_cweight = self.calc_group_cweight(group = base_group,
                                               group_masks = self.group_masks,
                                               weights = self.initial_cweights)

        

        #NOTE: Need to think through this a bit more, how to add this information?
            

        return True 
    
    def calc_group_cweight(self,
                            voter_data: pd.DataFrame,
                            group_name: str,
                            group_masks: Dict[str, pd.DataFrame],
                            weights_dict: Dict[str, float]):
        #TODO: We need to calculate the current group cweights based on the weights_dict
        masked_voter_data = group_masks.get(group_name) * voter_data
        weighted_masked_voter_info = masked_voter_data * pd.Series(weights_dict)
        group_cweight = weighted_masked_voter_info.sum().sum()
        return group_cweight
    
    def calc_current_voter_weights(self):
        """
        Return a dictionary of the voter weights, based on the current credential weights. 
        """

        # TODO: Write this code. 
    
    ################################
    ## End methods to re-weight  ##
    ################################ 
    
    def check_valid_masks(self, 
                          voter_data, 
                          group_masks):
        # TODO: Check that the masks, taken together, cover every cell exactly once.
        # NOTE: i.e Mutually Exclusive, Completely Exhaustive (a partition).
        pass 
        


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