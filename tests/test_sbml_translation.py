import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), os.pardir, 'translators')))
from sbml.sbml_to_biorecipe import get_biorecipeM_from_sbml
from sbml.biorecipe_to_sbml import get_sbml_from_biorecipeI

sbml_input = 'sbml/map_mapk.xml'
biorecipe_output = 'models/map_mapk.xlsx'

biorecipe_input = 'interaction_lists/reading_biorecipe.xlsx'
sbml_output = 'sbml/reading_sbml.xml'

test_files_rl_path = '../examples/'

def test_biorecipeM_from_sbml():

    get_biorecipeM_from_sbml(
    test_files_rl_path + sbml_input,
    test_files_rl_path + biorecipe_output
    )

def test_sbml_from_biorecipe():

    get_sbml_from_biorecipeI(
    test_files_rl_path + biorecipe_input,
    test_files_rl_path + sbml_output
    )

def main():
    test_biorecipeM_from_sbml()
    test_sbml_from_biorecipe()

if __name__ == "__main__":
    main()
