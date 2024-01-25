# SBML-BioRECIPE Translator
# BioRECIPE Format

The BioRECIPE format, which stands for Biological system Representation for Evaluation, Curation, Interoperability, Preserving, and Execution, was specifically crafted to enhance the interaction between humans and machines in the creation, validation, assessment, curation, and expansion of executable models pertaining to intra- and intercellular signaling.

This format offers a user-friendly experience, allowing easy visualization and modification of model components by human users. Simultaneously, it remains machine-readable, facilitating processing by various model development and analysis tools. BioRECIPE demonstrates compatibility with multiple representation formats, machine readers, modeling tools, and databases commonly utilized in the field of systems biology.

For in-depth information on utilizing the BioRECIPE format, please refer to the [BioRECIPE Documentation](https://melody-biorecipe.readthedocs.io/en/latest/index.html).

## SBML
SBML stands for Systems Biology Markup Language. It is a computer-readable format used to represent models of biological processes. SBML is designed to facilitate the exchange of computational models in systems biology, allowing researchers to share and collaborate on models of biological systems. This markup language provides a standardized way to represent mathematical models of biological processes, making it easier for scientists to simulate and analyze complex biological systems. SBML is widely used in the field of computational biology and systems biology for model representation and exchange.

One of the formats that this tool can translate to it to BioRECIPE is called SBL. 
you can find the folder under this path /BioRECIPE/translators/sbml.

If you want to translate an SBML file with the format .xml to a BioRECIPE file with the format .xlsx, you can use run_sbml_biorecipe.py script and run the following command. 
```bash
python run_sbml_biorecipe.py -i [PATH_TO_SBML_FILE] -o [PATH_TO_BIORECIPE_FILE]
```
and If you want to translate a BioRECIPE file with the format .xlsx to an SBML file with the format .xml, you can use run_biorecipe_sbml.py script and run the following command. 
```bash
python run_sbml_biorecipe.py -i [PATH_TO_BIORECIPE_FILE] -o [PATH_TO_SBML_FILE]
```
#### note: You need to have python version 3.8, 3.7 or 3.6 
