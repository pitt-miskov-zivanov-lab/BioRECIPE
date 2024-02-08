# FRIES/MITRE/TRIPS Pitt Translator
import os
from os import listdir
import json
import csv
from pprint import pprint
from tkinter import *
from tkinter import filedialog
from urllib.request import urlopen
from urllib.error import *
import xml.etree.ElementTree as ET

# Import the translations functions stores in the translatorFunctions.py file
from translatorFunctions import *

# linkDB uses external databases from database identifiers to complete
# missing fields for an element. 
def linkDB(modelData):
    if modelData[12] == None:
    	if len(modelData[7]) != 0:
	        # Get more information from UNIPROT database
	        try:
	            url = 'http://www.uniprot.org/uniprot/' + modelData[7][0] + '.xml'
	            body = urlopen(url).read()
	            root = ET.fromstring(body)
	            fullName = root.find('{http://uniprot.org/uniprot}entry/{http://uniprot.org/uniprot}protein/' +
	            				     '{http://uniprot.org/uniprot}recommendedName/{http://uniprot.org/uniprot}fullName')
	            location = root.find("{http://uniprot.org/uniprot}entry/{http://uniprot.org/uniprot}comment[@type='subcellular location']/" +
	            					 "{http://uniprot.org/uniprot}subcellularLocation/{http://uniprot.org/uniprot}location")
	            organism = root.find("{http://uniprot.org/uniprot}entry/{http://uniprot.org/uniprot}organism/" +
	            					 "{http://uniprot.org/uniprot}name[@type='common']")
	            modelData[1] = fullName.text
	            modelData[14] = location.text
	            modelData[12] = organism.text

	        except (ValueError, HTTPError, AttributeError) as e:
	            pass

    return modelData
# end linkDB





# The main loop of the program

origType = None
incorrectAttempts = 0
root = Tk()
##root.withdraw()

textBoxText = "Welcome to the translator!\nPlease select an original file type to translate to the Pitt formalism."
modelData = []

class App(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        
    def createWidgets(self):
        # Text box
        self.title = LabelFrame(self, text="FRIES/MITRE/Pitt Translator")
        self.title.pack(fill="both", expand=1)
        self.left = Label(self.title, text=textBoxText)
        self.left["justify"] = "left"
        self.left["width"] = 50
        self.left.pack(fill="both", expand=1)

        # File select button
        self.fries = Button(self)
        self.fries["text"] = "Load File"
        self.fries["command"] = self.selectFile
        self.fries["width"] = 10
        self.fries["height"] = 3
        self.fries["border"] = 3
        self.fries["font"] = ["calibri", 24, "bold"]
        self.fries["anchor"] = "center"
        self.fries.pack(side="left", padx=30, pady=30, fill="both")

        # MITRE folder select button
        self.mitre = Button(self)
        self.mitre["text"] = "Load MITRE \nFolder"
        self.mitre["command"] = self.mitreFolder
        self.mitre["width"] = 10
        self.mitre["height"] = 3
        self.mitre["border"] = 3
        self.mitre["font"] = ["calibri", 24, "bold"]
        self.mitre["anchor"] = "center"
        self.mitre.pack(side = "right", padx=30, pady=30, fill="both")

    def selectFile(self):
        # Delete the selection buttons and update text box
        self.fries.destroy()
        self.mitre.destroy()
        self.left["text"] = "Select a file for translation.\n"
        
        # Ask for a file to read
        filePath = filedialog.askopenfilename()

        global modelData
        format = checkFormat(filePath)

        if format == "FRIES":
            # Translate from FRIES to Pitt
            modelData = translateFRIES(filePath)

            # Ask if done or if user wants to link context and entity information
            # from an entity JSON file in FRIES format.
            self.left["text"] = "Translation from FRIES to Pitt successful.\n"
            self.left["text"] += "Would you like to add context and entity information?\n"
            self.addEntities = Button(self, text="Link Entity File",
                                      command=self.addEntityInfo, width=13, height=3,
                                      border=3, font=["calibri",24,"bold"])
            self.addEntities.pack(side="right", padx=30, pady=30, fill="both", expand=1)

            self.save = Button(self, text="Save Output",
                               command=self.saveOutput, width=10, height=3,
                               border=3, font=["calibri",24,"bold"])
            self.save.pack(side="left", padx=30, pady=30, fill="both", expand=1)

        elif format == "medscanFRIES":
            # Translate from MedScan FRIES to Pitt
            modelData = translateMedScanFRIES(filePath)

            self.left["text"] = "Translation from MedScan FRIES to Pitt successful.\n"
                    
            self.save = Button(self, text="Save Output",
                               command=self.saveOutput, width=10, height=3,
                               border=3, font=["calibri",24,"bold"])
            self.save.pack(side="left", padx=30, pady=30, fill="both", expand=1)

        elif format == "MITRE":
            # Translate from MITRE to Pitt
            modelData = translateMITRE(filePath)

            self.left["text"] = "Translation from MITRE to Pitt successful.\n"
            
            self.save = Button(self, text="Save Output",
                               command=self.saveOutput, width=10, height=3,
                               border=3, font=["calibri",24,"bold"])
            self.save.pack(side="left", padx=30, pady=30, fill="both", expand=1)

        elif format == "TRIPS":
            # Translate from TRIPS to Pitt
            modelData = translateTRIPS(filePath)

            self.left["text"] = "Translation from TRIPS to Pitt successful.\n"
            
            self.save = Button(self, text="Save Output",
                               command=self.saveOutput, width=10, height=3,
                               border=3, font=["calibri",24,"bold"])
            self.save.pack(side="left", padx=30, pady=30, fill="both", expand=1)


        else:
            # If file format is invalid or not supported, alert the user and
            # allow them to try again.
            self.left["text"] = "File is not in a valid format for translation. Please try again.\n"
            self.again = Button(self, text="Translate\n additional files",
                            command=self.doAgain, width=16, height=3,
                            border=3, font=["calibri",24,"bold"])
            self.again.pack(side="left", padx=30, pady=30, fill="both", expand=1)
        

    def addEntityInfo(self):
        self.left["text"] = "Select matching entity file, if any.\n"
        
        options = {}
        options["title"] = "Select matching entity file, if any\n"
        options["filetypes"] = [("JSON",".json"), ("Text files", ".txt"), ("All files", ".*")]
        entityFilePath = filedialog.askopenfilename(**options)
        global modelData
        
        try:
            modelData = addContextAndEntityInfo(modelData, entityFilePath)
            self.addEntities.destroy()
            self.left["text"] = "Entities linked successfully.\n"
        except KeyError:
            self.left["text"] = "KeyError... No context or entity information added.\n"
        
    def mitreFolder(self):
        self.mitre.destroy()
        self.fries.destroy()
        
        self.left["text"] = "Select a folder containing MITRE files.\n"
        self.left["text"] += "Output will be a multi-row spreadsheet.\n"
        path = filedialog.askdirectory()
        global modelData

        # Translate multiple files from a folder.
        # folderPath = filedialog.askdirectory(**options)
        modelData = translateMultipleMITRE(path)
        
        self.left["text"] = "Translation from MITRE to Pitt successful.\n"
        self.left["text"] += "Save output to .csv?\n"

        self.save = Button(self, text="Save Output",
                           command=self.saveOutput, width=10, height=3,
                           border=3, font=["calibri",24,"bold"])
        self.save.pack(side="left", padx=30, pady=30, fill="both", expand=1)

    def saveOutput(self):
        self.save.destroy()
        try:
            self.addEntities.destroy()
        except:
            pass
        
        self.left["text"] = "Preparing data..."
        global modelData
        # Convert PittRow class instance to array for for saving to a spreadsheet
        modelData = ConvertPittListToPittArray(modelData)
        # Remove empty rows, handle duplicate rows, and remove columns 43+
        modelData = removeRowsWithEmptyColumns(modelData, 4, None)
        #modelData = pittify(modelData) # Function deprecated
        #modelData = consolidateDuplicates(modelData)

        for i in range(len(modelData)):
            self.left["text"] = "Preparing data...\nFetching info from external databases: " + str(i) + "/" + str(len(modelData))
            modelData[i] = linkDB(modelData[i])
        self.left["text"] = "Data is ready to save.\nPlease name the output file.\n"
        
        options = {}
        options['defaultextension'] = '.csv'
        options['filetypes'] = [('CSV (Comma delimited)', '.csv'),('All files', '.*')]
        options['title'] = 'Save Output'
        #options['initialdir'] = os.getcwd()
        outputPath = filedialog.asksaveasfilename(**options)

        # Write to CSV
        if outputPath == '':
            # The user pressed cancel on the file saved dialog box
            # Allow them to start over or quit
            self.left["text"] = "File save canceled.\n"
        else:
            writeToCSV(modelData, declareColumnHeaders(), outputPath)
            self.left["text"] = "Save successful.\n"
            
        self.left["text"] += "Would you like to translate another file, or are you done?"

        self.again = Button(self, text="Translate\n additional files",
                            command=self.doAgain, width=16, height=3,
                            border=3, font=["calibri",24,"bold"])
        self.again.pack(side="left", padx=30, pady=30, fill="both", expand=1)
        
        self.quit = Button(self, text="Quit",
                           command=root.destroy, width=10, height=3,
                           border=3, font=["calibri",24,"bold"])
        self.quit.pack(side="right", padx=30, pady=30, fill="both", expand=1)

    def doAgain(self):
        try:
            self.again.destroy()
        except:
            pass
        try:
            self.quit.destroy()
        except:
            pass
        try:
            self.title.destroy()
        except:
            pass
        try:
            self.left.destroy()
        except:
            pass
        
        self.createWidgets()

# create the application
myapp = App(master=root)

myapp.master.title("Translator")
myapp.master.minsize(640, 320)

myapp.mainloop()        
