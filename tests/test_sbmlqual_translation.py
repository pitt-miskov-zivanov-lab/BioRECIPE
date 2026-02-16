import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), os.pardir, 'translators')))
from sbmlqual.sbmlqual_to_biorecipe import get_biorecipeM_from_sbmlqual
from sbmlqual.biorecipe_to_sbmlqual import get_sbmlqual_from_biorecipeM, get_sbmlqual_from_biorecipeI

sbmlqual_input = 'sbmlqual/Tcell_differentiation.sbml'
biorecipe_output = 'models/Tcell_differentiation.xlsx'

# M: model, I: interaction lists
biorecipeM_input = 'models/BooleanTcell_biorecipe.xlsx'
sbmlqualM_output = 'sbmlqual/BooleanTcell_sbmlqual.xml'

biorecipeI_input = 'interaction_lists/Reading_biorecipe.xlsx'
sbmlqualI_output ='sbmlqual/Reading_sbmlqual.xml'

test_files_rl_path = '../examples/'

def test_sbmlqual_from_biorecipeM():

    get_sbmlqual_from_biorecipeM(
    test_files_rl_path + biorecipeM_input,
    test_files_rl_path + sbmlqualM_output
    )

def test_sbmlqual_from_biorecipeI():

    get_sbmlqual_from_biorecipeI(
    test_files_rl_path + biorecipeI_input,
    test_files_rl_path + sbmlqualI_output
    )

def test_biorecipeM_from_sbmlqual():

    get_biorecipeM_from_sbmlqual(
    input_filename=test_files_rl_path + sbmlqual_input,
    output_filename=test_files_rl_path + biorecipe_output
    )

def main():
    test_sbmlqual_from_biorecipeM()
    test_sbmlqual_from_biorecipeI()
    test_biorecipeM_from_sbmlqual()

if __name__ == "__main__":
    main()
