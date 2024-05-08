from .processor import SIF

def biorecipeM_to_sif(input, output):
    sbml_qual = SIF()
    sbml_qual.biorecipeM_sif(input, output)
    print("Finished: {0}".format(output))

def biorecipeI_to_sif(input, output):
    sbml_qual = SIF()
    sbml_qual.biorecipeI_sif(input, output)
    print("Finished: {0}".format(output))

def sif_to_biorecipeI(input, output):
    sbml_qual = SIF()
    sbml_qual.sif_biorecipeI(input, output)
    print("Finished: {0}".format(output))