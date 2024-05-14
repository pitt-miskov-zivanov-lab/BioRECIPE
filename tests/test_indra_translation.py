import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), os.pardir)))
from translators.indra_engine.to_from import *

biorecipe_input = 'interaction_lists/interaction_biorecipe.xlsx'
indra_output = 'indra/indra_stmts.json'

ids = 'pmcid/ids.csv'
outdir = 'interaction_lists/ids_biorecipe.xlsx'

test_files_rl_path = '../examples/'

def test_biorecipe_to_indra():

    get_INDRAstmts_from_biorecipeI(
    test_files_rl_path + biorecipe_input,
    test_files_rl_path + indra_output
    )

def test_indra_pmcids_to_biorecipe():

    get_biorecipeI_from_pmcids(
    test_files_rl_path + ids,
    test_files_rl_path + outdir
    )

def main():
    test_biorecipe_to_indra()
    test_indra_pmcids_to_biorecipe()

if __name__ == "__main__":
    main()
