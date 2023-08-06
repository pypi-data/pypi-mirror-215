from typing import List
import pandas as pd
from . import get_data

def get_disease_hierarchy(parent_disease: str) -> List[str]:
    """
    Retrieve the hierarchy of diseases based on the given parent disease.

    Args:
        parent_disease (str): The ID of the parent disease.

    Returns:
        List[str]: A list of disease IDs representing the hierarchy.

    Raises:
        Exception: If the parent disease is not found in the dataset.
    """
    disease_df = get_data('Diseases')
    disease_df['ParentIDs'].str.split('|').explode()

    hierarchy_df = disease_df\
        .assign(ParentIDs=disease_df['ParentIDs'].str.split('|')).explode('ParentIDs')

    levels = 3

    all_diseases = [parent_disease]
    current_level = hierarchy_df.loc[hierarchy_df['ParentIDs'] == parent_disease]
    for level in range(levels):
        children = list(current_level['DiseaseID'].unique())
        all_diseases.extend(children)
        next_level = hierarchy_df.loc[hierarchy_df['ParentIDs'].isin(children)]
        current_level = next_level

    return all_diseases
