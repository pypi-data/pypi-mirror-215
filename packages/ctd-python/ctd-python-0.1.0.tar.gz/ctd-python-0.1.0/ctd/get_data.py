import os
import gzip
import shutil
import logging
import requests
import pandas as pd

PACKAGE_DIR = os.path.dirname(__file__)
ZIPPED_DATA_DIR = os.path.join(PACKAGE_DIR, 'zipped_data')
UNZIPPED_DATA_DIR = os.path.join(PACKAGE_DIR, 'unzipped_data')

def download_resource(resource: str) -> str:

    url_dl_pattern = 'http://ctdbase.org/reports/{resource}.csv.gz'
    url = url_dl_pattern.format(resource=resource)

    logging.info('[download_resource]: downloading: %s', resource)
    local_filename = os.path.join(ZIPPED_DATA_DIR, url.split('/')[-1])
    unzipped_filename = os.path.join(UNZIPPED_DATA_DIR, url.split('/')[-1].replace('.gz', ''))

    if os.path.isfile(unzipped_filename):
        return

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    with gzip.open(local_filename, 'rb') as f_in:
        with open(unzipped_filename, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    return local_filename

def get_data(resource: str) -> pd.DataFrame:
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
        'Chemicals': 'CTD_chemicals_diseases',
        'Diseases': 'CTD_diseases'
    }

    resource_name = RESOURCES.get(resource)
    if not resource_name:
        raise Exception(f"The resource '{resource}' is not available. Please check https://ctdbase.org/downloads/ for available resources.")

    download_resource(resource_name)

    line_number = 27  # All the files have the same header
    the_file = os.path.join(UNZIPPED_DATA_DIR, f"{resource_name}.csv")

    with open(the_file, 'r') as reader:
        for i, row in enumerate(reader):
            if i == line_number:
                header = row.replace("# ", "").split(",")

    df = pd.read_csv(the_file, skiprows=29, names=header)
    return df
