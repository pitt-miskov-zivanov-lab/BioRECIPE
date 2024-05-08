import sys
from translators.STRING.api import string_to_biorecipe

def main():
    input_name = sys.argv[1] #list of query proteins in HUGO symbol format
    output_dir = sys.argv[2]
    string_to_biorecipe(input_name, output_dir)

if __name__ == '__main__':
    main()
