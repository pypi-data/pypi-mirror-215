## CTD Python

Pyhton interface to access data from The Comparative Toxicogenomics Database (CTD)

### install

```
pip3 install ctd-python
```

### import the package in order to pull the data

```
from ctd import get_data
```

## The package offers the following resources as DataFrames

- GeneInteractionTypes
- ChemicalPathwaysEnriched
- GeneDisease
- GenePathways
- DiseasePathways
- ChemocalPhenoTypeInteractions
- Chemicals
- Genes
- ChemicalGeneInteractions
- Chemicals
- Diseases

### Get the Gene Information for TNF
```
gene_df = get_data('Genes')
tnf_df = gene_df[gene_df['GeneSymbol'] == 'TNF']
```

### Get Chemical Interactions for TNF
```
chem_gene_df = get_data('ChemicalGeneInteractions')
tnf_chem_df = chem_gene_df[chem_gene_df['GeneSymbol'] == 'TNF']
```

### Get Disease Hierarchy for Parkinson Disease
```
child_diseases = get_disease_hierarchy('MESH:D010300')
```
