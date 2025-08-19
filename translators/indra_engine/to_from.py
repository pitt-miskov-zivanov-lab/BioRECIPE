import os
import pandas as pd
import glob
from indra.belief import SimpleScorer
from indra.sources import indra_db_rest as idr
from indra.statements import *
import copy
from collections import defaultdict
import re
from indra.databases.hgnc_client import get_hgnc_name

# Define biorecipe_int_cols to match the PDF column order exactly
biorecipe_int_cols = [
    "Regulator Name", "Regulator Type", "Regulator Subtype", "Regulator HGNC Symbol", 
    "Regulator Database", "Regulator ID", "Regulator Compartment", "Regulator Compartment ID",
    "Regulated Name", "Regulated Type", "Regulated Subtype", "Regulated HGNC Symbol", 
    "Regulated Database", "Regulated ID", "Regulated Compartment", "Regulated Compartment ID",
    "Sign", "Connection Type", "Mechanism", "Site", "Cell Line", "Cell Type", "Tissue Type", 
    "Organism", "Score", "Source", "Statements", "Paper IDs", "Database Source", "Database ID"
]

def convert_hgnc_id_to_symbol(hgnc_id_value):
    """
    Convert HGNC ID to symbol using INDRA's HGNC client.
    
    Parameters
    ----------
    hgnc_id_value : str
        The HGNC ID value (e.g., "391", "HGNC:391")
        
    Returns
    -------
    str
        The HGNC symbol if found, otherwise the original value
    """
    if pd.isna(hgnc_id_value) or hgnc_id_value == "":
        return hgnc_id_value
    
    value_str = str(hgnc_id_value).strip()
    
    # Check if it looks like an HGNC ID (patterns like "HGNC:391", "hgnc:391", or just "391")
    hgnc_id_pattern = r'^(hgnc:?)?(\d+)$'
    match = re.match(hgnc_id_pattern, value_str, re.IGNORECASE)
    
    if match:
        numeric_id = match.group(2)
        try:
            hgnc_num = int(numeric_id)
            if 1 <= hgnc_num <= 60000:  # Reasonable HGNC ID range
                # Get symbol from INDRA's HGNC client
                symbol = get_hgnc_name(numeric_id)
                if symbol:
                    return symbol
        except (ValueError, Exception):
            pass
    
    return hgnc_id_value

def fix_hgnc_symbols_in_dataframe(df):
    """
    Fix HGNC symbols in a BioRECIPE DataFrame by converting IDs to symbols.
    
    Parameters
    ----------
    df : pandas.DataFrame
        BioRECIPE format DataFrame
        
    Returns
    -------
    int
        Number of conversions made
    """
    hgnc_cols = ["Regulator HGNC Symbol", "Regulated HGNC Symbol"]
    conversion_count = 0
    
    for col in hgnc_cols:
        if col in df.columns:
            # Store original values to count changes
            original_values = df[col].copy()
            
            # Apply conversion
            df[col] = df[col].apply(convert_hgnc_id_to_symbol)
            
            # Count conversions
            col_conversions = sum(1 for orig, new in zip(original_values, df[col]) 
                                if orig != new and pd.notna(orig) and orig != "")
            conversion_count += col_conversions
            

    
    return conversion_count

def get_complete_db_refs_dict():
    """
    Returns a comprehensive dictionary mapping database reference keys to 
    their display names and entity types for BioRECIPE format.
    
    Returns
    -------
    dict
        Dictionary with database keys mapping to (display_name, entity_type) tuples
    """
    return {
        'UP': ('uniprot', 'protein'),
        'UPPRO': ('uniprot', 'protein'), 
        'PF': ('pfam', 'family'),
        'CHEBI': ('chebi', 'small molecule'),
        'PUBCHEM': ('pubchem', 'small molecule'),
        'GO': ('go', 'biological process'),
        'MESH': ('mesh', 'biological process'),
        'HGNC': ('hgnc', 'gene'),
        'EGID': ('entrez', 'gene'),
        'FPLX': ('famplex', 'protein family'),
        'TEXT': ('other', 'other')
    }

def extract_context_info(s):
    """
    Extracts context information (organism, tissue, cell type, cell line) 
    from INDRA statement evidence.
    
    Parameters
    ----------
    s : indra.statements.Statement
        INDRA statement object
        
    Returns
    -------
    dict
        Dictionary containing context information with keys: 
        'Organism', 'Tissue Type', 'Cell Type', 'Cell Line'
    """
    context_info = {"Organism": "", "Tissue Type": "", "Cell Type": "", "Cell Line": ""}
    
    if hasattr(s, 'evidence') and s.evidence:
        for evidence in s.evidence:
            if hasattr(evidence, 'context') and evidence.context:
                ctx = evidence.context
                if hasattr(ctx, 'species') and ctx.species:
                    context_info['Organism'] = getattr(ctx.species, 'name', None) or str(ctx.species)
                if hasattr(ctx, 'cell_line') and ctx.cell_line:
                    context_info['Cell Line'] = getattr(ctx.cell_line, 'name', None) or str(ctx.cell_line)
                if hasattr(ctx, 'cell_type') and ctx.cell_type:
                    context_info['Cell Type'] = getattr(ctx.cell_type, 'name', None) or str(ctx.cell_type)
                if hasattr(ctx, 'organ') and ctx.organ:
                    context_info['Tissue Type'] = getattr(ctx.organ, 'name', None) or str(ctx.organ)
                
                if any(context_info.values()):
                    break
    
    return context_info

def assign_entity_info(agent, role, row, fOut, db_refs_dict):
    """
    Assigns entity information (name, database, type, compartment) to the output DataFrame
    for special statement types like Translocation and Complex.
    
    Parameters
    ----------
    agent : indra.statements.Agent
        INDRA agent object
    role : str
        Either "Regulator" or "Regulated"
    row : int
        Row index in the output DataFrame
    fOut : pandas.DataFrame
        Output DataFrame to populate
    db_refs_dict : dict
        Database reference mapping dictionary
    """
    if not agent:
        return
    
    fOut.loc[row, f"{role} Name"] = getattr(agent, 'name', '')
    db_refs = getattr(agent, 'db_refs', {})
    
    if 'HGNC' in db_refs:
        fOut.loc[row, f"{role} HGNC Symbol"] = db_refs['HGNC']
    
    # Compartment info
    if hasattr(agent, 'location') and agent.location:
        fOut.loc[row, f"{role} Compartment"] = getattr(agent.location, 'name', '') or str(agent.location)
        if hasattr(agent.location, 'db_refs') and agent.location.db_refs:
            fOut.loc[row, f"{role} Compartment ID"] = list(agent.location.db_refs.values())[0]
    
    # Database info
    for db_name, (db_display, entity_type) in db_refs_dict.items():
        try:
            if db_name in db_refs:
                fOut.loc[row, f"{role} Database"] = db_display
                fOut.loc[row, f"{role} Type"] = entity_type
                fOut.loc[row, f"{role} ID"] = db_refs[db_name]
                break
        except:
            pass

def parse_pmc(input, outdir):
    """
    Parse PMC files from input directory or single file and extract interactions.
    
    Parameters
    ----------
    input : str
        Path to input directory containing CSV files or single CSV file
    outdir : str
        Output directory path
    """
    if os.path.isdir(input):
        files = glob.glob(input + "/*.csv")
        for infile in files:
            get_biorecipeI_from_pmcids(infile, outdir)
    else:
        infile = input
        get_biorecipeI_from_pmcids(infile, outdir)

def get_biorecipeI_from_pmcids(infile, outdir):
    """
    This function queries PMCIDs using INDRA database API and
    outputs the reading file from INDRA statements in BioRECIPE format.

    Parameters
    ----------
    infile : str
        Input file that has "PMCID" and/or "PMID" column headers
    outdir : str
        Output directory path

    Returns
    -------
    None
        By default, it will output the extracted interactions in BioRECIPE format
        as an Excel file with two sheets: "statements" and "Paper Not Found"
    """

    infile_ = os.path.splitext(os.path.basename(infile))[0]
    fName = os.path.join(outdir, f'{infile_}_reading.xlsx')

    papers_df = pd.read_csv(infile, dtype=str)
    ext_cols = []
    if "PMID" in papers_df.columns:
        ext_cols.append("PMID")

    if "PMCID" in papers_df.columns:
        ext_cols.append("PMCID")

    if len(ext_cols) == 0:
        raise ValueError("No PMCID or PMID column found in the input file")

    papers_df = papers_df[ext_cols]
    
    papers = []
    for idx, row in papers_df.iterrows():
        tag = False
        if "PMCID" in papers_df.columns:
            pmcid = row["PMCID"]
            if pd.notna(pmcid):
                papers.append('PMC' + pmcid.lstrip('PMC'))
                tag = True

        if not tag:
            if "PMID" in papers_df.columns:
                pmid = row["PMID"]
                if pd.notna(pmid):
                    papers.append(pmid)

    # Reading output in BioRECIPE format
    fOut = pd.DataFrame(columns=biorecipe_int_cols)

    rowCount = 0
    noStatements = []
    
    # Track unspecified types for summary reporting
    unspecified_regulation_types = defaultdict(int)
    unspecified_connection_types = defaultdict(int)

    # Use enhanced database mapping
    db_refs_dict = get_complete_db_refs_dict()
    print(f"Processing {len(papers)} papers...")

    for p in papers:
        print(f"Processing paper: {p}")
        if "PMC" in p:
            idrp = idr.get_statements_for_papers(ids=[('pmcid',p)],)
        else:
            idrp = idr.get_statements_for_papers(ids=[('pmid',p)],)
        stmts = idrp.statements

        if(stmts):
            for s in stmts:
                bs = SimpleScorer()
                j = s.to_json()
                intType = j["type"]
                bScore = bs.score_statement(s)
                valid_st = False
                upstrDbFlag = False # check regulator db info

                # Extract context information
                context_info = extract_context_info(s)

                # Extract source information from evidence
                source_api = "INDRA"  # default
                try:
                    if hasattr(s, 'evidence') and s.evidence:
                        for evidence in s.evidence:
                            if hasattr(evidence, 'source_api') and evidence.source_api:
                                source_api = evidence.source_api
                                break
                except:
                    pass

                try:
                    # Regulator
                    upstr = j["subj"]
                    upstrName = upstr["name"]
                    fOut.loc[rowCount, "Regulator Name"] = upstrName
                    upstrDbRefs = upstr["db_refs"]

                    fOut.loc[rowCount, "Score"] = bScore
                    fOut.loc[rowCount, "Mechanism"] = intType
                    fOut.loc[rowCount, "Paper IDs"] = p
                    
                    # Add context information
                    for col, val in context_info.items():
                        if val:
                            fOut.loc[rowCount, col] = val
                    
                    valid_st = True

                    try:
                        paperStats = j["evidence"]
                        fOut.loc[rowCount, "Statements"] = paperStats[0]["text"]

                        epi_var = paperStats[0]["epistemics"]
                        fOut.loc[rowCount, "Connection Type"] = str(epi_var['direct'])

                    except Exception as e:
                        pass

                    # HGNC Symbol
                    try:
                        upstrHNGC = upstrDbRefs['HGNC']
                        fOut.loc[rowCount, "Regulator HGNC Symbol"] = upstrHNGC
                    except:
                        pass

                    for db_name, (db_display, entity_type) in db_refs_dict.items():
                        try:
                            upstrDb = upstrDbRefs[db_name]
                            fOut.loc[rowCount, "Regulator Database"] = db_display
                            fOut.loc[rowCount, "Regulator Type"] = entity_type
                            # Subtype is intentionally left empty
                            fOut.loc[rowCount, "Regulator ID"] = upstrDb
                            upstrDbFlag = True
                            break
                        except:
                            pass

                    # other type/element info should be assigned
                    if not upstrDbFlag:
                        db_name = list(upstrDbRefs.keys())[0]
                        upstrDb = upstrDbRefs[db_name]

                        fOut.loc[rowCount, "Regulator Database"] = db_name
                        fOut.loc[rowCount, "Regulator Type"] = "other"
                        fOut.loc[rowCount, "Regulator ID"] = upstrDb

                    if fOut.loc[rowCount, "Regulator Database"] == 0:
                        fOut.loc[rowCount, "Regulator ID"] = upstrName

                except Exception as e:
                    try:
                        upstr = j["enz"]
                        upstrName = upstr["name"]

                        fOut.loc[rowCount, "Regulator Name"] = upstrName

                        upstrDbRefs = upstr["db_refs"]
                        fOut.loc[rowCount, "Score"] = bScore
                        fOut.loc[rowCount, "Mechanism"] = intType
                        fOut.loc[rowCount, "Paper IDs"] = p
                        
                        # Add context information
                        for col, val in context_info.items():
                            if val:
                                fOut.loc[rowCount, col] = val
                                
                        valid_st = True

                        # HGNC Symbol
                        try:
                            upstrHNGC = upstrDbRefs['HGNC']
                            fOut.loc[rowCount, "Regulator HGNC Symbol"] = upstrHNGC
                        except:
                            pass

                        for db_name, (db_display, entity_type) in db_refs_dict.items():
                            try:
                                upstrDb = upstrDbRefs[db_name]
                                fOut.loc[rowCount, "Regulator Database"] = db_display
                                fOut.loc[rowCount, "Regulator Type"] = entity_type
                                fOut.loc[rowCount, "Regulator ID"] = upstrDb
                                upstrDbFlag = True
                                break
                            except:
                                pass

                        # other type/element info should be assigned
                        if not upstrDbFlag:
                            db_name = list(upstrDbRefs.keys())[0]
                            upstrDb = upstrDbRefs[db_name]
                            fOut.loc[rowCount, "Regulator Database"] = db_name
                            fOut.loc[rowCount, "Regulator Type"] = "other"
                            # Subtype is intentionally left empty
                            fOut.loc[rowCount, "Regulator ID"] = upstrDb

                        if fOut.loc[rowCount, "Regulator Database"] == 0:
                            fOut.loc[rowCount, "Regulator ID"] = upstrName

                    except Exception as e:
                        pass

                downstrDbFlag = False  # check regulated db info
                try:
                    # Regulated
                    downstr = j["obj"]
                    downstrName = downstr["name"]
                    fOut.loc[rowCount, "Regulated Name"] = downstrName
                    downstrDbRefs = downstr["db_refs"]

                    # HGNC Symbol
                    try:
                        downstrHNGC = downstrDbRefs['HGNC']
                        fOut.loc[rowCount, "Regulated HGNC Symbol"] = downstrHNGC
                    except:
                        pass

                    for db_name, (db_display, entity_type) in db_refs_dict.items():
                        try:
                            downstrDb = downstrDbRefs[db_name]
                            fOut.loc[rowCount, "Regulated Database"] = db_display
                            fOut.loc[rowCount, "Regulated Type"] = entity_type
                            # Subtype is intentionally left empty
                            fOut.loc[rowCount, "Regulated ID"] = downstrDb
                            downstrDbFlag = True
                            break
                        except:
                            pass

                    # other type/element info should be assigned
                    if not downstrDbFlag:
                        db_name = list(downstrDbRefs.keys())[0]
                        downstrDb = downstrDbRefs[db_name]
                        fOut.loc[rowCount, "Regulated Database"] = db_name
                        fOut.loc[rowCount, "Regulated Type"] = "other"
                        # Subtype is intentionally left empty
                        fOut.loc[rowCount, "Regulated ID"] = downstrDb

                    if fOut.loc[rowCount, "Regulated Database"] == 0:
                        fOut.loc[rowCount, "Regulated ID"] = downstrName

                except Exception as e:
                    try:
                        downstr = j["sub"]
                        downstrName = downstr["name"]
                        fOut.loc[rowCount, "Regulated Name"] = downstrName
                        downstrDbRefs = downstr["db_refs"]

                        # HGNC Symbol
                        try:
                            downstrHNGC = downstrDbRefs['HGNC']
                            fOut.loc[rowCount, "Regulated HGNC Symbol"] = downstrHNGC
                        except:
                            pass

                        for db_name, (db_display, entity_type) in db_refs_dict.items():
                            try:
                                downstrDb = downstrDbRefs[db_name]
                                fOut.loc[rowCount, "Regulated Database"] = db_display
                                fOut.loc[rowCount, "Regulated Type"] = entity_type
                                # Subtype is intentionally left empty
                                fOut.loc[rowCount, "Regulated ID"] = downstrDb
                                downstrDbFlag = True
                                break
                            except:
                                pass

                        # other type/element info should be assigned
                        if not downstrDbFlag:
                            db_name = list(downstrDbRefs.keys())[0]
                            downstrDb = downstrDbRefs[db_name]
                            fOut.loc[rowCount, "Regulated Database"] = db_name
                            fOut.loc[rowCount, "Regulated Type"] = "other"
                            # Subtype is intentionally left empty
                            fOut.loc[rowCount, "Regulated ID"] = downstrDb

                        if fOut.loc[rowCount, "Regulated Database"] == 0:
                            fOut.loc[rowCount, "Regulated ID"] = downstrName

                    except Exception as e:
                        pass

                # Handle special statement types using assign_entity_info function
                if intType == "Translocation":
                    # Set the mechanism explicitly for Translocation
                    fOut.loc[rowCount, "Mechanism"] = "Translocation"
                    
                    regulator_agent = regulated_agent = getattr(s, 'agent', None)
                    if regulator_agent:
                        assign_entity_info(regulator_agent, "Regulator", rowCount, fOut, db_refs_dict)
                        assign_entity_info(regulated_agent, "Regulated", rowCount, fOut, db_refs_dict)
                        
                        # Simple compartment extraction from text with IDs
                        if hasattr(s, 'evidence') and s.evidence:
                            text = getattr(s.evidence[0], 'text', '').lower()
                            if 'cytoplasm' in text and 'nucleus' in text:
                                fOut.loc[rowCount, "Regulator Compartment"] = "cytoplasm"
                                fOut.loc[rowCount, "Regulator Compartment ID"] = "GO:0005737"
                                fOut.loc[rowCount, "Regulated Compartment"] = "nucleus"
                                fOut.loc[rowCount, "Regulated Compartment ID"] = "GO:0005634"
                            elif 'nuclear translocation' in text:
                                fOut.loc[rowCount, "Regulated Compartment"] = "nucleus"
                                fOut.loc[rowCount, "Regulated Compartment ID"] = "GO:0005634"
                            elif 'plasma membrane' in text:
                                fOut.loc[rowCount, "Regulated Compartment"] = "plasma membrane"
                                fOut.loc[rowCount, "Regulated Compartment ID"] = "GO:0005886"
                        valid_st = True
                elif intType == "Complex":
                    # Set the mechanism explicitly for Complex
                    fOut.loc[rowCount, "Mechanism"] = "Complex"
                    
                    if hasattr(s, 'members') and len(s.members) >= 2:
                        regulator_agent, regulated_agent = s.members[0], s.members[1]
                        assign_entity_info(regulator_agent, "Regulator", rowCount, fOut, db_refs_dict)
                        assign_entity_info(regulated_agent, "Regulated", rowCount, fOut, db_refs_dict)
                        valid_st = True

                if(valid_st):
                    # translate for some columns here - track unspecified types instead of printing
                    mechanism = fOut.loc[rowCount, "Mechanism"]
                    if mechanism in ["Activation", "IncreaseAmount", "Phosphorylation"]:
                        fOut.loc[rowCount, "Sign"] = "positive"
                    elif mechanism in ["Inhibition", "DecreaseAmount", "Dephosphorylation"]:
                        fOut.loc[rowCount, "Sign"] = "negative"
                    elif mechanism in ["Translocation", "Complex"]:
                        # Set neutral or positive for these mechanisms
                        fOut.loc[rowCount, "Sign"] = "positive"
                    else:
                        unspecified_regulation_types[mechanism] += 1
                        fOut.loc[rowCount, "Sign"] = "positive"

                    connection_type = fOut.loc[rowCount, "Connection Type"]
                    if connection_type not in ["True", "False"]:
                        unspecified_connection_types[connection_type] += 1
                        fOut.loc[rowCount, "Connection Type"] = "False"

                    fOut.loc[rowCount, "Source"] = source_api

                    # next row count
                    rowCount += 1
        else:
            noStatements.append(str(p))

    if(len(noStatements) > 0):
        print("No statements found for papers: ")
        for n in noStatements:
            print(n)

    # Fix HGNC symbols before saving
    fix_hgnc_symbols_in_dataframe(fOut)

    # Create output directory if it doesn't exist
    os.makedirs(outdir, exist_ok=True)
    
    # IMPORTANT: Reorder columns to match the original biorecipe_int_cols order
    fOut = fOut.reindex(columns=biorecipe_int_cols)

    with pd.ExcelWriter(fName, engine='openpyxl') as writer:
        fOut.fillna("").to_excel(writer, sheet_name="statements", index=False)

        noStatements_df = pd.DataFrame(noStatements, columns=["Paper ID"])
        noStatements_df.to_excel(writer, sheet_name="Paper Not Found", index=False)

    print(f"✓ Wrote {rowCount} interactions → {fName}")

def get_INDRAstmts_from_biorecipeI(infile, outfile):
    """
    Translate BioRECIPE interaction lists to INDRA statements.

    Parameters
    ----------
    infile : str
        Name and path of input BioRECIPE interaction lists file (.xlsx)
    outfile : str
        Name and path of output json file (contains INDRA statements)

    Returns
    -------
    None
        Outputs INDRA statements as JSON file
    """

    df = pd.read_excel(infile, dtype=">U50", keep_default_na=False)

    # Map BioRECIPE mechanisms to INDRA statement types
    stmts_mapping = {
        "phosphorylation": Phosphorylation,
        "dephosphorylation": Dephosphorylation,
        "ubiquitination": Ubiquitination,
        "activation": Activation,
        "inhibition": Inhibition,
        "increaseamount": IncreaseAmount,
        "decreaseamount": DecreaseAmount
    }

    stmts = []
    for i in range(len(df)):
        t = df.loc[i, 'Regulated Name']
        s = df.loc[i, 'Regulator Name']
        sign = df.loc[i, 'Sign']
        m = df.loc[i, 'Mechanism']

        ta = Agent(t)
        sa = Agent(s)

        if not m or m.lower() not in stmts_mapping.keys():
            # default statements decided by interaction sign
            if sign == 'positive':
                stmt = Activation(sa, ta)
            elif sign == 'negative':
                stmt = Inhibition(sa, ta)
            else:
                raise ValueError('Invalid value was found in Sign column')
        else:
            # find an indra statement
            stmt = stmts_mapping[m.lower()](sa, ta)

        stmts.append(stmt)

    # Output statements to JSON file
    stmts_to_json_file(stmts, outfile)
