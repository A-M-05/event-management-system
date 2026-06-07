import sys

from ops_reserve import add_venue, reserve_slot, cancel_reservation
from schema import create_tables, import_data

def main():
    # The command format is:
    # python project.py functionName param1 param2 ...

    create_tables()
    
    function_name = sys.argv[1]
    args = sys.argv[2:]

    if function == "import":
        import_data(args[0])
    
    elif function_name == "addVenue":
        add_venue(args)

    elif function_name == "reserveSlot":
        reserve_slot(args)

    elif function_name == "cancelReservation":
        cancel_reservation(args)


if __name__ == "__main__":
    main()