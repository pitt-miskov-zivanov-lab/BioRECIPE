# Translation

## Description of files

- `event_collapse.py` - Main script for converting TRIPS, REACH, SOFIA extractions to tabular format
- `ModelNodes.py` - Contains data structures used by other translation scripts (event, entity, element, influence set classes)
- `ReachTranslate.py` - Standardizes REACH extractions to common semantic form
- `ReachManual.py` - converts .json extractions to .csv for easier reading
- `SofiaTranslate.py` - Standardizes SOFIA extractions to common semantic form
- `TripsTranslate.py` - Standardizes TRIPS extractions to common semantic form
- `TripsInterface.py` - Sends text or nxml papers to TRIPS parser and returns reading extractions
- `TripsAnalysis.py` - Used for converting batches of trips extractions into common sematic form (used in tandem with TripsInterface.py)

## Usage

- `event_collapse.py`
~~~
usage: event_collapse.py [-h] input_file
positional arguments: 
	input_file	machine reading extraction (.xlsx, .txt, .json)
~~~
- `*Translate.py`
~~~
usage: *Translate.py [-h] input_file
positional arguments: 
	input_file	machine reading extraction (.xlsx, .txt, .json)
~~~
- `TripsInterface.py`
~~~
usage: TripsInterface.py [-h] input_file pStart extension
positional arguments: 
	input_file	machine reading extraction (.xlsx, .txt, .json)
	pStart		all text chunks (groups of sentences under 500 chars) before this point are ignored
	extension	either 'CWMS' or 'DRUM' for world modelers or biological applications
output: is a series of extractions (.txt) for each chunk, labeled papernamePA-B.txt (paragraph A, chunk B)
~~~
- `TripsAnalysis.py`
~~~
usage: TripsInterface.py [-h] input_file
positional arguments: 
	input_file	name of paper sent for parsing through TripsInterface
output: common semantic form (output.txt) and printout of nested event, event, and sentence counts
~~~
