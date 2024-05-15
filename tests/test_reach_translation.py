import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), os.pardir, 'translators')))
from reach_engine.reach_fries_to_smy import summarize_reach_fries
from reach_engine.smy_to_rcp import reach_smy_to_biorecipeI

reach_jsons_dir = 'reach/usr_reach_fries_1'
reach_json_summary_file = 'reach/usr_reach_fries_1_summary.json'
result_interactions_file = 'interaction_lists/usr_reach_fries_1_interactions.xlsx'

test_files_rl_path = '../examples/'

def test_reach_fries_to_biorecipeI():

    summarize_reach_fries(
    test_files_rl_path + reach_jsons_dir,
    test_files_rl_path + reach_json_summary_file
    )

    reach_smy_to_biorecipeI(
    test_files_rl_path + reach_json_summary_file,
    test_files_rl_path + result_interactions_file
    )

def main():
    test_reach_fries_to_biorecipeI()

if __name__ == "__main__":
    main()
