from tkinter.filedialog import askopenfilename
from CWMSTranslate import TripsTranslator
import csv


# user selects EKB data to process (deprecated)
def file_input():
	
	#User selects text file
	filename = askopenfilename(title = "Select Text File")
	try:
		#Reading XML in string format
		text_data = open(filename,'r')
		ekb_data = text_data.read()
	except:
		print('ERROR: incompatible file format!')
		ekb_data = None

	return (ekb_data)

# user selects a text file containing XML data from TRIPS
ekb_data = file_input()
print(ekb_data)

if (ekb_data != None):
 	
 	trips_processor = TripsTranslator(ekb_data)
 	trips_processor.xml_to_dict()
 	trips_processor.refine_dict()
 	term_dict, event_dict = trips_processor.get_dicts()

# writing out the dictionaries to the csv
toCSV1 = []
toCSV2 = []
for k,v in term_dict.items():
	toCSV1.append(term_dict[k])
for k,v in event_dict.items():
	toCSV2.append(event_dict[k])
keys1 = ['term_id','term_name', 'term_norm', 'term_type','database_id','paragraph',
		'positive_reg_id', 'positive_reg_name', 'positive_reg_action', 
		'negative_reg_id','negative_reg_name','negative_reg_action', 'parent_event']
keys2 = ['event_id','event_name', 'event_norm', 'event_type','database_id','paragraph',
		'event_polarity', 'parent_event', ':AGENT', ':AFFECTED']

with open('cwms_output.csv', 'w', newline='') as output_file:
	dict_writer = csv.DictWriter(output_file,keys1)
	dict_writer.writeheader()
	firstrow = {}
	for i in range(0,len(keys1)):
		firstrow[keys1[i]]=keys1[i]
	dict_writer.writerows(toCSV1)

	dict_writer = csv.DictWriter(output_file,keys2)
	dict_writer.writeheader()
	firstrow = {}
	for i in range(0,len(keys2)):
		firstrow[keys2[i]]=keys2[i]
	dict_writer.writerows(toCSV2)