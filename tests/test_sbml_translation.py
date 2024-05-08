from translators.sbml import api

sbml_input = '../examples/sbml/map_mapk.xml'
biorecipe_output = '../examples/models/map_mapk.xlsx'

biorecipe_input = '../examples/interaction_lists/Reading_biorecipe.xlsx'
sbml_output = '../examples/sbml/reading_sbml.xml'
def test_biorecipe_to_sbml():
    api.biorecipe_to_sbml(biorecipe_input, sbml_output)

def test_sbml_to_biorecipe():
    api.sbml_to_biorecipe(sbml_input, biorecipe_output)

def main():
    # test apis and examples of our sbml translator
    test_sbml_to_biorecipe()
    test_biorecipe_to_sbml()

if __name__ == "__main__":
    main()