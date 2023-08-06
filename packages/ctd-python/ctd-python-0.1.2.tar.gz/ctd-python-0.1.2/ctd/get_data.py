import os
import gzip
import shutil
import logging
import requests
from tqdm import tqdm
import pandas as pd

PACKAGE_DIR = os.path.dirname(__file__)
RAW_DATA_DIR = os.path.join(PACKAGE_DIR, 'unzipped_data')

from tqdm import tqdm

from tqdm import tqdm
import io

def download_resource(resource: str) -> str:
    url_dl_pattern = 'http://ctdbase.org/reports/{resource}.csv.gz'
    url = url_dl_pattern.format(resource=resource)

    logging.info('[download_resource]: downloading: %s', resource)
    local_filename = os.path.join(RAW_DATA_DIR, url.split('/')[-1])

    ## TODO - make this a config to refresh
    ## perhaps even add the date of the file created so we can dl new
    ## files when they come in
    if os.path.isfile(local_filename):
        return local_filename

    response = requests.get(url, stream=True)
    response.raise_for_status()
    total_size = int(response.headers.get('content-length', 0))
    block_size = 8192
    progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)

    with open(local_filename, 'wb') as f:
        with gzip.GzipFile(fileobj=response.raw, mode='rb') as gz_file:
            while True:
                chunk = gz_file.read(block_size)
                if not chunk:
                    break
                f.write(chunk)
                progress_bar.update(len(chunk))
    progress_bar.close()

    return local_filename


def get_data(resource: str) -> pd.DataFrame:
    """
    Fetch the data for a specific resource from the CTD database.

    Args:
        resource (str): The name of the resource.

    Returns:
        pd.DataFrame: The data as a pandas DataFrame.

    Raises:
        Exception: If the specified resource is not available.

    Notes:
        The available resources are:
        - GeneInteractionTypes
        - ChemicalPathwaysEnriched
        - GeneDisease
        - GenePathways
        - DiseasePathways
        - ChemocalPhenoTypeInteractions
        - Exposure Studies
        - Chemicals
        - Genes
        - ChemicalGeneInteractions
        - ChemicalDiseaseInteractions
        - Diseases
    """
    RESOURCES = {
        'GeneInteractionTypes': 'CTD_chem_gene_ixn_types',
        'ChemicalPathwaysEnriched': 'CTD_chem_pathways_enriched',
        'GeneDisease': 'CTD_genes_diseases',
        'GenePathways': 'CTD_genes_pathways',
        'DiseasePathways': 'CTD_diseases_pathways',
        'ChemocalPhenoTypeInteractions': 'CTD_pheno_term_ixns',
        'Exposure Studies': 'CTD_exposure_studies',
        'Chemicals': 'CTD_chemicals',
        'Genes': 'CTD_genes',
        'ChemicalGeneInteractions': 'CTD_chem_gene_ixns',
        'ChemicalDiseaseInteractions': 'CTD_chemicals_diseases',
        'Diseases': 'CTD_diseases'
    }

    resource_name = RESOURCES.get(resource)
    if not resource_name:
        raise Exception(f"The resource '{resource}' is not available. Please check https://ctdbase.org/downloads/ for available resources.")

    download_resource(resource_name)

    line_number = 27  # files have the same header, TODO need to make dynamic
    the_file = os.path.join(RAW_DATA_DIR, f"{resource_name}.csv")

    with open(the_file, 'r') as reader:
        for i, row in enumerate(reader):
            if i == line_number:
                header = row.replace("# ", "").split(",")

    df = pd.read_csv(the_file, skiprows=29, names=header)
    return df
