from translators.SIF import api

biorecipeM_input = '../examples/models/BooleanTcell_biorecipe.xlsx'
biorecipeI_input = '../examples/interaction_lists/Reading_biorecipe.xlsx'
sifM_output = '../examples/sif/BooleanTcell_biorecipe.sif'
sifI_output = '../examples/sif/Reading_biorecipe.sif'

sif_input = '../examples/sif/gbm_ints.sif'
biorecipe_output = '../examples/interaction_lists/gbm_ints.xlsx'

def test_biorecipeM_to_sif():
    api.biorecipeM_to_sif(biorecipeM_input, sifM_output)

def test_biorecipeI_to_sif():
    api.biorecipeI_to_sif(biorecipeI_input, sifI_output)

def test_sif_to_biorecipeI():
    api.sif_to_biorecipeI(sif_input, biorecipe_output)

def main():
    # test apis and examples of our sif translator
    test_biorecipeM_to_sif()
    test_biorecipeI_to_sif()
    test_sif_to_biorecipeI()

if __name__ == "__main__":
    main()