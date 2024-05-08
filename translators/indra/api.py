from .processor import INDRA
from .run_indra_pmcids_biorecipe import parse_pmc

def biorecipe_to_indra(input, output):
    indra = INDRA()
    indra.biorecipeI_stmts(input, output)
    print("Finished: {0}".format(output))

