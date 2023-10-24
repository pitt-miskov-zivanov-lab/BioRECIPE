# BioRECIPES
The standard format of model spreadsheet used by MeLoDy Lab

##### Translation from SBML to BioRECEIPES:

1. First, parse the SBML through CellDesigner software
2. After you get the converted CellDesigner model file, run the following command: 

```python
python run_sbml_biorecipe.py -i [CellDesigner filename] -o [BioRECEIPE filename]
```

--input: Converted [CellDesigner](https://www.celldesigner.org/models.html) xml file stored in examples/ folder

--output: BioRECIPES spreadsheet 
