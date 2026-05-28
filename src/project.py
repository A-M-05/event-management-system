import sys
from schema import create_tables, import_data

def main():

    create_tables()

    function = sys.argv[1]
    args = sys.argv[2:]

    if function == "import":
        result = import_data(args[0])

    else:
        print(f"Unkown function: {function}")
        sys.exit(1)
    
    print(result) # This will print True on success and False on fail

if __name__ == "__main__":
    main()