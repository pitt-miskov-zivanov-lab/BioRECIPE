# SBMLQual-BioRECIPE Translator

## BioRECIPE Format

The BioRECIPE format, which stands for Biological system Representation for Evaluation, Curation, Interoperability, Preserving, and Execution, was specifically crafted to enhance the interaction between humans and machines in the creation, validation, assessment, curation, and expansion of executable models pertaining to intra- and intercellular signaling.

This format offers a user-friendly experience, allowing easy visualization and modification of model components by human users. Simultaneously, it remains machine-readable, facilitating processing by various model development and analysis tools. BioRECIPE demonstrates compatibility with multiple representation formats, machine readers, modeling tools, and databases commonly utilized in the field of systems biology.

For in-depth information on utilizing the BioRECIPE format, please refer to the [BioRECIPE Documentation](https://melody-biorecipe.readthedocs.io/en/latest/index.html).

## SBMLQual

"SBMLQual" refers to the Qualitative Models extension of the Systems Biology Markup Language (SBML). SBML is a standard for representing computational models in systems biology, and it provides a way to exchange models between different software tools.

If you want to translate a SBMLQual file with the format .sbml to a BioRECIPE file, you can use run_sbmlqual_biorecipe.py script and run the following command.
```bash
python run_sbmlqual_biorecipe.py -i [SBMLQual] -o [BioRECIPE]
```
Both BioRECIPE model and interaction lists can be translated into SBMLQual, you can run_biorecipe_sbmlqual.py script and run the following commands:

1. From BioRECIPE model to SBMLQual

```
python run_biorecipe_sbmlqual.py -i model ..\..\examples\models\BooleanTcell_biorecipe.xlsx  ..\..\examples\sbmlqual\BooleanTcell_sbmlqual.xml
```

2. From BioRECIPE interaction lists to SBMLQual

```
python run_biorecipe_sbmlqual.py -i interactions ..\..\examples\interaction_lists\Reading_biorecipe.xlsx ..\..\examples\sbmlqual\Reading_sbmlqual.xml
```

#### note: You need to have python version 3.8, 3.7 or 3.6 

