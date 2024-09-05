from typing import Dict
import pandas as pd


def convert_voter_cred_df_to_dict(voter_cred_df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
    """
    Converts a DataFrame of voter credentials to a DataFrame. 
    """
    voter_cred_dict = {}
    for voter in list(voter_cred_df.index):
        voter_cred_dict[voter] = {}
        for cred in list(voter_cred_df.columns):
            voter_cred_dict[voter][cred] = voter_cred_df.at[voter,cred]
    return voter_cred_dict

def convert_voter_weights_dict_to_weights(voter_weights_dict: Dict[str, Dict[str, float]]):
    """ 
    Converts a voter weight dictionary where entries look like {"voter_name": {"weight": 100} } to one where entries look like {"voter_name": 100}
    """
    simplified_weights_dict = {voter_name: voter_info.get("weight") 
                    for voter_name, voter_info in voter_weights_dict.items()
                    }
    return simplified_weights_dict


