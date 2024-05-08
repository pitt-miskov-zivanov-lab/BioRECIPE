from translators.sbmlqual import api

sbmlqual_input = '../examples/sbmlqual/Tcell_differentiation.sbml'
biorecipe_output = '../examples/models/Tcell_differentiation.xlsx'

# M: model, I: interaction lists
biorecipeM_input = '../examples/models/BooleanTcell_biorecipe.xlsx'
biorecipeI_input = '../examples/interaction_lists/Reading_biorecipe.xlsx'
sbmlqualM_output = '../examples/sbmlqual/BooleanTcell_sbmlqual.xml'
sbmlqualI_output ='../examples/sbmlqual/Reading_sbmlqual.xml'

def test_biorecipe_to_sbmlqual():
    api.biorecipeM_to_sbmlqual(biorecipeM_input, sbmlqualM_output)
    api.biorecipeI_to_sbmlqual(biorecipeI_input, sbmlqualI_output)

def test_sbmlqual_to_biorecipe():
    api.sbmlqual_to_biorecipe(sbmlqual_input, biorecipe_output)

def main():
    # test apis and examples of our sbmlqual translator
    test_biorecipe_to_sbmlqual()
    test_sbmlqual_to_biorecipe()

if __name__ == "__main__":
    main()