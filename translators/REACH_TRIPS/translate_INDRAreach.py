
#Created by Casey July 2018
#Last updated March 22 2019
import argparse
import sys
import csv
import json
import indra
from indra.sources import reach
from indra.preassembler import Preassembler

#reach_processor = reach.process_text('MEK1 phosphorylates ERK2.')
def main_translator(filelist,pmc,append,output_file):
    #FIXME: format function defintitions
    """This can be replaced by either PCC PMCs, or direct statements assigned to some kind of varible"""
    # filelist = ['4936323','4513933','4171619','4896000','3439927','3154272','2954851','4102778','3039802','4687460',
    #             '4381256','4135037','1325242','2714081','3837323','1440880','2801705','4258317','3388235','3734838']
    # filelist = 'C:/Users/Casey/Development/evidence.txt'
    # filelist = pmc.tsv
    #pmc = list,evidence,tsv
    #append = True, False
    #output_file = 'translated_reading_statements.csv'
    if append == "True":
        app = 'at'
    else:
        app = 'wt'
    

    ##To get pmc numbers from a .tsv file
    # argument is the file containing pmc numbers
    # def get_pmc(filename):
    #     #with open('C:/Users/Casey/Development/example_reading_combined.tsv','rt') as tsvin:
    #     pmclist = []
    #     with open(filename,'rt') as tsvin:
    #         tsvin = csv.reader(tsvin, delimiter='\t')

    #         for row in tsvin:
    #             ID = (row[21][3:len(row)])
    #             pmclist.append(ID)
    #             pmclist = list(set(pmclist))
    #     return pmclist

    def get_pmc(filename):
        """Get PMC numbers from a .csv file, argument is the file containing PMC numbers"""
        #with open('C:/Users/Casey/Development/example_reading_combined.tsv','rt') as tsvin:
        pmc_list = []
        k = open(filename)
        line = k.readline()
        while line:
            line = line.replace("pmc","")
            pmc_list.append(line)
            line = h.readline()
        return pmc_list

    def translate(string, translateFile):
        """Translates the entity name if the name isn't already in the list of entity IDs"""
        remove = ["dephosphrylated","phosphorylated","phosphorylates","phosphorylate","phosphorylations of",
                    "phosphorylation of","phosphorylation", "expression of","expression","levels","level of",
                    "level","protein","Runt"]
        for each in remove:
            string = string.replace(each,"")
        if " at " in string:
            string = string[0:string.find("at ")]
        elif " and " in string:
            string = string[0:string.find("and ")]
        elif " (" in string:
            string = string[0:string.find("(")]
        else:
            with open(translateFile,'rt') as csvin:
                csvin = csv.reader(csvin, delimiter=',')
                for row in csvin:
                    if string in row[0]:
                        string = row[1]
                    else:
                        string = ""
        string = string.strip()
        return string
        

    def read_interact(statements):
        """Creates list of interaction mechanisms from REACH statements"""
        mech = []
        ev = []
        for x in range(len(statements)):
            line = str(statements[x])
            mech.append(line[0:line.find('(')])
            ev.append(statements[x].__dict__.get('evidence')[0].__dict__.get('text'))
        return [mech, ev]

    # mainFunction(filelist, directory, pmc=file,list,statements, append=True, outFile)

    def json_read(filename,pmc_ID):
        """reads JSON file created by INDRA"""
        with open(filename,'r') as json_file:
            reading = json.load(json_file)

            ##getting lists for entity identification
            text = []
            eltype = []
            database = [] #called "namespace" in json file
            elid = []
            for y in range(len(reading['entities']['frames'])):
                if reading['entities']['frames'][y]['text'] not in text:
                    text.append(reading['entities']['frames'][y]['text'])
                    eltype.append(reading['entities']['frames'][y]['type'])
                    database.append(reading['entities']['frames'][y]['xrefs'][0]['namespace'])
                    elid.append(reading['entities']['frames'][y]['xrefs'][0]['id'])

            ## Sorting through entities
            for x in range(len(reading['events']['frames'])):
                args =  reading['events']['frames'][x]['arguments'][0]['type']
                if args =='controller' or args=='controlled':
                    #assigning entity names and labels
                    ent1 = reading['events']['frames'][x]['arguments'][0]['text']
                    if ent1 in text:
                        idx = text.index(ent1)
                        ent1TYPE, ent1DATA, ent1ID = eltype[idx], database[idx] ,elid[idx]
                    else:
                        ent11 = translate(ent1,'translator.csv')
                        if ent11 in text:
                            idz = text.index(ent11)
                            ent1TYPE, ent1DATA, ent1ID = eltype[idz], database[idz] ,elid[idz]
                        else:
                            ent1TYPE, ent1DATA, ent1ID = " "," "," "
                    
                    ent2 = reading['events']['frames'][x]['arguments'][1]['text']
                    if ent2 in text:
                        idx = text.index(ent2)
                        ent2TYPE, ent2DATA, ent2ID = eltype[idx], database[idx], elid[idx] 
                    else:
                        ent22 = translate(ent2,'translator.csv')
                        if ent22 in text:
                            idz = text.index(ent22)
                            ent2TYPE, ent2DATA, ent2ID = eltype[idz], database[idz] ,elid[idz]
                        else:
                            ent2TYPE, ent2DATA, ent2ID = " "," "," "
                    if (ent1TYPE == " " or ent2TYPE == " ") and x not in empty:
                        empty.append(x)
                    #used to assign regulator as either 'positive' or 'negative'
                    reg = reading['events']['frames'][x]['subtype']

                    #determining direct or indirect interaction
                    if 'is-direct' in reading['events']['frames'][x]:
                        if reading['events']['frames'][x]['is-direct'] == False:
                            direction = "I"
                        else:
                            reading['events']['frames'][x]['is-direct'] = "D"
                    else:
                        direction = "D"

                    #evidence from reading
                    evidence = reading['events']['frames'][x]['verbose-text']
                    if evidence in interactions[1]:
                        idz = interactions[1].index(evidence)
                        mechanism = interactions[0][idz]
                    else:
                        mechanism = reading['events']['frames'][x]['type']
                    

                    #creating output lines
                    if args == 'controller' and 'negative' in reg:
                        #enz1 negative regulator
                        f.writerow([ent2,ent2TYPE,ent2DATA,ent2ID," "," "," "," "," ", " "," "," "," "," ",
                        ent1,ent2TYPE,ent1DATA,ent1ID," ",direction, mechanism, "pmc"+pmc_ID, evidence])
                    elif args == 'controller' and 'negative' not in reg:
                        #enz1 positive regulator
                        f.writerow([ent2, ent2TYPE, ent2DATA, ent2ID, " "," "," "," "," ", ent1,ent1TYPE,ent1DATA,ent1ID,
                        " ", " "," "," "," "," ",direction, mechanism, "pmc"+pmc_ID, evidence])
                    elif args == 'controlled' and 'negative' in reg:
                        #enz2 negative regulator
                        f.writerow([ent1,ent1TYPE,ent1DATA,ent1ID," "," "," "," "," ", " "," "," "," "," ",
                        ent2,ent2TYPE,ent2DATA,ent2ID," ",direction, mechanism, "pmc"+pmc_ID, evidence])
                    elif args == 'controlled' and 'negative' not in reg:
                        #enz2 positive regulato
                        f.writerow([ent1,ent1TYPE,ent1DATA,ent1ID, " "," "," "," "," ", ent2,ent2TYPE,ent2DATA,ent2ID,
                        " ", " "," "," "," "," ",direction, mechanism, "pmc"+pmc_ID, evidence])

    ##Header for output file
    header = ['Element Name','Element Type','Database','Element Identifier','Location',
            'Location Identifier','Cell Line','Cell Type','Organism', 'PosReg Name', 
            'PosReg Type', 'PosReg ID', 'PosReg Location','PosReg Location ID', 'NegReg Name','NegReg Type', 
            'NegReg ID', 'NegReg Location','NegReg Location ID', 'Interaction Direct or Indirect','Mechanism','PaperID','Evidence']

    empty = []

    if pmc == 'list':
        filelist = json.loads(filelist)
        with open(output_file, app, newline='') as csvfile:
            f = csv.writer(csvfile,delimiter=',')
            #only write header if append = false
            if app == 'wt':
                f.writerow(header)
            if len(filelist) > 1:
                for x in range(len(filelist)):
                    empty.append("For pmc: "+str(filelist[x]))
                    reach_processor = reach.process_pmc(str(filelist[x]))
                    interactions = Preassembler.combine_duplicate_stmts(reach_processor.statements)
                    interactions = read_interact(interactions)
                    # interactions = readInteract(reach_processor.statements)
                    json_read('reach_output.json',str(filelist[x]))
            elif len(filelist) == 1:
                reach_processor = reach.process_pmc(str(filelist[0]))
                interactions = Preassembler.combine_duplicate_stmts(reach_processor.statements)
                interactions = read_interact(interactions)
                json_read('reach_output.json',str(filelist[0]))
            else:
                print("Error: no files to read")

    elif pmc == 'evidence':
        with open(output_file, app, newline='') as csvfile:
            f = csv.writer(csvfile,delimiter=',')
            if app == 'wt':
                f.writerow(header)
                h = open(filelist)
                line = h.readline()
                num = 0
                while line:
                    reach_processor = reach.process_text(line)
                    interactions = read_interact(reach_processor.statements)
                    json_read('reach_output.json',"Null")
                    # num += 1
                    line = h.readline() 

    elif pmc == 'csv':
        filelist = get_pmc(filelist)
        with open(output_file, app, newline='') as csvfile:
            f = csv.writer(csvfile,delimiter=',')
            #only write header if append = false
            if app == 'wt':
                f.writerow(header)
            if len(filelist) > 1:
                for x in range(len(filelist)):
                    reach_processor = reach.process_pmc(filelist[x])
                    interactions = read_interact(reach_processor.statements)
                    json_read('reach_output.json',filelist[x])
            elif len(filelist) == 1:
                reach_processor = reach.process_pmc(filelist[0])
                interactions = read_interact(reach_processor.statements)
                json_read('reach_output.json',filelist[0])
            else:
                print("Error: no files to read")    

    print("The following lines have unidentified entities:")
    #empty.sort()
    print(empty)
       

def main():
    parser = argparse.ArgumentParser(description='Use INDRA to create a reading file from PMC IDs.')
    parser.add_argument('filelist', type=str, 
                        help='list of PMC IDs to be read with INDRA')
    parser.add_argument('pmc', type=str, choices=['list','evidence','csv'],
                        help='format PMC list \n' 
                        'list: python-formatted list of PMC numbers \n' 
                        'evidence: a single line of evidence text, given as string \n' 
                        'csv: single-column csv file with list of PMC ID numbers \n' 
                        )
    parser.add_argument('append', type=bool, 
                        help='Boolean. Determines if you want to add to file or create new')
    parser.add_argument('output_file', type=str, 
                        help='path and name of output file to save reading')

    args = parser.parse_args()

    if (args.pmc == 'list' or args.pmc == 'evidence' or args.pmc == 'csv') and (type(args.append)==bool):
        main_translator(args.filelist,args.pmc,args.append,args.output_file)
    else: 
        raise InputError('Unrecognized input format')

if __name__ == '__main__':
    main()