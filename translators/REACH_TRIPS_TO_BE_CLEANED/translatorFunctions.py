# FRIES/MITRE/Pitt Translator
# Created by Bryce Aidukaitis
# June 14th, 2016

import os
from os import listdir
import json
import csv
from pprint import pprint
from TripsTranslate import *
from TreeExtraction import *

# The class PittRow defines fields in the U. Pitt modeling formalism
# that are converted into rows by the function ConvertPittListToPittArray
class PittRow:
    # Regulated element fields
    ElementName = None
    ElementComponents = None
    ElementType = None
    ElementDatabaseID = None
    ElementElementID = None
    ElementSite = None
    ElementCellLine = None
    ElementCellType = None
    ElementOrganism = None
    ElementTissueType = None
    ElementLocation = None
    ElementLocationID = None

    ElementContextID = None
    ElementEntityMentionID = None
    

    # Positive regulator fields
    PosRegName = None
    PosRegComponents = None
    PosRegType = None
    PosRegDatabaseID = None
    PosRegElementID = None

    # Negative regulator fields
    NegRegName = None
    NegRegComponents = None
    NegRegType = None
    NegRegDatabaseID = None
    NegRegElementID = None

    # Other fields
    RegEntityMentionID = None
    RegContextID = None
    MechanismType = None
    PaperID = None
    IndexCardID = None
# end class PittRow

# The class "Participant" holds information about a single MITRE participant,
# useful in the function getMITREParticipantInformation
class Participant:
    Name = None
    Components = None
    Type = None
    DatabaseID = None
    ElementID = None
# end class Participant

# The function ConvertPittListToPittArray converts a list Pittlist of instances
# of the class PittRow into an array for saving as a spreadsheet of Pitt data
def ConvertPittListToPittArray(PittList):
    # Create an array with as many rows as there are items in PittList
    if type(PittList) is list:
        Array = [None] * len(PittList)
        numPitt = len(PittList)
    else:
        Array = [None]
        numPitt = 1

    # Define the number of columns in each row
    NumColumns = 54
    
    # Convert each item in PittList to a row of Pitt array data
    if type(PittList) is list:
        for i in range(numPitt):
            Array[i] = [None] * NumColumns

            # Transfer regulated element information to the appropriate columns
            Array[i][4] = PittList[i].ElementName
            Array[i][5] = PittList[i].ElementComponents
            Array[i][6] = PittList[i].ElementType
            Array[i][7] = PittList[i].ElementDatabaseID
            Array[i][8] = PittList[i].ElementElementID
            Array[i][9] = PittList[i].ElementSite
            Array[i][10] = PittList[i].ElementCellLine
            Array[i][11] = PittList[i].ElementCellType
            Array[i][12] = PittList[i].ElementOrganism
            Array[i][13] = PittList[i].ElementTissueType
            Array[i][14] = PittList[i].ElementLocation
            Array[i][15] = PittList[i].ElementLocationID

            # Transfer regulator information to the appropriate columns
            Array[i][34] = PittList[i].PosRegName
            Array[i][35] = PittList[i].PosRegComponents
            Array[i][36] = PittList[i].PosRegType
            Array[i][37] = PittList[i].PosRegDatabaseID
            Array[i][38] = PittList[i].PosRegElementID
            Array[i][39] = PittList[i].NegRegName
            Array[i][40] = PittList[i].NegRegComponents
            Array[i][41] = PittList[i].NegRegType
            Array[i][42] = PittList[i].NegRegDatabaseID
            Array[i][43] = PittList[i].NegRegElementID

            # Transfer other information to the appropriate columns
            Array[i][45] = PittList[i].MechanismType
            Array[i][52] = PittList[i].PaperID
            Array[i][53] = PittList[i].IndexCardID

    elif type(PittList) is PittRow:
        Array[0] = [None] * NumColumns
        
        # Transfer regulated element information to the appropriate columns
        Array[0][4] = PittList.ElementName
        Array[0][5] = PittList.ElementComponents
        Array[0][6] = PittList.ElementType
        Array[0][7] = PittList.ElementDatabaseID
        Array[0][8] = PittList.ElementElementID
        Array[0][9] = PittList.ElementSite
        Array[0][10] = PittList.ElementCellLine
        Array[0][11] = PittList.ElementCellType
        Array[0][12] = PittList.ElementOrganism
        Array[0][13] = PittList.ElementTissueType
        Array[0][14] = PittList.ElementLocation
        Array[0][15] = PittList.ElementLocationID

        # Transfer regulator information to the appropriate columns
        Array[0][34] = PittList.PosRegName
        Array[0][35] = PittList.PosRegComponents
        Array[0][36] = PittList.PosRegType
        Array[0][37] = PittList.PosRegDatabaseID
        Array[0][38] = PittList.PosRegElementID
        Array[0][39] = PittList.NegRegName
        Array[0][40] = PittList.NegRegComponents
        Array[0][41] = PittList.NegRegType
        Array[0][42] = PittList.NegRegDatabaseID
        Array[0][43] = PittList.NegRegElementID

        # Transfer other information to the appropriate columns
        Array[0][45] = PittList.MechanismType
        Array[0][52] = PittList.PaperID
        Array[0][53] = PittList.IndexCardID
    else:
        print('Warning... Could not convert PittRow List to Pitt array as input PittList type is unacceptable: ' + str(type(PittList)))

            
    return Array
#end ConvertPittListToPittArray


# sumStrings converts a list of string into a comma-separated combined string
def sumStrings(listOfStrings):
    if isinstance(listOfStrings, list):
        allStrings = listOfStrings[0]
        for index in range(1, len(listOfStrings)):
                           allStrings += ', ' + listOfStrings[index]
        return allStrings
    else:
        return listOfStrings
# end sumStrings
    
# declareColumnHeaders Creates an array of column headers for our model file 
def declareColumnHeaders():
    columnHeaders = ['#',                           
                      'Full Element Name',          
                      'Importance',                 
                      None,                         
                      'Element name',               
                      'Element components',
                      'Element type',               
                      'Database ID',                
                      'Element ID',                 
                      'Site',
                      'Cell line',                  
                      'Cell type',                  
                      'Organism',                   
                      'Tissue type',                #
                      'Location',                   #
                      'Location identifier',        # 
                      'NOTES',                      # 
                      None,                         # 
                      'Variable name',              # 
                      'Model Input (I) Output (O)', # 
                      'Spontaneously Restores (R) Degrades (D)',    # 
                      'Type of value: Activity (A) Amount (C) Process (P)', #
                      'Begin',                      # 
                      'End',                        # 
                      'Sim End',                    # 
                      'Begin',                      # 
                      'End',                        # 
                      'Sim End',                    # 
                      'Begin',                      # 
                      'End',                        # 
                      'Sim End',                    # 
                      'NOTES',                      # 
                      None,                         # 
                      'No. of reg.',                # 
                      'PosReg Name',                   
                      'PosReg Components',                   
                      'PosReg Type',
                      'PosReg Database ID',
                      'PosReg Element ID',                   
                      'NegReg Name',                   
                      'NegReg Components',                   
                      'NegReg Type',
                      'NegReg Database ID',
                      'NegReg Element ID', 
                      'Interaction Direct (D) Indirect (I)',    # 
                      'Mechanism type for direct (D)',          # 
                      'NOTES',                                  # 
                      None,                                     # 
                      'Unique ID (text)',                       # 
                      'Element kind',                           # 
                      'Element sub-type',                       # 
                      None,                                     # 
                      'Paper ID',        #
                      'Index Card / Frame ID'
        ]            
    return columnHeaders
# end declareColumnHeaders

# checkFormat takes a file and returns its format - FRIES, MITRE, TRIPS, or
# unsupported/unknown types
def checkFormat(filePath):
    if ".json" in filePath:
        with open(filePath) as file:
            contents = json.load(file)
        if "frames" in contents:
            # This is likely a FRIES file. Inspect further...
            # Is it UAZ FRIES?
            formatFrameCount = 0
            for i in range(len(contents["frames"])):
                try:
                    if contents["frames"][i]["frame-type"] == "event-mention":
                        formatFrameCount += 1
                except:
                    return "invalidFRIES"
            # If there are as many of this type of frame as there are frame, return this format
            if formatFrameCount == len(contents["frames"]):
                return "FRIES"

            #Is it Medscan FRIES?
            formatFrameCount = 0
            for i in range(len(contents["frames"])):
                try:
                    if contents["frames"][i]["frame-type"] == "relation-mention" or contents["frames"][i]["frame-type"] == "relation":
                        formatFrameCount += 1
                except:
                    return "invalidFRIES" 
            # If there are as many of this type of frame as there are frame, return this format
            if formatFrameCount == len(contents["frames"]):
                return "medscanFRIES"

            # If it is neither, return invalidFRIES       
            return "invalidFRIES"
        if "interaction" in contents:
            # This is likely a MITRE file
            return "MITRE"
        else:
            return "unknown"
    if ".txt" in filePath:
        contents = list(open(filePath))
        for i in range(len(contents)):
            if "ONT::EVENT" in contents[i]:
                # This is likely a TRIPS file in XML format
                return "TRIPS"
        # If file is not TRIPS, return unknown    
        return "unknown"
# end checkFormat

# endWithChar accepts a string and returns the first substring that terminates
# with an acceptable character, with said characters being defined in the
# array "chars" given below (e.g., endWithChar("V142362 ONT:EVENT...") will
# return "V142362", as a space is not an acceptable character
def endWithChar(string):
    chars = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p',
             'q','r','s','t','u','v','w','x','y','z',
             'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
             'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
             '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
             '-', '_', '/', '\\', '.', ',']
    
    for i in range(len(string)):
        if string[i] not in (chars):
            return string[:i]
    return string
# end endWithChar

# removeRowsWithEmptyColumns removes rows from an array "modelData" that do
# not contain a value other than "nullValue" in the column "columnToCheck"
def removeRowsWithEmptyColumns(array, columnToCheck, nullValue):
    # Make a list of the row indices for later removal
    badRows = []
    # Search for rows to remove
    for i in range(len(array)):
        if array[i][columnToCheck] == nullValue:
            # Make a list of the index for later removal
            badRows.append(i)
    if len(badRows) == 0:
        # There were no rows to delete--return the original array
        return array
    else:
        # Recreate the list without rows with numbers listed in badRows
        newArray = [None] * (len(array) - len(badRows))
        badIndex = 0
        for i in range(len(array)):
            if i in badRows:
                badIndex += 1
            else:
                newArray[i - badIndex] = array[i]
        return newArray
# end removeRowsWithEmptyColumns       

# writeToCSV writes the data in modelData with column header defined by
# columnHeaders to a file fileName
def writeToCSV(modelData, columnHeaders, filePath):
    try:
        with open(filePath, 'w') as csvfile:
            modelfile = csv.writer(csvfile, dialect = 'excel', delimiter=',',
                                   lineterminator = '\n'
                                   #quotechar='|',
                                   #quoting=csv.QUOTE_MINIMAL
                                   )
            # Comment out this next line if you do not want to include
            # column headers in the output document
            modelfile.writerow(columnHeaders)
            modelfile.writerows(modelData)
    except PermissionError:
        print("Please close the file " + fileName + " and try again.")
# end writeToCSV


# translateMITRE translates a single MITRE file at the path filePath
# and returns the data
def deprecatedTranslateMITRE(filePath):
    modelData = [None] * 46

    # Import JSON file
    with open(filePath) as MITREData:
        data = json.load(MITREData)

    # If the "negative information" field is set to true, then none of the
    # binding described in this file occurs - so skip this file!
    try:
        if data["interaction"]["negative_information"] == "true":
            return modelData
    except KeyError:
        pass

    # Extract reference article ID
    try:
        modelData[42] = data["pmc_id"]
    except:
        print("Warning in file " + filePath + " ... could not extract PMC ID.")
    # For convenience, limit data to interaction data
    try:
        data = data["interaction"]
    except:
        print("Warning in file " + filePath + " ... could not access 'interaction' field.")

    # Check to see if the primary element is a complex
    if "entities" in data["participant_b"]:
        # Store names in a complex, formatted as {element1, element 2, ...}
        try:
            modelData[4] = '{' + sumStrings(data["participant_b"]["entities"][0]["entity_text"])
            for entity in range(1, len(data["participant_b"]["entities"])):
                modelData[4] += ', ' + sumStrings(data["participant_b"]["entities"][entity]["entity_text"])
                if entity == len(data["participant_b"]["entities"]) - 1:
                    modelData[4] += "}"
        except KeyError:
            print("Warning in file " + filePath + " ... Error storing entity names in a complex.")

        # Store type ("complex")
        try:
            modelData[5] = data["participant_b"]["entity_type"]
        except KeyError:
            print("Warning in file " + filePath + " ... Error storing entity type in a complex.")
        
        # Store database IDs in a complex, formatted as {element1, element 2, ...}
        try:
            if data["participant_b"]["entities"][0]["identifier"] == "ungrounded":
                modelData[6] = "ungrounded"
                modelData[7] = "ungrounded"
            else:
                modelData[6] = '{' + data["participant_b"]["entities"][0]["identifier"][:data["participant_b"]["entities"][0]["identifier"].index(':')]
                modelData[7] = '{' + data["participant_b"]["entities"][0]["identifier"][data["participant_b"]["entities"][0]["identifier"].index(':')+1:]
                for entity in range(1, len(data["participant_b"]["entities"])):
                    modelData[6] += ', ' + data["participant_b"]["entities"][entity]["identifier"][:data["participant_b"]["entities"][0]["identifier"].index(':')]
                    modelData[7] += ', ' + data["participant_b"]["entities"][entity]["identifier"][data["participant_b"]["entities"][0]["identifier"].index(':')+1:]
                    if entity == len(data["participant_b"]["entities"]) - 1:
                        modelData[6] += "}"
                        modelData[7] += "}"
        except:
            print("Warning in file " + filePath + " ... Error storing database IDs in a complex.")

    # If it is not a complex, do the following
    else:
        # participant_b is the element under study - set its name
        try:
            modelData[4] = sumStrings(data["participant_b"]["entity_text"])
        except:
            print("Warning in file " + filePath + " ... Error extracting entity name.")
    
        # Set its type
        try:
            modelData[5] = data["participant_b"]["entity_type"]
        except:
            print("Warning in file " + filePath + " ... Error storing entity type.")

        # Set its database type
        try:
            modelData[6] = data["participant_b"]["identifier"][:data["participant_b"]["identifier"].index(':')]
            # Set its database value (number)
            modelData[7] = data["participant_b"]["identifier"][data["participant_b"]["identifier"].index(':')+1:]
        except ValueError:
            modelData[6] = data["participant_b"]["identifier"] # Works in the case that the identifier is "ungrounded"
            modelData[7] = data["participant_b"]["identifier"]
   
    # Determine what regulators exist and populate the appropriate fields
    try:
        if data["interaction_type"] == "increases":
            # participant_a is a positive regulator of participant_b
            modelData[32] = sumStrings(data["participant_a"]["entity_text"])
            modelData[35] = "positive activation"
        elif data["interaction_type"] == "decreases":
            # participant_a is a negative regulator of participant_b
            modelData[33] = sumStrings(data["participant_a"]["entity_text"])
            modelData[35] = "negative activation"
        else:
            # We don't know what type of regulator is involved -- default to positive regulation
            modelData[32] = sumStrings(data["participant_a"]["entity_text"])
            modelData[35] = data["interaction_type"]
    except:
        print("Warning in file " + filePath + " ... Error storing regulator names/types.")

    # Return the translated data
    return modelData
# end deprecatedTranslateMITRE

def translateMITRE(filePath):
    Row = PittRow()

    # Import JSON file
    with open(filePath) as MITREData:
        data = json.load(MITREData)

    # If the "negative information" field is set to true, then none of the
    # binding described in this file occurs - so skip this file!
    try:
        if data["interaction"]["negative_information"] == "true":
            return Row # Returns the empty row
    except KeyError:
        pass

    # Extract reference article ID
    try:
        Row.PaperID = data["pmc_id"]
    except:
        print("Warning in file " + filePath + " ... could not extract PMC ID.")

    # Extract the index card ID (MITRE file name) from the full file path
    try:
        FileName = filePath.split("\\")
        FileName = FileName[len(FileName) - 1]
        Row.IndexCardID = FileName
    except:
        print("Warning in file " + filePath + " ... could not extract index card ID.")
        
    # For convenience, limit data to interaction data
    try:
        data = data["interaction"]
    except:
        print("Warning in file " + filePath + " ... could not access 'interaction' field.")

    # Extract element information based on element type

    # Check to see if the element contains a nested reaction:
    if "participant_a" in data["participant_b"] or "participant_b" in data["participant_b"]:
        Row = getMITRENestedReactionParticipants(data, Row, filePath)
        return Row
    elif "participant_a" in data["participant_a"] or "participant_b" in data["participant_a"]:
        print("Warning in file " + filePath + " ... Nested reactions in field 'participant_a' unsupported.")
        return Row
    
    # Check to see if the element is a complex
    elif "entity_type" in data["participant_b"] and data["participant_b"]["entity_type"] == "complex":
        # If the element is a complex, do the following

        # Extract the complex name
        if "entity_text" in data["participant_b"]:
            Row.ElementName = data["participant_b"]["entity_text"][0]
        else:
            print("Warning in file " + filePath + " ... no field 'entity_text' found in object 'participant_b'.")

        # Store the data from each listed entity in a comma-separated list between parentheses
        if "entities" in data["participant_b"] and len(data["participant_b"]["entities"]) > 0:           
            for i in range(len(data["participant_b"]["entities"])):
                # Check to see if the required fields exist in each entity
                if "entity_text" in data["participant_b"]["entities"][i]:
                    ElementName = data["participant_b"]["entities"][i]["entity_text"][0]
                else:
                    ElementName = None

                if "entity_type" in data["participant_b"]["entities"][i]:
                    ElementType = data["participant_b"]["entities"][i]["entity_type"]
                else:
                    ElementType = None

                if "identifier" in data["participant_b"]["entities"][i] and ':' in data["participant_b"]["entities"][i]["identifier"]:
                    DatabaseID = data["participant_b"]["entities"][i]["identifier"][:data["participant_b"]["entities"][i]["identifier"].index(':')]
                    ElementID = data["participant_b"]["entities"][i]["identifier"][data["participant_b"]["entities"][i]["identifier"].index(':')+1:]
                elif "identifier" in data["participant_b"]["entities"][i] and ':' not in data["participant_b"]["entities"][i]["identifier"]:
                    DatabaseID = data["participant_b"]["entities"][i]["identifier"]
                    ElementID = data["participant_b"]["entities"][i]["identifier"]
                else:
                    DatabaseID = None
                    ElementID = None

                # Place those fields into comma-separated lists between parentheses
                if i == 0:
                    Row.ElementComponents = "("
                    Row.ElementType = "("
                    Row.ElementDatabaseID = "("
                    Row.ElementElementID = "("
                elif i <= len(data["participant_b"]["entities"]) - 1:
                    Row.ElementComponents += ","
                    Row.ElementType += ","
                    Row.ElementDatabaseID += ","
                    Row.ElementElementID += ","

                Row.ElementComponents += ElementName
                Row.ElementType += ElementType
                Row.ElementDatabaseID += DatabaseID
                Row.ElementElementID += ElementID
                
                if i == len(data["participant_b"]["entities"]) - 1:
                    Row.ElementComponents += ")"
                    Row.ElementType += ")"
                    Row.ElementDatabaseID += ")"
                    Row.ElementElementID += ")"
                    
        elif "entities" not in data["participant_b"]:
            print("Warning in file " + filePath + " ... no field 'entities' found in object 'participant_b'.")            

    # Check to see if the element is a protein family
    elif "entity_type" in data["participant_b"] and data["participant_b"]["entity_type"] == "protein_family":
        # If the element is a protein family, do the following

        Row.ElementType = "Protein family"

        # Extract the protein family name
        if "entity_text" in data["participant_b"]:
            Row.ElementName = data["participant_b"]["entity_text"][0]
        else:
            print("Warning in file " + filePath + " ... no field 'entity_text' found in object 'participant_b'.")

        # Store the data from each listed entity in a comma-separated list between parentheses
        if "entities" in data["participant_b"] and len(data["participant_b"]["entities"]) > 0:
            for i in range(len(data["participant_b"]["entities"])):
                # Check to see if the required fields exist in each entity
                if "entity_text" in data["participant_b"]["entities"][i]:
                    ElementName = data["participant_b"]["entities"][i]["entity_text"][0]
                else:
                    ElementName = None

                if "identifier" in data["participant_b"]["entities"][i] and ':' in data["participant_b"]["entities"][i]["identifier"]:
                    DatabaseID = data["participant_b"]["entities"][i]["identifier"][:data["participant_b"]["entities"][i]["identifier"].index(':')]
                    ElementID = data["participant_b"]["entities"][i]["identifier"][data["participant_b"]["entities"][i]["identifier"].index(':')+1:]
                elif "identifier" in data["participant_b"]["entities"][i] and ':' not in data["participant_b"]["entities"][i]["identifier"]:
                    DatabaseID = data["participant_b"]["entities"][i]["identifier"]
                    ElementID = data["participant_b"]["entities"][i]["identifier"]
                else:
                    DatabaseID = None
                    ElementID = None

                # Place those fields into comma-separated lists between parentheses
                if i == 0:
                    Row.ElementComponents = "{"
                    Row.ElementDatabaseID = "{"
                    Row.ElementElementID = "{"
                elif i <= len(data["participant_b"]["entities"]) - 1:
                    Row.ElementComponents += ","
                    Row.ElementDatabaseID += ","
                    Row.ElementElementID += ","

                Row.ElementComponents += ElementName
                Row.ElementDatabaseID += DatabaseID
                Row.ElementElementID += ElementID
                
                if i == len(data["participant_b"]["entities"]) - 1:
                    Row.ElementComponents += "}"
                    Row.ElementDatabaseID += "}"
                    Row.ElementElementID += "}"
                    
        elif "entities" not in data["participant_b"]:
            print("Warning in file " + filePath + " ... no field 'entities' found in object 'participant_b'.")    

    # If the element is neither, do the following
    elif "entity_type" in data["participant_b"]:
        # The element is neither a complex nor a protein family
        if "entity_text" in data["participant_b"]:
            Row.ElementName = data["participant_b"]["entity_text"][0]
            Row.ElementComponents = Row.ElementName
            Row.ElementType = data["participant_b"]["entity_type"]
            if "identifier" in data["participant_b"] and ':' in data["participant_b"]["identifier"]:
                Row.ElementDatabaseID = data["participant_b"]["identifier"][:data["participant_b"]["identifier"].index(':')]
                Row.ElementElementID = data["participant_b"]["identifier"][data["participant_b"]["identifier"].index(':')+1:]
            elif "identifier" in data["participant_b"] and ':' not in data["participant_b"]["identifier"]:
                Row.ElementDatabaseID = data["participant_b"]["identifier"]
                Row.ElementElementID = data["participant_b"]["identifier"]

    # Alert the user if no "entity_type" field is found
    elif "entity_type" not in data["participant_b"]:
        print("Warning in file " + filePath + " ... no field 'entity_type' found in object 'participant_b'.")
    
    # Determine what regulators exist and populate the appropriate fields
    # First, check to see if there is a regulator listed
    if "participant_a" in data:
        # Check to see what type of regulator this is
        if "interaction_type" in data and data["interaction_type"] != "decreases":
            # This is a positive regulator or defaults to one - transfer data to the appropriate fields

            if  data["interaction_type"] == "increases":
                Row.MechanismType = "Positive regulation"
            else:
                Row.MechanismType =  data["interaction_type"] # If neither "increases" nor "decreases", just copy what it is into this field
            
            # Check to see if the element is a complex
            if "entity_type" in data["participant_a"] and data["participant_a"]["entity_type"] == "complex":
                # If the element is a complex, do the following

                # Extract the complex name
                if "entity_text" in data["participant_a"]:
                    Row.PosRegName = data["participant_a"]["entity_text"][0]
                else:
                    print("Warning in file " + filePath + " ... no field 'entity_text' found in object 'participant_a'.")

                # Store the data from each listed entity in a comma-separated list between parentheses
                if "entities" in data["participant_a"] and len(data["participant_a"]["entities"]) > 0:           
                    for i in range(len(data["participant_a"]["entities"])):
                        # Check to see if the required fields exist in each entity
                        if "entity_text" in data["participant_a"]["entities"][i]:
                            ElementName = data["participant_a"]["entities"][i]["entity_text"][0]
                        else:
                            ElementName = None

                        if "entity_type" in data["participant_a"]["entities"][i]:
                            ElementType = data["participant_a"]["entities"][i]["entity_type"]
                        else:
                            ElementType = None

                        if "identifier" in data["participant_a"]["entities"][i] and ':' in data["participant_a"]["entities"][i]["identifier"]:
                            DatabaseID = data["participant_a"]["entities"][i]["identifier"][:data["participant_a"]["entities"][i]["identifier"].index(':')]
                            ElementID = data["participant_a"]["entities"][i]["identifier"][data["participant_a"]["entities"][i]["identifier"].index(':')+1:]
                        elif "identifier" in data["participant_a"]["entities"][i] and ':' not in data["participant_a"]["entities"][i]["identifier"]:
                            DatabaseID = data["participant_a"]["entities"][i]["identifier"]
                            ElementID = data["participant_a"]["entities"][i]["identifier"]
                        else:
                            DatabaseID = None
                            ElementID = None

                        # Place those fields into comma-separated lists between parentheses
                        if i == 0:
                            Row.PosRegComponents = "("
                            Row.PosRegType = "("
                            Row.PosRegDatabaseID = "("
                            Row.PosRegElementID = "("
                        elif i <= len(data["participant_a"]["entities"]) - 1:
                            Row.PosRegComponents += ","
                            Row.PosRegType += ","
                            Row.PosRegDatabaseID += ","
                            Row.PosRegElementID += ","

                        Row.PosRegComponents += ElementName
                        Row.PosRegType += ElementType
                        Row.PosRegDatabaseID += DatabaseID
                        Row.PosRegElementID += ElementID
                        
                        if i == len(data["participant_a"]["entities"]) - 1:
                            Row.PosRegComponents += ")"
                            Row.PosRegType += ")"
                            Row.PosRegDatabaseID += ")"
                            Row.PosRegElementID += ")"
                            
                elif "entities" not in data["participant_a"]:
                    print("Warning in file " + filePath + " ... no field 'entities' found in object 'participant_a'.")            

            # Check to see if the element is a protein family
            elif "entity_type" in data["participant_a"] and data["participant_a"]["entity_type"] == "protein_family":
                # If the element is a protein family, do the following

                Row.PosRegType = "Protein family"

                # Extract the protein family name
                if "entity_text" in data["participant_a"]:
                    Row.PosRegName = data["participant_a"]["entity_text"][0]
                else:
                    print("Warning in file " + filePath + " ... no field 'entity_text' found in object 'participant_a'.")

                # Store the data from each listed entity in a comma-separated list between parentheses
                if "entities" in data["participant_a"] and len(data["participant_a"]["entities"]) > 0:
                    for i in range(len(data["participant_a"]["entities"])):
                        # Check to see if the required fields exist in each entity
                        if "entity_text" in data["participant_a"]["entities"][i]:
                            ElementName = data["participant_a"]["entities"][i]["entity_text"][0]
                        else:
                            ElementName = None

                        if "identifier" in data["participant_a"]["entities"][i] and ':' in data["participant_a"]["entities"][i]["identifier"]:
                            DatabaseID = data["participant_a"]["entities"][i]["identifier"][:data["participant_a"]["entities"][i]["identifier"].index(':')]
                            ElementID = data["participant_a"]["entities"][i]["identifier"][data["participant_a"]["entities"][i]["identifier"].index(':')+1:]
                        elif "identifier" in data["participant_a"]["entities"][i] and ':' not in data["participant_a"]["entities"][i]["identifier"]:
                            DatabaseID = data["participant_a"]["entities"][i]["identifier"]
                            ElementID = data["participant_a"]["entities"][i]["identifier"]
                        else:
                            DatabaseID = None
                            ElementID = None

                        # Place those fields into comma-separated lists between parentheses
                        if i == 0:
                            Row.PosRegComponents = "{"
                            Row.PosRegDatabaseID = "{"
                            Row.PosRegElementID = "{"
                        elif i <= len(data["participant_a"]["entities"]) - 1:
                            Row.PosRegComponents += ","
                            Row.PosRegDatabaseID += ","
                            Row.PosRegElementID += ","

                        Row.PosRegComponents += ElementName
                        Row.PosRegDatabaseID += DatabaseID
                        Row.PosRegElementID += ElementID
                        
                        if i == len(data["participant_a"]["entities"]) - 1:
                            Row.PosRegComponents += "}"
                            Row.PosRegDatabaseID += "}"
                            Row.PosRegElementID += "}"
                            
                elif "entities" not in data["participant_a"]:
                    print("Warning in file " + filePath + " ... no field 'entities' found in object 'participant_a'.")    

            # If the element is neither, do the following
            elif "entity_type" in data["participant_a"]:
                # The element is neither a complex nor a protein family
                if "entity_text" in data["participant_a"]:
                    Row.PosRegName = data["participant_a"]["entity_text"][0]
                    Row.PosRegComponents = Row.PosRegName
                    Row.PosRegType = data["participant_a"]["entity_type"]
                    if "identifier" in data["participant_a"] and ':' in data["participant_a"]["identifier"]:
                        Row.PosRegDatabaseID = data["participant_a"]["identifier"][:data["participant_a"]["identifier"].index(':')]
                        Row.PosRegElementID = data["participant_a"]["identifier"][data["participant_a"]["identifier"].index(':')+1:]
                    elif "identifier" in data["participant_a"] and ':' not in data["participant_a"]["identifier"]:
                        Row.PosRegDatabaseID = data["participant_a"]["identifier"]
                        Row.PosRegElementID = data["participant_a"]["identifier"]

            # Alert the user if no "entity_type" field is found
            elif "entity_type" not in data["participant_a"]:
                print("Warning in file " + filePath + " ... no field 'entity_type' found in object 'participant_a'.")
            
        elif "interaction_type" in data and data["interaction_type"] == "decreases":
            # This is a negative regulator - transfer data to the appropriate fields

            Row.MechanismType = "Negative regulation"
            
            # Check to see if the element is a complex
            if "entity_type" in data["participant_a"] and data["participant_a"]["entity_type"] == "complex":
                # If the element is a complex, do the following

                # Extract the complex name
                if "entity_text" in data["participant_a"]:
                    Row.NegRegName = data["participant_a"]["entity_text"][0]
                else:
                    print("Warning in file " + filePath + " ... no field 'entity_text' found in object 'participant_a'.")

                # Store the data from each listed entity in a comma-separated list between parentheses
                if "entities" in data["participant_a"] and len(data["participant_a"]["entities"]) > 0:           
                    for i in range(len(data["participant_a"]["entities"])):
                        # Check to see if the required fields exist in each entity
                        if "entity_text" in data["participant_a"]["entities"][i]:
                            ElementName = data["participant_a"]["entities"][i]["entity_text"][0]
                        else:
                            ElementName = None

                        if "entity_type" in data["participant_a"]["entities"][i]:
                            ElementType = data["participant_a"]["entities"][i]["entity_type"]
                        else:
                            ElementType = None

                        if "identifier" in data["participant_a"]["entities"][i] and ':' in data["participant_a"]["entities"][i]["identifier"]:
                            DatabaseID = data["participant_a"]["entities"][i]["identifier"][:data["participant_a"]["entities"][i]["identifier"].index(':')]
                            ElementID = data["participant_a"]["entities"][i]["identifier"][data["participant_a"]["entities"][i]["identifier"].index(':')+1:]
                        elif "identifier" in data["participant_a"]["entities"][i] and ':' not in data["participant_a"]["entities"][i]["identifier"]:
                            DatabaseID = data["participant_a"]["entities"][i]["identifier"]
                            ElementID = data["participant_a"]["entities"][i]["identifier"]
                        else:
                            DatabaseID = None
                            ElementID = None

                        # Place those fields into comma-separated lists between parentheses
                        if i == 0:
                            Row.NegRegComponents = "("
                            Row.NegRegType = "("
                            Row.NegRegDatabaseID = "("
                            Row.NegRegElementID = "("
                        elif i <= len(data["participant_a"]["entities"]) - 1:
                            Row.NegRegComponents += ","
                            Row.NegRegType += ","
                            Row.NegRegDatabaseID += ","
                            Row.NegRegElementID += ","

                        Row.NegRegComponents += ElementName
                        Row.NegRegType += ElementType
                        Row.NegRegDatabaseID += DatabaseID
                        Row.NegRegElementID += ElementID
                        
                        if i == len(data["participant_a"]["entities"]) - 1:
                            Row.NegRegComponents += ")"
                            Row.NegRegType += ")"
                            Row.NegRegDatabaseID += ")"
                            Row.NegRegElementID += ")"
                            
                elif "entities" not in data["participant_a"]:
                    print("Warning in file " + filePath + " ... no field 'entities' found in object 'participant_a'.")            

            # Check to see if the element is a protein family
            elif "entity_type" in data["participant_a"] and data["participant_a"]["entity_type"] == "protein_family":
                # If the element is a protein family, do the following

                Row.NegRegType = "Protein family"

                # Extract the protein family name
                if "entity_text" in data["participant_a"]:
                    Row.NegRegName = data["participant_a"]["entity_text"][0]
                else:
                    print("Warning in file " + filePath + " ... no field 'entity_text' found in object 'participant_a'.")

                # Store the data from each listed entity in a comma-separated list between parentheses
                if "entities" in data["participant_a"] and len(data["participant_a"]["entities"]) > 0:
                    for i in range(len(data["participant_a"]["entities"])):
                        # Check to see if the required fields exist in each entity
                        if "entity_text" in data["participant_a"]["entities"][i]:
                            ElementName = data["participant_a"]["entities"][i]["entity_text"][0]
                        else:
                            ElementName = None

                        if "identifier" in data["participant_a"]["entities"][i] and ':' in data["participant_a"]["entities"][i]["identifier"]:
                            DatabaseID = data["participant_a"]["entities"][i]["identifier"][:data["participant_a"]["entities"][i]["identifier"].index(':')]
                            ElementID = data["participant_a"]["entities"][i]["identifier"][data["participant_a"]["entities"][i]["identifier"].index(':')+1:]
                        elif "identifier" in data["participant_a"]["entities"][i] and ':' not in data["participant_a"]["entities"][i]["identifier"]:
                            DatabaseID = data["participant_a"]["entities"][i]["identifier"]
                            ElementID = data["participant_a"]["entities"][i]["identifier"]
                        else:
                            DatabaseID = None
                            ElementID = None

                        # Place those fields into comma-separated lists between parentheses
                        if i == 0:
                            Row.NegRegComponents = "{"
                            Row.NegRegDatabaseID = "{"
                            Row.NegRegElementID = "{"
                        elif i <= len(data["participant_a"]["entities"]) - 1:
                            Row.NegRegComponents += ","
                            Row.NegRegDatabaseID += ","
                            Row.NegRegElementID += ","

                        Row.NegRegComponents += ElementName
                        Row.NegRegDatabaseID += DatabaseID
                        Row.NegRegElementID += ElementID
                        
                        if i == len(data["participant_a"]["entities"]) - 1:
                            Row.NegRegComponents += "}"
                            Row.NegRegDatabaseID += "}"
                            Row.NegRegElementID += "}"
                            
                elif "entities" not in data["participant_a"]:
                    print("Warning in file " + filePath + " ... no field 'entities' found in object 'participant_a'.")    

            # If the element is neither, do the following
            elif "entity_type" in data["participant_a"]:
                # The element is neither a complex nor a protein family
                if "entity_text" in data["participant_a"]:
                    Row.NegRegName = data["participant_a"]["entity_text"][0]
                    Row.NegRegComponents = Row.NegRegName
                    Row.NegRegType = data["participant_a"]["entity_type"]
                    if "identifier" in data["participant_a"] and ':' in data["participant_a"]["identifier"]:
                        Row.NegRegDatabaseID = data["participant_a"]["identifier"][:data["participant_a"]["identifier"].index(':')]
                        Row.NegRegElementID = data["participant_a"]["identifier"][data["participant_a"]["identifier"].index(':')+1:]
                    elif "identifier" in data["participant_a"] and ':' not in data["participant_a"]["identifier"]:
                        Row.NegRegDatabaseID = data["participant_a"]["identifier"]
                        Row.NegRegElementID = data["participant_a"]["identifier"]

            # Alert the user if no "entity_type" field is found
            elif "entity_type" not in data["participant_a"]:
                print("Warning in file " + filePath + " ... no field 'entity_type' found in object 'participant_a'.")

        elif "interaction_type" not in data:
            print("Warning in file " + filePath + " ... no field 'interaction_type' found in object 'interaction'.")
    else:
        print("Warning in file " + filePath + " ... no field 'participant_a' found in object 'interaction'.")

    # Return the translated data
    return Row
# end translateMITRE

# getMITREParticipantInformation takes either participant_a or participant_b and outputs an
# instance of a class with Name, Type, DatabaseID, and ElementID fields, properly formatted
# for complexes, etc.
# The input variable "filePath" is for warning messages only
# This function is not suitable for when the participant contains a nested reaction, as
# nested reactions in one participant may influence data for BOTH the regulator and
# regulated element
def getMITREParticipantInformation(participant, filePath):
    # Initialize the participant's data as an instance of the class Participant
    data = Participant()

    if "participant_a" in participant or "participant_b" in participant:
        print("Error in file " + filePath + " ... cannot handle nested reactions with function getMITREParticipantInformation.")

    # Check to see if the element is a complex
    if "entity_type" in participant and participant["entity_type"] == "complex":
        # If the element is a complex, do the following

        # Extract the complex name
        if "entity_text" in participant:
            data.Name = participant["entity_text"][0]
        else:
            print("Warning in file " + filePath + " ... no field 'entity_text' found in object 'participant_a'.")

        # Store the data from each listed entity in a comma-separated list between parentheses
        if "entities" in participant and len(participant["entities"]) > 0:           
            for i in range(len(participant["entities"])):
                # Check to see if the required fields exist in each entity
                if "entity_text" in participant["entities"][i]:
                    ElementName = participant["entities"][i]["entity_text"][0]
                else:
                    ElementName = None

                if "entity_type" in participant["entities"][i]:
                    ElementType = participant["entities"][i]["entity_type"]
                else:
                    ElementType = None

                if "identifier" in participant["entities"][i] and ':' in participant["entities"][i]["identifier"]:
                    DatabaseID = participant["entities"][i]["identifier"][:participant["entities"][i]["identifier"].index(':')]
                    ElementID = participant["entities"][i]["identifier"][participant["entities"][i]["identifier"].index(':')+1:]
                elif "identifier" in participant["entities"][i] and ':' not in participant["entities"][i]["identifier"]:
                    DatabaseID = participant["entities"][i]["identifier"]
                    ElementID = participant["entities"][i]["identifier"]
                else:
                    DatabaseID = None
                    ElementID = None

                # Place those fields into comma-separated lists between parentheses
                if i == 0:
                    data.Components = "("
                    data.Type = "("
                    data.DatabaseID = "("
                    data.ElementID = "("
                elif i <= len(participant["entities"]) - 1:
                    data.Components += ","
                    data.Type += ","
                    data.DatabaseID += ","
                    data.ElementID += ","

                data.Components += ElementName
                data.Type += ElementType
                data.DatabaseID += DatabaseID
                data.ElementID += ElementID
                
                if i == len(participant["entities"]) - 1:
                    data.Components += ")"
                    data.Type += ")"
                    data.DatabaseID += ")"
                    data.ElementID += ")"
                    
        elif "entities" not in participant:
            print("Warning in file " + filePath + " ... no field 'entities' found in object 'participant_a'.")            

    # Check to see if the element is a protein family
    elif "entity_type" in participant and participant["entity_type"] == "protein_family":
        # If the element is a protein family, do the following

        data.Type = "Protein family"

        # Extract the protein family name
        if "entity_text" in participant:
            data.Name = participant["entity_text"][0]
        else:
            print("Warning in file " + filePath + " ... no field 'entity_text' found in object 'participant_a'.")

        # Store the data from each listed entity in a comma-separated list between parentheses
        if "entities" in participant and len(participant["entities"]) > 0:
            for i in range(len(participant["entities"])):
                # Check to see if the required fields exist in each entity
                if "entity_text" in participant["entities"][i]:
                    ElementName = participant["entities"][i]["entity_text"][0]
                else:
                    ElementName = None

                if "identifier" in participant["entities"][i] and ':' in participant["entities"][i]["identifier"]:
                    DatabaseID = participant["entities"][i]["identifier"][:participant["entities"][i]["identifier"].index(':')]
                    ElementID = participant["entities"][i]["identifier"][participant["entities"][i]["identifier"].index(':')+1:]
                elif "identifier" in participant["entities"][i] and ':' not in participant["entities"][i]["identifier"]:
                    DatabaseID = participant["entities"][i]["identifier"]
                    ElementID = participant["entities"][i]["identifier"]
                else:
                    DatabaseID = None
                    ElementID = None

                # Place those fields into comma-separated lists between parentheses
                if i == 0:
                    data.Components = "{"
                    data.DatabaseID = "{"
                    data.ElementID = "{"
                elif i <= len(participant["entities"]) - 1:
                    data.Components += ","
                    data.DatabaseID += ","
                    data.ElementID += ","

                data.Components += ElementName
                data.DatabaseID += DatabaseID
                data.ElementID += ElementID
                
                if i == len(participant["entities"]) - 1:
                    data.Components += "}"
                    data.DatabaseID += "}"
                    data.ElementID += "}"
                    
        elif "entities" not in participant:
            print("Warning in file " + filePath + " ... no field 'entities' found in object 'participant_a'.")    

    # If the element is neither, do the following
    elif "entity_type" in participant:
        # The element is neither a complex nor a protein family
        if "entity_text" in participant:
            data.Name = participant["entity_text"][0]
            data.Components = data.Name
            data.Type = participant["entity_type"]
            if "identifier" in participant and ':' in participant["identifier"]:
                data.DatabaseID = participant["identifier"][:participant["identifier"].index(':')]
                data.ElementID = participant["identifier"][participant["identifier"].index(':')+1:]
            elif "identifier" in participant and ':' not in participant["identifier"]:
                data.DatabaseID = participant["identifier"]
                data.ElementID = participant["identifier"]

    # Alert the user if no "entity_type" field is found
    elif "entity_type" not in participant:
        print("Warning in file " + filePath + " ... no field 'entity_type' found in object 'participant_a'.")
        # The element is neither a complex nor a protein family and does not contain a "entity_type" field
        if "entity_text" in participant:
            data.Name = participant["entity_text"][0]
            data.Components = data.Name
            if "identifier" in participant and ':' in participant["identifier"]:
                data.DatabaseID = participant["identifier"][:participant["identifier"].index(':')]
                data.ElementID = participant["identifier"][participant["identifier"].index(':')+1:]
            elif "identifier" in participant and ':' not in participant["identifier"]:
                data.DatabaseID = participant["identifier"]
                data.ElementID = participant["identifier"]

    return data
# end getMITREParticipantInformation

# getMITRENestedReactionParticipants accepts two participants as inputs and outputs
# a list of those participants' data, correctly formatted for the Pitt formalism
# The input is the "interaction" field containing participant_a and participant_b
# The input "filePath" is for error reporting only
# The input modelData is the instance of class PittRow in which to insert data
def getMITRENestedReactionParticipants(interaction, modelData, filePath):
    # How a nested interaction is handled will depend on whether or not it is in participant_a
    # or participant_b, as well as on the type of interaction exhibited

    # First, we make the assumption that all nested interactions occur in participant_b (the
    # regulated element) and throw an error if otherwise

    nested_a = {}
    nested_b = {}

    if "participant_a" in interaction["participant_a"]:
        print("Error in file " + filePath + " ... Unable to process nested reactions in participant_a.")
        return modelData

    if "negative_information" in interaction["participant_b"] and interaction["participant_b"]["negative_information"] == "true":
            # If "negative_information" is set to true, discard this data, as this reaction evidently does NOT occur
            return modelData

    # Get the overall regulator's data
    if "participant_a" in interaction:
        participant_a = getMITREParticipantInformation(interaction["participant_a"], filePath)
##        print(participant_a.Name)
##        print(participant_a.Components)
##        print(participant_a.Type)
##        print(participant_a.DatabaseID)
##        print(participant_a.ElementID)
    # Copy the nested regulator's information
    if "participant_a" in interaction["participant_b"] and interaction["participant_b"]["participant_a"]["entity_text"][0] != "":
        nested_a = interaction["participant_b"]["participant_a"]
    # Copy the nested regulated element's information
    if "participant_b" in interaction["participant_b"]:
        nested_b = interaction["participant_b"]["participant_b"]
    # Collect information on the type of regulation in the main (non-nested) reaction
    if "interaction_type" in interaction and interaction["interaction_type"] == "decreases":
        RegulatorIsNegative = True
    else:
        RegulatorIsNegative = False

    if "interaction_type" in interaction["participant_b"] and interaction["participant_b"]["interaction_type"] == "binds":
        # If the nested reaction is of type "binds", procees as follows:

        if RegulatorIsNegative:
            modelData.NegRegName = participant_a.Name
            modelData.NegRegComponents = participant_a.Components
            modelData.NegRegType = participant_a.Type
            modelData.NegRegDatabaseID = participant_a.DatabaseID
            modelData.NegRegElementID = participant_a.ElementID
            modelData.MechanismType = "Binding,Negative regulation"
        else:
            modelData.PosRegName = participant_a.Name
            modelData.PosRegComponents = participant_a.Components
            modelData.PosRegType = participant_a.Type
            modelData.PosRegDatabaseID = participant_a.DatabaseID
            modelData.PosRegElementID = participant_a.ElementID
            modelData.MechanismType = "Binding,Positive regulation"
            
        if nested_a != {} and nested_b != {}:
            # Do the following if there is both a nested participant_a and a nested participant_b
            aData = getMITREParticipantInformation(nested_a, filePath)
            bData = getMITREParticipantInformation(nested_b, filePath)
            
            modelData.ElementName = "(" + aData.Name + "," + bData.Name + ")"
            modelData.ElementComponents = "(" + aData.Components + "," + bData.Components + ")"
            modelData.Type = "(" + aData.Type + "," + bData.Type + ")"
            modelData.DatabaseID = "(" + aData.DatabaseID + "," + bData.DatabaseID + ")"
            modelData.ElementID = "(" + aData.ElementID + "," + bData.ElementID + ")"
    
        elif nested_a == {} and nested_b != {}:
            # Do the following if a nested participant_a is missing
            bData = getMITREParticipantInformation(nested_b, filePath)

            modelData.ElementName = bData.Name
            modelData.ElementComponents = bData.Components
            modelData.Type = bData.Type
            modelData.DatabaseID = bData.DatabaseID
            modelData.ElementID = bData.ElementID
            
        else:
            # If both nested participants are missing or participant_a is the only one, return empty data
            print("Error in file " + filePath + " ... Nested reaction must contain field 'participant_b'.")
            return modelData
            
    elif "interaction_type" in interaction["participant_b"] and (interaction["participant_b"]["interaction_type"] == "adds_modification" or interaction["participant_b"]["interaction_type"] == "removes_modification"):
        # If the nested reaction is of type "adds_modification" or "removes_modification", procees as follows:

        # Determine whether the regulator is positive or negative based on interaction type and nested modification type
        if "modifications" in interaction["participant_b"] and len(interaction["participant_b"]["modifications"]) > 0:
            if interaction["participant_b"]["modifications"][0]["modification_type"] == "ubiquitination":
                # Ubiquitination implies a negative regulator, unless this nested reaction is being removed                
                if interaction["participant_b"]["interaction_type"] == "adds_modification":
                    RegulatorIsNegative = True
                if interaction["participant_b"]["interaction_type"] == "removes_modification":
                    RegulatorIsNegative = False
            else:
                # Everything else implies a positive regulator, unless the nested reaction is being removed
                if interaction["participant_b"]["interaction_type"] == "adds_modification":
                    RegulatorIsNegative = False
                if interaction["participant_b"]["interaction_type"] == "removes_modification":
                    RegulatorIsNegative = True

        elif "modifications" not in interaction["participant_b"] and interaction["participant_b"]["interaction_type"] == "adds_modification":
            # Default to positive regulation if no modification type is present but interaction type is "adds_modification"
            RegulatorIsNegative = False            
        elif "modifications" not in interaction["participant_b"] and interaction["participant_b"]["interaction_type"] == "removess_modification":
            # Default to negative regulation if no modification type is present but interaction type is "removes_modification"
            RegulatorIsNegative = True

        if nested_b != {}:
            bData = getMITREParticipantInformation(nested_b, filePath)
##
##            print("WHAETAKSDHJTGA!!!!")
##            print(bData.Name)
##            print(bData.Components)
##            print(bData.Type)
##            print(bData.DatabaseID)
##            print(bData.ElementID)
            
            modelData.ElementName = bData.Name
            modelData.ElementComponents = bData.Components
            modelData.Type = bData.Type
            modelData.DatabaseID = bData.DatabaseID
            modelData.ElementID = bData.ElementID
        else:
            print("Error in file " + filePath + " ... Nested reaction must contain field 'participant_b'.")
            return modelData

        modificationType = interaction["participant_b"]["modifications"][0]["modification_type"]
            
        if "interaction_type" in interaction and interaction["interaction_type"] == "increases":
            modelData.MechanismType = modificationType + "," + "Increases"
            Increases = True
        elif "interaction_type" in interaction and interaction["interaction_type"] == "decreases":
            modelData.MechanismType = modificationType + "," + "Decreases"
            Increases = False
        elif "interaction_type" in interaction:
            modelData.MechanismType = modificationType + "," + interaction["interaction_type"]
            Increases = True
        elif "interaction_type" not in interaction:
            print("Warning in file " + filePath + " ... No field 'interaction_type' found in object 'interaction'")
            modelData.MechanismType = modificationType + "," + "Unknown"
            Increases = True
            
        if nested_a != {}:
            # Do the following if there is both a nested participant_a and a nested participant_b
            aData = getMITREParticipantInformation(nested_a, filePath)                      
            
            if RegulatorIsNegative and not Increases:
                # Both the overall and nested regulators are negative
                modelData.NegRegName = "{" + aData.Name + "}[" + participant_a.Name + "]"
                modelData.NegRegComponents = "{" + aData.Components + "}[" + participant_a.Components + "]"
                modelData.NegRegType = "{" + aData.Type + "}[" + participant_a.Type + "]"
                modelData.NegRegDatabaseID = "{" + aData.DatabaseID + "}[" + participant_a.DatabaseID + "]"
                modelData.NegRegElementID = "{" + aData.ElementID + "}[" + participant_a.ElementID + "]"
                
            elif RegulatorIsNegative and Increases:
                # The overall regulator is positive but the nested regulator is negative
                modelData.NegRegName = aData.Name
                modelData.NegRegComponents = aData.Components
                modelData.NegRegType = aData.Type
                modelData.NegRegDatabaseID = aData.DatabaseID
                modelData.NegRegElementID = aData.ElementID

                modelData.PosRegName = participant_a.Name
                modelData.PosRegComponents = participant_a.Components
                modelData.PosRegType = participant_a.Type
                modelData.PosRegDatabaseID = participant_a.DatabaseID
                modelData.PosRegElementID = participant_a.ElementID
                
            elif not RegulatorIsNegative and not Increases:
                # The overall regulator is negative but the nested regulator is positive
                modelData.NegRegName = participant_a.Name
                modelData.NegRegComponents = participant_a.Components
                modelData.NegRegType = participant_a.Type
                modelData.NegRegDatabaseID = participant_a.DatabaseID
                modelData.NegRegElementID = participant_a.ElementID

                modelData.PosRegName = aData.Name
                modelData.PosRegComponents = aData.Components
                modelData.PosRegType = aData.Type
                modelData.PosRegDatabaseID = aData.DatabaseID
                modelData.PosRegElementID = aData.ElementID

            elif not RegulatorIsNegative and Increases:
                # Both the overall and nested regulators are positive
                modelData.PosRegName = "{" + aData.Name + "}[" + participant_a.Name + "]"
                modelData.PosRegComponents = "{" + aData.Components + "}[" + participant_a.Components + "]"
                modelData.PosRegType = "{" + aData.Type + "}[" + participant_a.Type + "]"
                modelData.PosRegDatabaseID = "{" + aData.DatabaseID + "}[" + participant_a.DatabaseID + "]"
                modelData.PosRegElementID = "{" + aData.ElementID + "}[" + participant_a.ElementID + "]"
    
        elif nested_a == {}:
            # Do the following if a nested participant_a is missing
            bData = getMITREParticipantInformation(nested_b, filePath)

            if RegulatorIsNegative and not Increases:
                # Both the overall and nested regulators are negative
                modelData.NegRegName = participant_a.Name
                modelData.NegRegComponents = participant_a.Components
                modelData.NegRegType = participant_a.Type
                modelData.NegRegDatabaseID = participant_a.DatabaseID
                modelData.NegRegElementID = participant_a.ElementID
                
            elif RegulatorIsNegative and Increases:
                # The overall regulator is positive but the nested regulator is negative
                modelData.PosRegName = participant_a.Name
                modelData.PosRegComponents = participant_a.Components
                modelData.PosRegType = participant_a.Type
                modelData.PosRegDatabaseID = participant_a.DatabaseID
                modelData.PosRegElementID = participant_a.ElementID
                
            elif not RegulatorIsNegative and not Increases:
                # The overall regulator is negative but the nested regulator is positive
                modelData.NegRegName = participant_a.Name
                modelData.NegRegComponents = participant_a.Components
                modelData.NegRegType = participant_a.Type
                modelData.NegRegDatabaseID = participant_a.DatabaseID
                modelData.NegRegElementID = participant_a.ElementID
                
            elif RegulatorIsNegative and not Increases:
                # Both the overall and nested regulators are positive
                modelData.PosRegName = participant_a.Name
                modelData.PosRegComponents = participant_a.Components
                modelData.PosRegType = participant_a.Type
                modelData.PosRegDatabaseID = participant_a.DatabaseID
                modelData.PosRegElementID = participant_a.ElementID
            
        else:
            # If both nested participants are missing or participant_a is the only one, return empty data
            print("Error in file " + filePath + " ... Nested reaction must contain field 'participant_b'.")
            return modelData
 
    else:
        print("Error in file " + filePath + " ... Unsupported interaction type in nested reaction.")
        return modelData

    # Return the data
    return modelData
# end getMITRENestedReactionParticipants


# getComplexMembers takes a field containing a MITRE protein complex and returns a dictionary
# containing the properly formatted information found within that complex
def deprecatedGetComplexMembers(participant):
    data = {}
    
    # First, check to see if there really is actually only one entity
    if len(participant["entities"]) == 1:
        if "entity_text" in participant["entities"][0]:
            data["text"] = participant["entities"][0]["entity_text"][0]
        if "entity_type" in participant["entities"][0]:
            data["type"] = participant["entities"][0]["entity_type"]
        if "identifier" in participant["entities"][0]:
            if ":" in participant["entities"][0]["identifier"]:
                data["database"] = "{" + participant["entities"][0]["identifier"][:participant["entities"][0]["identifier"].index(':')]
                data["id"] = "{" + participant["entities"][0]["identifier"][participant["entities"][0]["identifier"].index(':') + 1:]
            else:
                data["database"] = "{" + participant["entities"][0]["identifier"]
                data["id"] = "{" + participant["entities"][0]["identifier"]
                               
    # If there is more than one entity, format as {entity1;entity2; ... ;entityN}
    else:
        for i in range(len(participant["entities"])):
            if i == 0:
                # Start with an opening bracket and the first entries
                if "entity_text" in participant["entities"][i]:
                    data["text"] = "{" + participant["entities"][i]["entity_text"][0]
                if "entity_type" in participant["entities"][i]:
                    data["type"] = "{" + participant["entities"][i]["entity_type"]
                if "identifier" in participant["entities"][i]:
                    if ":" in participant["entities"][i]["identifier"]:
                        data["database"] = "{" + participant["entities"][i]["identifier"][:participant["entities"][i]["identifier"].index(':')]
                        data["id"] = "{" + participant["entities"][i]["identifier"][participant["entities"][i]["identifier"].index(':') + 1:]
                    else:
                        data["database"] = "{" + participant["entities"][i]["identifier"]
                        data["id"] = "{" + participant["entities"][i]["identifier"]
                        
            if i > 0 and i < len(participant["entities"]):
                # Add a semicolon and the next entry
                if "entity_text" in participant["entities"][i]:
                    data["text"] += ";" + participant["entities"][i]["entity_text"][0]
                if "entity_type" in participant["entities"][i]:
                    data["type"] += ";" + participant["entities"][i]["entity_type"]
                if "identifier" in participant["entities"][i]:
                    if ":" in participant["entities"][i]["identifier"]:
                        data["database"] += ";" + participant["entities"][i]["identifier"][:participant["entities"][i]["identifier"].index(':')]
                        data["id"] += ";" + participant["entities"][i]["identifier"][participant["entities"][i]["identifier"].index(':') + 1:]
                    else:
                        data["database"] += ";" + participant["entities"][i]["identifier"]
                        data["id"] += ";" + participant["entities"][i]["identifier"]
                        
            if i == len(participant["entities"]) - 1:
                # Add a closing bracket to each category
                data["text"] += "}"
                data["type"] += "}"
                data["database"] += "}"
                data["id"] += "}"
            
    return data
# end getComplexMembers

def translateMultipleMITRE(JSONFolderPath):
    # Make a list of files in the current directory
    fileList = listdir(JSONFolderPath)

    # Create an empty array in which to store the Pitt model data as we translate
    modelData = [None] * len(fileList)

    for i in range(len(modelData)):
        if checkFormat(JSONFolderPath + "\\" + fileList[i]) == "MITRE":
            modelData[i] = translateMITRE(JSONFolderPath + "\\" + fileList[i])
        else:
            print("Warning: the file at path " + fileList[i] + " is not a valid MITRE file and was not translated.")        

    # Return the translated data
    return modelData
# end translateMultipleMITRE

# loadEntities loads a JSON file at a specified path filePath and directory.
# If the file does not exist at that path and directory, a warning is printed.
def loadEntities(filePath, directory):
    import json
    try:
        with open(str(directory) + '\\' + filePath) as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print("The file " + filePath + " does not exist.")
# end loadEntities

# translateFRIES translates the JSON data in FRIES format at the path filePath
# and returns it.
def deprecatedTranslateFRIES(filePath):
    with open(filePath) as FRIESData:
        data = json.load(FRIESData)

    # For simplicity, limit data to frames and not meta information
    data = data["frames"]
    # Create an empty array in which to store the Pitt model data as we translate
    modelData = [None] *len(data)

    for i in range(len(data)):
        modelData[i] = [None] * 46

    for i in range(len(data)):
        if len(data[i]["arguments"]) == 1:
            # Make this the element under study
            modelData[i][4] = data[i]["arguments"][0]["text"]
            # Name the event taking place (e.g. "phosphorylation")
            modelData[i][35] = data[i]["subtype"]
            # Extract "entity-mention" ID for later analysis
            modelData[i][44] = data[i]["arguments"][0]["arg"]
        else:
            for j in range(len(data[i]["arguments"])):
                if data[i]["arguments"][j]["type"] == "controlled":
                    # Make this the element under study
                    modelData[i][4] = data[i]["arguments"][j]["text"]
                    if "arg" in data[i]["arguments"][j]:
                        modelData[i][44] = data[i]["arguments"][j]["arg"]
                elif data[i]["arguments"][j]["type"] == "controller":
                    # Make this the regulator, depending on event type/subtype
                    if data[i]["subtype"] == "positive-activation" or data[i]["subtype"] == "positive-regulation":
                        modelData[i][32] = data[i]["arguments"][j]["text"]
                        modelData[i][35] = "positive activation"
                    elif data[i]["subtype"] == "negative-activation" or data[i]["subtype"] == "negative-regulation":
                        modelData[i][33] = data[i]["arguments"][j]["text"]
                        modelData[i][35] = "negative activation"
                    else:
                        modelData[i][32] = data[i]["arguments"][j]["text"]
                        modelData[i][35] = data[i]["subtype"]
                    # Extract the "entity-mention" ID of this regulator for later analysis
                    if "arg" in data[i]["arguments"][j]:
                        modelData[i][45] = data[i]["arguments"][j]["arg"]
                elif data[i]["arguments"][j]["type"] == "theme":
                    # Handle unusual "theme" and "site" types based on order of appearance
                    if j == 0:
                        # Make the first "theme" the primary element
                        modelData[i][4] = data[i]["arguments"][j]["text"]
                        if "arg" in data[i]["arguments"][j]:
                            modelData[i][44] = data[i]["arguments"][j]["arg"]
                    if j == 1 and data[i]["arguments"][0]["type"] != "site":
                        modelData[i][32] = data[i]["arguments"][j]["text"]
                        modelData[i][35] = data[i]["arguments"][j]["type"]
                    if j == 1 and data[i]["arguments"][0]["type"] == "site":
                        # Make the first "theme" the primary element
                        modelData[i][4] = data[i]["arguments"][j]["text"]
                        if "arg" in data[i]["arguments"][j]:
                            modelData[i][44] = data[i]["arguments"][j]["arg"]
                elif data[i]["arguments"][j]["type"] == "site":
                    if len(data[i]["arguments"][j]) < 3:
                        # A "site" only affects the mechanism description. 
                        modelData[i][35] = data[i]["arguments"][0]["subtype"]                        
                
        # Extract PubMed reference
        modelData[i][42] = data[i]["frame-id"][data[i]["frame-id"].index("PMC"):data[i]["frame-id"][data[i]["frame-id"].index("PMC"):].index("-") + data[i]["frame-id"].index("PMC")]
        # Extract "context" ID for later analysis
        modelData[i][43] = data[i]["context"]

    # return the translated data
    return modelData
# end translateFRIES
# DEPRECATED

def translateFRIES(filePath):
    with open(filePath) as FRIESData:
        data = json.load(FRIESData)

    # For simplicity, limit data to frames and not meta information
    data = data["frames"]
    # Create an empty array in which to store the Pitt model data as we translate
    modelData = [None] *len(data)

    for i in range(len(data)):
        modelData[i] = PittRow()

    for i in range(len(data)):
        if "frame-id" in data[i]:
            modelData[i].IndexCardID = data[i]["frame-id"]
        
        if len(data[i]["arguments"]) == 1:
            # Make this the element under study
            modelData[i].ElementName = data[i]["arguments"][0]["text"]
            modelData[i].ElementComponents = modelData[i].ElementName
            # Name the event taking place (e.g. "phosphorylation")
            modelData[i].MechanismType = data[i]["subtype"]
            # Extract "entity-mention" ID for later analysis
            modelData[i].ElementEntityMentionID = data[i]["arguments"][0]["arg"]
        else:
            for j in range(len(data[i]["arguments"])):
                if data[i]["arguments"][j]["type"] == "controlled":
                    # Make this the element under study
                    modelData[i].ElementName = data[i]["arguments"][j]["text"]
                    modelData[i].ElementComponents = modelData[i].ElementName
                    if "arg" in data[i]["arguments"][j]:
                        modelData[i].ElementEntityMentionID = data[i]["arguments"][j]["arg"]
                elif data[i]["arguments"][j]["type"] == "controller":
                    # Make this the regulator, depending on event type/subtype
                    if data[i]["subtype"] == "positive-activation" or data[i]["subtype"] == "positive-regulation":
                        modelData[i].PosRegName = data[i]["arguments"][j]["text"]
                        modelData[i].PosRegComponents = modelData[i].PosRegName
                        modelData[i].MechanismType = "positive activation"
                    elif data[i]["subtype"] == "negative-activation" or data[i]["subtype"] == "negative-regulation":
                        modelData[i].NegRegName = data[i]["arguments"][j]["text"]
                        modelData[i].NegRegComponents = modelData[i].NegRegName
                        modelData[i].MechanismType = "negative activation"
                    else:
                        modelData[i].PosRegName = data[i]["arguments"][j]["text"]
                        modelData[i].PosRegComponents = modelData[i].PosRegName
                        modelData[i].MechanismType = data[i]["subtype"]
                    # Extract the "entity-mention" ID of this regulator for later analysis
                    if "arg" in data[i]["arguments"][j]:
                        modelData[i].RegEntityMentionID = data[i]["arguments"][j]["arg"]
                elif data[i]["arguments"][j]["type"] == "theme":
                    # Handle "theme" and "site" types based on order of appearance
                    if j == 0:
                        # Make the first "theme" the primary element
                        modelData[i].ElementName = data[i]["arguments"][j]["text"]
                        modelData[i].ElementComponents = modelData[i].ElementName
                        # Extract entity-mention ID
                        if "arg" in data[i]["arguments"][j]:
                            modelData[i].ElementEntityMentionID = data[i]["arguments"][j]["arg"]
                        # Also note the mechanism type
                        if "type" in data[i]:
                            if data[i]["type"] == "complex-assembly":
                                modelData[i].MechanismType = "Complex assembly"
                            else:
                                modelData[i].MechanismType = data[i]["type"]
                        else:
                            print("Warning in frame " + str(i) + " - no field 'type' found.")
                    if j == 1 and data[i]["arguments"][0]["type"] != "site":
                        # Make the second "theme" the regulator
                        modelData[i].PosRegName = data[i]["arguments"][j]["text"]
                        modelData[i].PosRegComponents = modelData[i].PosRegName
                        modelData[i].MechanismType = data[i]["type"]
                    if j == 1 and data[i]["arguments"][0]["type"] == "site":
                        # Make the first "theme" the primary element
                        modelData[i].ElementName = data[i]["arguments"][j]["text"]
                        modelData[i].ElementComponents = modelData[i].ElementName
                        if "arg" in data[i]["arguments"][j]:
                            modelData[i].ElementEntityMentionID = data[i]["arguments"][j]["arg"]
                    if j == 2 and data[i]["arguments"][0]["type"] == "site":
                        # Make the second "theme" the regulator
                        modelData[i].PosRegName = data[i]["arguments"][j]["text"]
                        modelData[i].PosRegComponents = modelData[i].PosRegName
                        modelData[i].MechanismType = data[i]["type"]
                elif data[i]["arguments"][j]["type"] == "site":
                    # Record the site name in the "site" field
                    modelData[i].ElementSite = data[i]["arguments"][j]["text"]        
                
        # Extract PubMed reference
        if "frame-id" in data[i]:
            modelData[i].PaperID = data[i]["frame-id"][data[i]["frame-id"].index("PMC"):data[i]["frame-id"][data[i]["frame-id"].index("PMC"):].index("-") + data[i]["frame-id"].index("PMC")]
        else:
            print("Warning in frame " + str(i) + " - No field 'frame-id' found.")
            
        # Extract "context" ID for later analysis
        if "context" in data[i]:
            modelData[i].ElementContextID = data[i]["context"]
        else:
            # Uncomment the following line to enable this warning, whose frequent occurence may slow
            # execution of the translator.
            #print("Warning in frame " + str(i) + " - No field 'context' found.")
            pass

    # return the translated data
    return modelData
# end translateFRIES

# addContextAndEntityInformation adds linked context and entity data to that
# contained in modelData from the file contextFilePath
def addContextAndEntityInfo(modelData, contextFilePath):
    # Compare with entity and context information
    try:
        with open(str(contextFilePath)) as file:
            data = json.load(file)
    except FileNotFoundError:
        print("The file " + filePath + " does not exist.")
        return modelData
    
    frames = data["frames"]

    frameTypes = [None] * len(frames)
    typeListing = {}
    for i in range(len(frames)):
        frameTypes[i] = frames[i]["frame-type"]
        if frameTypes[i] not in typeListing:
            typeListing[frameTypes[i]] = 1
        else:
            typeListing[frameTypes[i]] += 1

    contexts = [None] * typeListing["context"]
    entities = [None] * typeListing["entity-mention"]

    j = 0
    k = 0
    for i in range(len(frames)):
        if frames[i]["frame-type"] == "context":
            contexts[j] = frames[i]
            j += 1
        elif frames[i]["frame-type"] == "entity-mention":
            entities[k] = frames[i]
            k += 1

    contextIndices = {}
    for i in range(len(contexts)):
        contextIndices[contexts[i]["frame-id"]] = i
    entityIndices = {}
    for i in range(len(entities)):
        entityIndices[entities[i]["frame-id"]] = i

    # Place context and entity information into model
    for i in range(len(modelData)):
        # Begin by placing entity information into the model
        if modelData[i].ElementEntityMentionID in entityIndices:
            thisEntity = entities[entityIndices[modelData[i].ElementEntityMentionID]]
            # Extract element type
            modelData[i].ElementType = thisEntity["type"]

            # Extract other useful information about the element
            modelData[i].ElementDatabaseID = thisEntity["xrefs"][0]["namespace"]
            if ":" in thisEntity["xrefs"][0]["id"]:
                modelData[i].ElementElementID = thisEntity["xrefs"][0]["id"][thisEntity["xrefs"][0]["id"].index(":")+1:]
            else:
                modelData[i].ElementElementID = thisEntity["xrefs"][0]["id"]
                
            # Use the entity's context ID if event context is unavailable
            contextAvailable = False
            availableContextIndex = 0
            if modelData[i].ElementContextID != None:
                for j in range(len(modelData[i].ElementContextID)):
                    if modelData[i].ElementContextID[j] in contextIndices:
                        contextAvailable = True
                        availableContextIndex = j
            if not contextAvailable and "context" in thisEntity:
                modelData[i].ElementContextID = thisEntity["context"]

        # Also place POSITIVE regulator entity information into the model
        if modelData[i].PosRegName != None and modelData[i].RegEntityMentionID in entityIndices:
            thisEntity = entities[entityIndices[modelData[i].RegEntityMentionID]]
            # Extract POSITIVE regulator type
            modelData[i].PosRegType = thisEntity["type"]

            # Extract other useful information about the POSITIVE regulator
            modelData[i].PosRegDatabaseID = thisEntity["xrefs"][0]["namespace"]
            if ":" in thisEntity["xrefs"][0]["id"]:
                modelData[i].PosRegElementID = thisEntity["xrefs"][0]["id"][thisEntity["xrefs"][0]["id"].index(":")+1:]
            else:
                modelData[i].PosRegElementID = thisEntity["xrefs"][0]["id"]

        # Also place NEGATIVE regulator entity information into the model
        elif modelData[i].NegRegName != None and modelData[i].RegEntityMentionID in entityIndices:
            thisEntity = entities[entityIndices[modelData[i].RegEntityMentionID]]
            # Extract NEGATIVE regulator type
            modelData[i].NegRegType = thisEntity["type"]

            # Extract other useful information about the NEGATIVE regulator
            modelData[i].NegRegDatabaseID = thisEntity["xrefs"][0]["namespace"]
            if ":" in thisEntity["xrefs"][0]["id"]:
                modelData[i].NegRegElementID = thisEntity["xrefs"][0]["id"][thisEntity["xrefs"][0]["id"].index(":")+1:]
            else:
                modelData[i].NegRegElementID = thisEntity["xrefs"][0]["id"]    

        # Place context information into model
        if modelData[i].ElementContextID != None and modelData[i].ElementContextID[availableContextIndex] in contextIndices:
            thisContext = contexts[contextIndices[modelData[i].ElementContextID[availableContextIndex]]]
            # Set cell line and remove superfluous characters
            if "cell-line" in thisContext["facets"]:
                modelData[i].ElementCellLine = thisContext["facets"]["cell-line"][0]
                if modelData[i].ElementCellLine.count(":") > 1:
                    modelData[i].ElementCellLine = modelData[i].ElementCellLine[modelData[i].ElementCellLine.index(":") + 1:]
            # Set cell type and remove superfluous characters
            if "cell-type" in thisContext["facets"]:
                modelData[i].ElementCellType = thisContext["facets"]["cell-type"][0]
                if modelData[i].ElementCellType.count(":") > 1:
                    modelData[i].ElementCellType = modelData[i].ElementCellType[modelData[i].ElementCellType.index(":") + 1:]
            # Set organism and remove superfluous characters
            if "organism" in thisContext["facets"]:
                modelData[i].ElementOrganism = thisContext["facets"]["organism"][0]
                if modelData[i].ElementOrganism.count(":") > 1:
                    modelData[i].ElementOrganism = modelData[i].ElementOrganism[modelData[i].ElementOrganism.index(":") + 1:]
            # Set tissue type and remove superfluous characters
            if "tissue-type" in thisContext["facets"]:
                modelData[i].ElementTissueType = thisContext["facets"]["tissue-type"][0]
                if modelData[i].ElementTissueType.count(":") > 1:
                    modelData[i].ElementTissueType = modelData[i].ElementTissueType[modelData[i].ElementTissueType.index(":") + 1:]

    # return the enhanced data
    return modelData
# end addContextAndEntityInfo

# translateMedScanFRIES translates JSON files in the MedScan FRIES format
def translateMedScanFRIES(filePath):
    # Load the JSON data from the MedScan FRIES file
    with open(filePath) as file:
        data = json.load(file)

    # Extract the PMC ID before continuing
    try:
        PMC_ID = data["object-meta"]["doc-id"]
    except Exception as e:
        print("Warning: could not obtain the document's PMC ID.")
        
    # For convenience, limit to frame information
    try:
        data = data["frames"]
    except Exception as e:
        print("Fatal error: could not access the document's frames.")
        return
                
    modelData = [None] * len(data)

    for i in range(len(data)):
        # Initialize this row of modelData
        modelData[i] = PittRow()

        try:
            # If the frame is a "relation" type, work differently
            #than if it is a "relation-mention" type
            if data[i]["frame-type"] == "relation":
                for j in range(len(data[i]["arguments"])):
                    try:
                        if data[i]["arguments"][j]["type"] == "participant-a":
                            # This entity is the regulator - label it as positive, as
                            # MedScan does not always specify a clear mechanism type
                            modelData[i].PosRegName = data[i]["arguments"][j]["arg"]
                    except Exception as e:
                        print("Regulator not found for frame " + str(i) + ".")

                    try:
                        if data[i]["arguments"][j]["type"] == "participant-b":
                            # This entity is the primary element
                            modelData[i].ElementName = data[i]["arguments"][j]["arg"]
                    except Exception as e:
                        print("Regulated element not found for frame " + str(i) + ".")

                    # Make the frame's "type" field into the mechanism
                    try:
                        modelData[i].MechanismType = data[i]["type"]
                    except Exception as e:
                        print("No mechanism type found for frame " + str(i) + ".")

            elif data[i]["frame-type"] == "relation-mention":
                for j in range(len(data[i]["arguments"])):
                    try:
                        if data[i]["arguments"][j]["type"] == "participant-a":
                            # This entity is the regulator - label it as positive, as
                            # MedScan does not specify a mechanism type
                            modelData[i].PosRegName = data[i]["arguments"][j]["text"]
                    except Exception as e:
                        print("Regulator not found for frame " + str(i) + ".")

                    try:
                        if data[i]["arguments"][j]["type"] == "participant-b":
                            # This entity is the primary element
                            modelData[i].ElementName = data[i]["arguments"][j]["text"]
                    except Exception as e:
                        print("Regulated element not found for frame " + str(i) + ".")

##                    # Make the frame's "text" field into the mechanism
##                    try:
##                        modelData[i].MechanismType = data[i]["text"]
##                    except Exception as e:
##                        print("No mechanism type found for frame " + str(i) + ".")
        except:
            print("Error accessing frame type of frame " + str(i))
        # Set reference (PMC ID) field to previously obtained information
        modelData[i].PaperID = PMC_ID
        
    # Return the translated data
    return modelData
# end translateMedScanFRIES

# translateTRIPS translates from the TRIPS/DRUM output format, saved as 
# XML data in a .txt file, to the Pitt formalism.
def translateTRIPS(filePath):

    # Open the file and read data
    try:
      text_data = open(filePath,'r')
      ekb_data = text_data.read()
    except:
      print('ERROR: incompatible file format!')
      ekb_data = None

    # Main parsing functions
    if (ekb_data != None):
      
      trips_processor = TripsTranslator(ekb_data)
      trips_processor.xml_to_dict()
      trips_processor.refine_dict()
      term_dict, event_dict = trips_processor.get_dicts()

      trips_extractor = TreeExtractor(term_dict, event_dict)
      trips_extractor.condense_tree()
      trips_extractor.convert_tree()
      trips_extractor.finalize_melody()
      term_dict, event_dict, melody_dict = trips_extractor.get_dicts()

      # Fills modelData with values
      modelData = [None] * len(melody_dict)

      # Assigning data to modelData objects
      i = 0
      for element_id, attrib_dict in melody_dict.items():
        modelData[i] = PittRow()
        modelData[i].ElementName = attrib_dict['term_name']
        modelData[i].ElementType = attrib_dict['term_type']
        modelData[i].ElementDatabaseID = attrib_dict['database_id']
        modelData[i].ElementElementID = attrib_dict['term_id']
        modelData[i].PosRegName = attrib_dict['positive_reg_name']
        modelData[i].PosRegElementID = attrib_dict['positive_reg_id']
        modelData[i].PosRegComponents = attrib_dict['positive_reg_action']
        modelData[i].NegRegName = attrib_dict['negative_reg_name']
        modelData[i].NegRegElementID = attrib_dict['negative_reg_id']
        modelData[i].NegRegComponents = attrib_dict['negative_reg_action']
        i += 1
       
      # Return the output array
      return modelData

    return None
# end translateTRIPS

# consolidateDuplicates analyzes what rows involve the same element and fills
# in blank entries in that row that are not blank in "duplicate" rows
def consolidateDuplicates(modelData):
    # Compare entries for the same element
    duplicateRows = []

    for i in range(len(modelData)):
        if i in duplicateRows:
            continue
        duplicates = 0
        duplicateIndex = []
        for j in range(len(modelData)):
            if i == j:
                continue
            elif modelData[i][4] == modelData[j][4]:
                duplicates += 1
                duplicateIndex.append(j)
                duplicateRows.append(j)
        if duplicates == 0:
            continue
        else:
            # Consolidate information
            for j in range(duplicates):
                # If an element is in one row and not the other, add it
                for k in range(43):
                    if modelData[i][k] == None and modelData[duplicateIndex[j]][k] == None:
                        continue
                    elif modelData[i][k] == None and modelData[duplicateIndex[j]][k] != None:
                        modelData[i][k] = modelData[duplicateIndex[j]][k]
    ##                elif modelData[i][k] != None and modelData[duplicateIndex[j]][k] != None and modelData[i][k] != modelData[duplicateIndex[j]][k]:
    ##                    modelData[i][k] += ", " + modelData[duplicateIndex[j]][k]

    if len(duplicateRows) > 0:
        newArray = [None] * (len(modelData) - len(duplicateRows))
        badIndex = 0
        for i in range(len(modelData)):
            if i in duplicateRows:
                badIndex += 1
            else:
                newArray[i - badIndex] = modelData[i]
        modelData = newArray

    # return the consolidated data
    return modelData
# end consolidateDuplicates

# pittify returns an array that does not contain information not used in the
# PITT formalism (i.e. columns 43+ that contain FRIES entity/context info
def deprecatedPittify(modelData):
    printableData = [None] * len(modelData)
    for i in range(len(modelData)):
        printableData [i] = modelData[i][0:43]

    # return the pittified data
    return printableData
# end deprecatedPittify




