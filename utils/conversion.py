from typing import Dict
import pandas as pd


def voter_cred_df_to_dict(voter_cred_df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
    voter_cred_dict = {}
    for voter in list(voter_cred_df.index):
        voter_cred_dict[voter] = {}
        for cred in list(voter_cred_df.columns):
            voter_cred_dict[voter][cred] = voter_cred_df.at[voter,cred]
    return voter_cred_dict

