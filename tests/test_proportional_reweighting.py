# Tests for the proportional re-weighting mechanism. 


###################################
## Begin template  for testing.  ##
###################################

#TODO: Add the template for testing here. 

###################################
## End  template  for testing.   ##
###################################

import pytest
import pandas as pd
from mechanisms.proportional_reweighting import ProportionalReweightingMechanism

@pytest.fixture
def setup_proportional_reweighting_mechanism():
    # Setup initial voter data
    initial_voter_data = pd.DataFrame({
        'Voter1': [1, 0, 1],
        'Voter2': [0, 1, 1],
        'Voter3': [1, 1, 0]
    })

    # Setup new credentials
    new_credentials = {
        "cred1": lambda row: row.sum() > 1,
        "cred2": lambda row: row['Voter1'] == 1
    }

    # Setup group rules
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

    # Setup group proportions
    group_proportions = {
        "group1": 0.6,
        "group2": 0.4
    }

    # Setup initial credential weights
    initial_credential_weights = {
        "cred1": 1.5,
        "cred2": 2.0
    }

    # Create the ProportionalReweightingMechanism object
    pr_mechanism = ProportionalReweightingMechanism(
        initial_voter_data=initial_voter_data,
        new_credentials=new_credentials,
        group_rules=group_rules,
        group_proportions=group_proportions,
        initial_credential_weights=initial_credential_weights
    )

    return pr_mechanism

def test_create_modified_voter_data(setup_proportional_reweighting_mechanism):
    pr_mechanism = setup_proportional_reweighting_mechanism
    
    # Expected result
    expected_result = pd.DataFrame({
        'Voter1': [1, 0, 1],
        'Voter2': [0, 1, 1],
        'Voter3': [1, 1, 0],
        'cred1': [True, False, True],
        'cred2': [True, False, True]
    })
    
    # Actual result
    actual_result = pr_mechanism.create_modified_voter_data()
    
    # Condition check
    condition_check = expected_result.equals(actual_result)
    condition_not_met_msg = f"Expected to see {expected_result}, but got {actual_result}."
    
    assert condition_check, condition_not_met_msg

def test_process_group_rules_to_masks(setup_proportional_reweighting_mechanism):
    pr_mechanism = setup_proportional_reweighting_mechanism
    
    # Expected result
    expected_result = {
        "group1": pd.DataFrame({
            'cred1': [1, 0, 1],
            'cred2': [1, 0, 1]
        }, index=[0, 1, 2]),
        "group2": pd.DataFrame({
            'cred1': [0, 1, 1],
            'cred2': [0, 1, 1]
        }, index=[0, 1, 2])
    }
    
    # Actual result
    actual_result = pr_mechanism.process_group_rules_to_masks()
    
    # Condition check
    condition_check = all(expected_result[group].equals(actual_result[group]) for group in expected_result)
    condition_not_met_msg = f"Expected to see {expected_result}, but got {actual_result}."
    
    assert condition_check, condition_not_met_msg

# Additional tests for other methods can be added similarly...

if __name__ == "__main__":
    pytest.main()
