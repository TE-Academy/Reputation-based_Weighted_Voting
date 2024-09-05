from typing import Callable, List, Literal, Dict, TypedDict
import pandas as pd

Credential = str
GroupName = str

VoterData = pd.DataFrame

class GroupRule(TypedDict):
    selection_rule: Callable[pd.Series, bool]
    credentials_to_sum: List[str]
    credentials_to_reweight: List[str]

GroupRulesDict = Dict[str, GroupRule]

GroupMask = pd.DataFrame
GroupMasksDict = Dict[str, GroupMask]

NewCredentialRule = Callable[pd.Series, Literal[0,1]]
NewCredentialRulesDict = Dict[Credential, NewCredentialRule]

CredentialWeightRule = Dict[Credential, float]


