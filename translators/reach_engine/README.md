# REACH-BioRECIPE Translator

This repository contains a translator to convert REACH output (multiple json files per paper) into our BioRECIPE interaction lists file. 

### 1. Preprocessing json files from REACH 

To translate all the biomedical relations extracted by the REACH reader, the first step is to summarize individual json files in REACH fries data representation to a big json file.

Run the script with the following command:

```
python reach_fries_to_smy.py -i input/usr_reach_fries_1 -o input/usr_reach_fries_1_summary.json
```

### 2. Convert processed json file to BioRECIPE interaction lists

Run the script with the following command:

```bash
python smy_to_rcp.py -i input/usr_reach_fries_1_summary.json -o output/usr_reach_fries_1_interactions.xlsx
```

