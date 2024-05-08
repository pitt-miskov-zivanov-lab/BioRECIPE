from translators.indra import api

biorecipe_input = '../examples/interaction_lists/interaction_biorecipe.xlsx'
indra_output = '../examples/indra/interaction_indra.json'

ids = '../translators/indra/ids.csv'
outdir = '../examples/interaction_lists/'

def test_biorecipe_to_indra():
    api.biorecipe_to_indra(biorecipe_input, indra_output)

def test_indra_pmcids_to_biorecipe():
    # FIXME: separate api
    api.parse_pmc(ids, outdir)