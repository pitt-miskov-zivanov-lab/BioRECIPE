from .processor import write_sbml
from .celldesigner2qual import map_to_model

def sbml_to_biorecipe(input, output):
    map_to_model(input, output)

def biorecipe_to_sbml(input, output):
    write_sbml(input, output)
    print("Finished: {0}".format(output))
