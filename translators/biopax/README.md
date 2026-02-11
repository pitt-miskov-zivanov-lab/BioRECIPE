# BioPAX-BioRECIPE Translator
# BioRECIPE Format

The BioRECIPE format, which stands for Biological system Representation for Evaluation, Curation, Interoperability, Preserving, and Execution, was specifically crafted to enhance the interaction between humans and machines in the creation, validation, assessment, curation, and expansion of executable models pertaining to intra- and intercellular signaling.

This format offers a user-friendly experience, allowing easy visualization and modification of model components by human users. Simultaneously, it remains machine-readable, facilitating processing by various model development and analysis tools. BioRECIPE demonstrates compatibility with multiple representation formats, machine readers, modeling tools, and databases commonly utilized in the field of systems biology.

For in-depth information on utilizing the BioRECIPE format, please refer to the [BioRECIPE Documentation](https://melody-biorecipe.readthedocs.io/en/latest/index.html).

## BioPAX
Biological Pathway Exchange ([BioPAX](https://www.biopax.org/)) is a standard language that aims to enable integration, exchange, visualization and analysis of biological pathway data. Specifically, BioPAX supports data exchange between pathway data groups and thus reduces the complexity of interchange between data formats by providing an accepted standard format for pathway data. It is an open and collaborative effort by the community of researchers, software developers, and institutions.


you can find the folder under this path /BioRECIPE/translators/biopax.

We currently only support the translation of BioPAX Level3. If you want to translate an BioPAX file with the format .owl/.xml to a BioRECIPE file with the format .xlsx, you can use script and run the following command.
```bash
# Model translation
python translate.py --input_file [BioPAX pathway filename] --output_file [BioRECIPE interaction filename] --biorecipe_type model

# intreactions list translation
python translate.py --input_file [BioPAX pathway filename] --output_file [BioRECIPE interaction filename] --biorecipe_type interaction
```

Programming access: We also support for translating BioPAX Level3 string to pandas DataFrame.

```python
from translators.biopax import translate

# BioPAX string access
# e.g. requesting from database
uri = 'http://bioregistry.io/reactome:R-HSA-8854521'

response = requests(
    ...
)

df = translate.biopax_to_biorecipeM(input_str=response.text)
```
