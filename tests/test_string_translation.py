from translators.STRING import api

string_input = '../translators/STRING/protlist.txt'
out_dir = '../translators/STRING/'

def test_string_to_biorecipe():
    api.string_to_biorecipe(string_input, output_dir=out_dir)

def main():
    # test apis and examples of our string translator
    test_string_to_biorecipe()

if __name__ == "__main__":
    main()