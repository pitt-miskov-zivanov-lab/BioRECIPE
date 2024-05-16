import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), os.pardir, 'translators')))
from within_biorecipe.md_and_int import get_model_from_interactions, get_interactions_from_model, get_biorecipeI_from_reach_tab

biorecipeI_input = 'interaction_lists/MachineReadingOutput.xlsx'
biorecipeM_output = 'models/MachineReadingOuput_model.xlsx'

biorecipeM_input = 'models/Tcell_N3_PTEN2_bio.xlsx'
biorecipeI_output = 'interaction_lists/Tcell_N3_PTEN2_interactions.xlsx'

reach_tab_input = 'interaction_lists/PMC9653562_cmu_out.tsv'
reach_tab_output = 'interaction_lists/PMC9653562_interactions.xlsx'

test_files_rl_path = '../examples/'

# model and interactions files are in BioRECIPE format
def test_model_from_interactions():

    get_model_from_interactions(
    test_files_rl_path + biorecipeI_input,
    test_files_rl_path + biorecipeM_output
    )

def test_interactions_from_model():

    get_interactions_from_model(
    test_files_rl_path + biorecipeM_input,
    test_files_rl_path + biorecipeI_output
    )

def test_biorecipeI_from_reach_tab():

    get_biorecipeI_from_reach_tab(
    test_files_rl_path + reach_tab_input,
    test_files_rl_path + reach_tab_output
    )

def main():
    # test apis and examples of translator
    test_model_from_interactions()
    test_interactions_from_model()
    test_biorecipeI_from_reach_tab()

if __name__ == "__main__":
    main()
