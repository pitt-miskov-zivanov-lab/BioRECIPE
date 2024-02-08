# Translation

## Description of files

- `translator_wm.py` - world modelers translation
- `interactions.py` - functions for processing interactions and reading from files (preliminaries for a separate class)
- `model.py` - functions for processing models and reading from files (preliminaries for a separate class)
- `translate_INDRAreach.py` - used to automatically read multiple files through REACH and assemble them into a combined reading file for use of model assembly
- `Reading Output Translator - Windowed.py`
    1. Open `Reading Output Translator - Windowed.py` in a Python editor (IDLE) and then run the program (F5, or press Run -> Run Module).
        - Occasionally, an error occurs if this script is opened by the "Python" program instead. If this occurs, open the IDLE (Python 3.5) editor and then open the `Reading Output Translator - Windowed.py` script, ensuring that the script `translatorFunctions.py` is in the same folder. 
        - Update script to run from the Terminal
    2. When the script runs, a screen will appear prompting the user to choose between selecting a single file for translation or a folder full of MITRE files. Select the appropriate option. 
    3. A file dialog appears. Select the file you wish to translate. 
    4. The window will alert the user that the translation is complete. The Python shell window (running in the background) will display any errors or details related to the translation. 
    5. If a FRIES file was translated, the user will be asked whether or not they wish to link an appropriate FRIES "entity-mention" file, which will allow additional details (such as element types and IDs) to be included in the translated file. If this is undesired or no such file exists, simply select "Save Output". 
    6. If a MITRE file/folder was translated, the option to save the output will appear. Click this to save as a spreadsheet (.csv). 
    7. After saving the option to translate additional files will appear, as well as the option to quit the program.
- TODO: `translateMultipleFRIES.py`
- TODO: `translatorFunctions.py` - also why are there two copies
- TODO: note from Bryce: Sometimes an element is clearly a protein family (bracket notation on components), but no type or database/element IDs are listed

## Usage

- `model.py`
~~~
usage: model.py [-h] [--output_format {dyse,json,edges,sauce}]
                input_file output_file

Process model files/objects and convert among formats.

positional arguments:
  input_file            Input model file name
  output_file           Output model file name

optional arguments:
  -h, --help            show this help message and exit
  --output_format {dyse,json,edges,sauce}, -o {dyse,json,edges,sauce}
                        Output file format 
                        	 dyse (default): DySE model tabular format 
                        	 json: json format 
                        	 edges: element-regulator-interaction triplets 
                        	 sauce: CRA json format for SAUCE analysis 
~~~

- `interactions.py`
~~~
usage: interactions.py [-h] [--model_file MODEL_FILE]
                       [--output_format {ic,schema,mitre,bio}] [--compare]
                       [--score_threshold SCORE_THRESHOLD] [--protein_only]
                       input_files output_file

Process interaction files/objects and convert among formats.

positional arguments:
  input_files           interactions in tabular format. 
                        can be a directory of files or multiple comma-separated names. 
                        supported file formats: excel (SCHEMA or PosReg/NegReg format), csv (IC output), dms (IC output)
  output_file           Output file name

optional arguments:
  -h, --help            show this help message and exit
  --model_file MODEL_FILE, -m MODEL_FILE
                        model file to map element and variable names
  --output_format {ic,schema,mitre,bio}, -o {ic,schema,mitre,bio}
                        format of interactions output 
                        	 ic (default): same format as interaction classifier output, compatible with extension 
                        	 schema: all DySE column names (Element, Regulator and attributes) 
                        	 mitre: abbreviated MITRE tabular format 
                        	 bio: PosReg NegReg column format (for input to interaction classifier)
  --compare, -c         Keep file index to compare interactions among files
  --score_threshold SCORE_THRESHOLD, -s SCORE_THRESHOLD
                        threshold score to filter interactions
  --protein_only, -p    use only protein-protein interactions
~~~

- `translator_wm.py`
~~~
usage: translator_wm.py [-h] input_file output_file {text,sofia,eidos,bbn}

Translate automated reading output into standard format (for DySE model assembly or extension).

positional arguments:
  input_file            automated reading output to convert to standard format
  output_file           path and name of output file to save converted reading
  {text,sofia,eidos,bbn}
                        format of automated reading 
                        text: plain text, translate using eidos and indra 
                        sofia: tabular output from SOFIA reader 
                        eidos: json output from the eidos parser 
                        bbn: json-ld output from BBN's reader

optional arguments:
  -h, --help            show this help message and exit
~~~

- `translate_INDRAreach.py`
~~~
Required files and software:
  -This file runs using INDRA, which can be downloaded from the [INDRA website](http://indra.readthedocs.io/en/latest/installation.html)
  -You also need a translator file to ground the entity names used in INDRA to match the entity in the entity section of the JSON file
    - this file must be named `translator.csv` (it must be a comma separated file)
    - the first column of the file must be the entity names as they're found in INDRA, the second column is the grounded version of the entity

usage: winpty python translate_INDRAreach.py filelist PMC append outfile

positional arguments:
  filelist          This can be given as a list of PMC numbers (without quotations), a `.csv` file containing a column of evidence statements, or a `.csv` file containing a column of PMC numbers. 
  PMC               Here you specify the format of your `filelist`. Acceptable input is `list`, `evidence`, or `csv`
  append            Boolean value determining if output is added to an existing file or created in new file
  outfile           name of output file reading will be written to; must have format `.csv`

Example of execution:
  > winpty python /c/USers/Casey/framework/Translation/translate_INDRAreach.py [4936323,4513933,4171619,4896000] list False test_reading.csv

Description of translator output:
  - INDRA output
      - from INDRA, you get an NXML and JSON file for each PMC ID (the JSON file is overwritten for each new PMC number)
  - reading output
      - this is the output that is written into `otufile`
  - command line output
      - after the code has finished running, the command line will report the lines of the reading code which have improperly defined entities

Post-translation editing:
  For now, some entities and interactions are improperly defined, and will be noted in the output message of the code
  You will need to manually change these in the reading file

TO-DO: include INDRA's de-duplicating package
TO-DO: reduce number of improperly defined entites
TO-DO: find cell type/line
~~~


## Examples
- see [`examples/test-translation.bash`](examples/test-translation.bash)