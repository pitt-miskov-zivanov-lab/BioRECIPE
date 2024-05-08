from .processor import SBMLQual
from .run_sbmlqual_biorecipe import SBMLQualMath

def biorecipeM_to_sbmlqual(input, output):
    sbml_qual = SBMLQual()
    sbml_qual.to_sbmlqual(input, output)
    print("Finished: {0}".format(output))

def biorecipeI_to_sbmlqual(input, output):
    sbml_qual = SBMLQual()
    sbml_qual.to_sbmlqual_interactions(input, output)
    print("Finished: {0}".format(output))

def sbmlqual_to_biorecipe(input, output):
    sbmlqual_math = SBMLQualMath()
    sbmlqual_math.sbmlqual_biorecipe(input, output)
    print("Finished: {0}".format(output))


