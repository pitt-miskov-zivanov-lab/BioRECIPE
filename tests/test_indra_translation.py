import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), os.pardir, 'translators')))
from indra_engine.to_from import get_INDRAstmts_from_biorecipeI, get_biorecipeI_from_pmcids

biorecipe_input = 'interaction_lists/interaction_biorecipe.xlsx'
indra_output = 'indra/indra_stmts.json'

ids = 'pmcid/ids.csv'
outdir = 'interaction_lists/ids_biorecipe.xlsx'

test_files_rl_path = '../examples/'

def test_INDRAstmts_from_biorecipeI():

    get_INDRAstmts_from_biorecipeI(
    test_files_rl_path + biorecipe_input,
    test_files_rl_path + indra_output
    )

def test_biorecipeI_from_pmcids():

    get_biorecipeI_from_pmcids(
    infile=test_files_rl_path + ids,
    outdir=test_files_rl_path + outdir
    )

def main():
    test_INDRAstmts_from_biorecipeI()
    test_biorecipeI_from_pmcids()

if __name__ == "__main__":
    main()
