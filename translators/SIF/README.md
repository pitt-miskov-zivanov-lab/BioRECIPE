# SIF-BioRECIPE Translator
## BioRECIPE Format

The BioRECIPE format, which stands for Biological system Representation for Evaluation, Curation, Interoperability, Preserving, and Execution, was specifically crafted to enhance the interaction between humans and machines in the creation, validation, assessment, curation, and expansion of executable models pertaining to intra- and intercellular signaling.

This format offers a user-friendly experience, allowing easy visualization and modification of model components by human users. Simultaneously, it remains machine-readable, facilitating processing by various model development and analysis tools. BioRECIPE demonstrates compatibility with multiple representation formats, machine readers, modeling tools, and databases commonly utilized in the field of systems biology.

For in-depth information on utilizing the BioRECIPE format, please refer to the [BioRECIPE Documentation](https://melody-biorecipe.readthedocs.io/en/latest/index.html).

## SIF
In network analysis or social network research, a SIF file is a format used to represent graph data that describes social interactions. It typically contains information about relationships between entities, such as nodes and edges in a graph.

1) From BioRECIPE model to SIF: 

   ```
   python to_from.py -i model --input_file input/BooleanTcell_biorecipe.xlsx --output_file output/BooleanTcell_biorecipe.sif
   ```

2) From BioRECIPE interaction lists to SIF:

    ```
    python to_from.py -i interactions --input_file input/Reading_biorecipe.xlsx --output_file output/Reading_biorecipe.sif
    
    ```
    
3) From SIF to BioRECIPE interaction lists:

    ```
    python to_from.py -i sif --input_file input/pc-mdm2-network.sif.txt --output_file output/mdm2.xlsx
    
    ```
#### note: You need to have python version 3.8, 3.7 or 3.6
