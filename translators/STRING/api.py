import sys,os
import requests
import numpy as np
import json
import time
from operator import itemgetter
import pandas as pd
#######################################
#Emilee Holtzapple
#Last modified by: Difei Tang May 8th 2024
#######################################

def string_to_biorecipe(input_name, output_dir):
    prots = []
    f = open(input_name)  # load list of query proteins
    for line in f:
        prots.append(line.rstrip())  # add all protein names to a list

    url_m = 'http://string-db.org/api/json/get_string_ids?identifiers='  # url needed for ID mapping

    for el in prots:
        url_m = url_m + el + '_HUMAN%0d'  # add all IDs to url separated by carriage return

    url_m = url_m + '&limit=1'  # take only the first (best) match
    resp = requests.get(url_m)
    protInfo = json.loads(resp.text)  # use json interpreter

    stringIds = []
    for prot in protInfo:
        stringIds.append(prot["stringId"])  # object is a list of dictionaries - we only want IDs

    url_n = 'http://string-db.org/api/json/network?identifiers='  # Now let's get the list of network interactions

    for sid in stringIds:
        url_n = url_n + sid + '%0d'
    time.sleep(1)  # Very important - do not overload server!
    resp_n = requests.get(url_n)
    ints = json.loads(resp_n.text)
    ints_df = pd.DataFrame.from_dict(ints)
    print(ints_df)

    input_name_ = os.path.splitext(os.path.basename(input_name))[0]
    out_file = f"{input_name_}_STRING_interactions.xlsx"
    outf_name = os.path.join(output_dir, out_file)

    ints_df.to_excel(outf_name)