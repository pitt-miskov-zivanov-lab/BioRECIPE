import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), os.pardir, 'translators')))
from sif.to_from import get_sif_from_biorecipeM, get_sif_from_biorecipeI, get_biorecipeI_from_sif

biorecipeM_input = 'models/BooleanTcell_biorecipe.xlsx'
sifM_output = 'sif/BooleanTcell_biorecipe.sif'

biorecipeI_input = 'interaction_lists/reading_biorecipe.xlsx'
sifI_output = 'sif/reading_biorecipe.sif'

sif_input = 'sif/gbm_ints.sif'
biorecipe_output = 'interaction_lists/gbm_ints.xlsx'

test_files_rl_path = '../examples/'

def test_sif_from_biorecipeM():

    get_sif_from_biorecipeM(
    test_files_rl_path + biorecipeM_input,
    test_files_rl_path + sifM_output
    )

def test_sif_from_biorecipeI():

    get_sif_from_biorecipeI(
    test_files_rl_path + biorecipeI_input,
    test_files_rl_path + sifI_output
    )

def test_biorecipeI_from_sif():

    get_biorecipeI_from_sif(
    test_files_rl_path + sif_input,
    test_files_rl_path + biorecipe_output
    )

def main():
    test_sif_from_biorecipeM()
    test_sif_from_biorecipeI()
    test_biorecipeI_from_sif()

if __name__ == "__main__":
    main()
