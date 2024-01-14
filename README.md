# BioRECIPE Package README
The standard format of model spreadsheet used by MeLoDy Lab. For more details, please follow the official documentation webpage of BioRECIPE format   

https://melody-biorecipe.readthedocs.io/en/latest/index.html.

### SBML translator

To translate files in SBML format to BioRECIPE, you will need to use CellDesigner to convert the pure SBML to CellDesigner extended SBML. 

```python
python src/run_sbml_biorecipe.py -i [SBML] -o [BioRECEIPE]
```

Translate SBMLQual to BioRECIPE:

```
python src/run_sbmlqual_biorecipe.py -i [SBMLQual] -o [BioRECIPE]
```

