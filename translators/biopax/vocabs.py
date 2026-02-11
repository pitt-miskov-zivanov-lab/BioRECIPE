

# Entity type in BioPAX

BPTYPE2BIORECIPE = {
    'Protein': 'protein',
    'Complex': 'protein complex',
    'SmallMolecule': 'chemical',
    'DNA': 'gene',
    'DNARegion': 'other',
    'RNA': 'rna',
    'RNARegion': 'other'
}

# Entity reference primary database 
PRIME_DB = [
    'uniprot',
    'chebi', 
    'pubchem',
    'ensembl',
    'refseq', 
    'hgnc',
    'go',
    'gene ontology',

]

# Interaction type for control interactions in BioPAX
CONTROLTYPE_VOCABULARY = [
    'activation',
    'inhibition',
    'inhibition-allosteric',
    'inhibition-competitive',
    'inhibition-irreversible',
    'inhibition-noncompetitive',
    'inhibition-other',
    'inhibition-uncompetitive',
    'activation-nonallosteric',
    'activation-allosteric'
]

CONTROLTYPE2SIGN = {
    "activation": "positive", 
    "activation-allosteric": 'positive',
    "activation-nonallosteric": 'positive',
    "inhibition": 'negative', 
    "inhibition-allosteric": 'negative', 
    "inhibition-competitive": 'negative', 
    "inhibition-irreversible": 'negative', 
    "inhibition-noncompetitive": 'negative', 
    "inhibition-other": 'negative', 
    "inhibition-uncompetitive": 'negative', 
}
