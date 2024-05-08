# Interactions translator
This script serve for three translation, which are from interaction to model file, from model to interactions file, and from CMU tabular output to BioRECIPE interactions list.
## BioRECIPE interactions list -> BioRECIPE model file
```bash
  python run_BioRECIPE.py -i [interactions] --input_file [BioRECIPE interaction file path] --output_file [output filename]
```
## BioRECIPE model file -> Interactions list
```bash
  python run_BioRECIPE.py -i [model] --input_file [BioRECIPE model tabular file path] --output_file [output filename]
```

## REACH tabular reading output -> BioRECIPE interactions list
We also support the translation of tabular file from [REACH](https://github.com/clulab/reach/wiki/Supported-Output-Formats) reading output.
```bash
  python run_BioRECIPE.py -i [cmu] --input_file [cmu tsv file path] --output_file [output filename]
```

## Requirements
python>=3.6, pandas
