# translateMultipleMITRE
# Created by Bryce Aidukaitis
# September 3rd, 2016

# This program prompts the user to select a folder containing FRIES (JSON)
# files whose file names contain the terms "events" and "entities".
# The program translates each "events" file to the Pitt formalism (.csv),
# linking it with its corresponding "entities" file. The user is prompted
# for a directory in which to save the output files, which are named
# similar to the file from which they were translated.

# NOTE: file names in the folder must be of this type:
# ...\PMCxxxxxx.entities.json
# ...\PMCxxxxxx.events.json
# ...\PMCxxxxxx.links.json
# ...\PMCxxxxxx.sentences.json

# Import relevant libraries
import os
from os import listdir
import json
import csv
from pprint import pprint
from tkinter import *
from translatorFunctions import *

root = Tk()
root.withdraw()

# Get the input folder
print("Please select the input folder.")
inputPath = filedialog.askdirectory()

# Get the output folder
print("\nThank you.\nPlease select the output path.")
#outputPath = filedialog.askdirectory()
options = {}
options['defaultextension'] = '.csv'
options['filetypes'] = [('CSV (Comma delimited)', '.csv'),('All files', '.*')]
options['title'] = 'Save as...'
savePath = filedialog.asksaveasfilename(**options)

# Get the files in that folder
fileList = listdir(inputPath)

# Transform the file list into a list of PMC IDs, "events" files,
# "entities" files, and file paths
# Developer's note: the following to "for" loops can be consolidated
inputList = []
for i in range(len(fileList)):
    if "events" in fileList[i]:
        # Split the file name from "PMCxxxxxxx.events.json" into components,
        # "PMCxxxxxxx", "events", and "json"
        fileNameComponents = fileList[i].split('.')

        # Create a dictionary to store PMC id, the "entities" file path,
        # and the "events" file path
        myDictionary = {}
        myDictionary["PMCID"] = fileNameComponents[0]
        myDictionary["eventsPath"] = inputPath + "\\" + fileList[i]
        myDictionary["entitiesPath"] = (inputPath + "\\"
                                        + fileNameComponents[0] + "."
                                        + fileNameComponents[1]
                                        + ".entities.json")

        # Add this dictionary to the list of inputs
        inputList.append(myDictionary)

# Initialize a list to store the information from all files
allData = []

# Translate each "events" file, link with "entities", print output
for i in range(len(inputList)):
    print("Translating for article " + inputList[i]["PMCID"])
    # First translate the input file 
    data = translateFRIES(inputList[i]["eventsPath"])

    # Then link the "entities" file
    data = addContextAndEntityInfo(data, inputList[i]["entitiesPath"])

    # Add this translated information to the list of all data
    allData += data

# Prepare the file for saving
allData = ConvertPittListToPittArray(allData)
allData = removeRowsWithEmptyColumns(allData, 4, None)
#allData = consolidateDuplicates(data)

# Print the translated data to the output file
#savePath = outputPath + "\\" + inputList[i]["PMCID"] + ".csv"
writeToCSV(allData, declareColumnHeaders(), savePath)

# Print a success message for the user upon successful completion
print("Successfully translated " + str(len(inputList)) + " files.")



