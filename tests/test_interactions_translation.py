from translators.interactions import api

biorecipeI_input = '../translators/interactions/example/MachineReadingOutput.xlsx'
cmuI_input = '../translators/interactions/example/PMC9653562-cmu-out.tsv'
biorecipeM_input = '../translators/interactions/example/Tcell_N3_PTEN2_bio.xlsx'
biorecipeM_output = '../translators/interactions/example/MachineReadingOuput_model.xlsx'
cmuI_output = '../translators/interactions/example/PMC9653562_interactions.xlsx'
biorecipeI_output = '../translators/interactions/example/Tcell_N3_PTEN2_interactions.xlsx'

# model and interactions files are in BioRECIPE format
def test_model_to_interactions():
    api.model_to_interactions(biorecipeM_input, biorecipeI_output)
def test_interactions_to_model():
    api.interactions_to_model(biorecipeI_input, biorecipeM_output)
def test_cmu_to_interactions():
    api.cmu_to_biorecipe(cmuI_input, cmuI_output)

def main():
    # test apis and examples of our interactions translator
    test_model_to_interactions()
    test_interactions_to_model()
    test_cmu_to_interactions()

if __name__ == "__main__":
    main()