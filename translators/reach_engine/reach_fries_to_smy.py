# Created by Difei May 2023

# Usage
###############
# python reach_fries_to_smy.py -i multiple_json_dir -o json_summary_file
###############

# Function
###############
# Take REACH outputs(multiple JSON files in the folder), assemble them into a single and large JSON file
###############

import json
import os
import glob
import argparse

def summarize_reach_fries(reach_input_dir, reach_output_file):

    path = os.path.join(reach_input_dir, '*.txt')
    files = glob.glob(path)

    data_events = dict()
    data_entities = dict()
    data_sentences = dict()
    for fn in files:
        pathname, _ = os.path.splitext(fn)
        basename = os.path.basename(pathname)

        # Opening JSON file
        events_fn = os.path.join(reach_input_dir, basename + '.uaz.events.json')
        entities_fn = os.path.join(reach_input_dir, basename + '.uaz.entities.json')
        sentences_fn = os.path.join(reach_input_dir, basename + '.uaz.sentences.json')

        with open(events_fn, 'r', encoding='utf-8') as json_file:
            events = json.load(json_file)
            for i, value in events.items():
                if i == 'frames':
                    if i not in data_events:
                        data_events[i] = value
                    else:
                        data_events[i].extend(value)

        with open(entities_fn, 'r', encoding='utf-8') as json_file:
            entities = json.load(json_file)
            for i, value in entities.items():
                if i == 'frames':
                    if i not in data_entities:
                        data_entities[i] = value
                    else:
                        data_entities[i].extend(value)

        with open(sentences_fn, 'r', encoding='utf-8') as json_file:
            sentences = json.load(json_file)
            for i, value in sentences.items():
                if i == 'frames':
                    if i not in data_sentences:
                        data_sentences[i] = value
                    else:
                        data_sentences[i].extend(value)

        data = dict()

        data["events"] = data_events
        data["entities"] = data_entities
        data["sentences"] = data_sentences

        with open(reach_output_file, 'w') as output_file:
            json.dump(data, output_file, indent=4)


def main():
	parser = argparse.ArgumentParser(description='summarize individual json files in reach_fries data representation to a big json file')

	parser.add_argument('-i', '--input', type=str, required=True,
	                     help='Folder name that contains multiple json files')
	parser.add_argument('-o', '--output', type=str, required=True,
	                     help='Path of the output summary json file')
	args = parser.parse_args()
	summarize_reach_fries(args.input, args.output)

if __name__ == '__main__':
	main()
