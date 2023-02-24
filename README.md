# BioRECIPES
The standard format of model spreadsheet used by MeLoDy Lab

##### Translation from CellDesigner to BioRECIPES

```python
import celldesigner2qual as casq

casq.map_to_model("examples/map_mapk.xml", "examples/map_mapk_biorecipes.xlsx")
```

--input: (CellDesigner)[ https://www.celldesigner.org/models.html ] xml file stored in examples/ folder

--output: BioRECIPES spreadsheet 
