import sys

from ops_insert import insert_admin, update_event, delete_organizer
from ops_reserve import add_venue, reserve_slot, cancel_reservation
from ops_query import (
    available_events,
    popular_event_types,
    participant_schedule,
    organizer_stats,
    venue_events,
)
from schema import create_tables, import_data


def main():
    # The command format is:
    # python project.py functionName param1 param2 ...

    function_name = sys.argv[1]
    args = sys.argv[2:]

    if function_name == "import":
        import_data(args[0])

    elif function_name == "insertAdmin":
        insert_admin(args)

    elif function_name == "addVenue":
        add_venue(args)

    elif function_name == "reserveSlot":
        reserve_slot(args)

    elif function_name == "cancelReservation":
        cancel_reservation(args)

    elif function_name == "updateEvent":
        update_event(args)

    elif function_name == "deleteOrganizer":
        delete_organizer(args)

    elif function_name == "availableEvents":
        available_events(args[0])

    elif function_name == "popularEventTypes":
        popular_event_types(int(args[0]))

    elif function_name == "participantSchedule":
        participant_schedule(int(args[0]))

    elif function_name == "organizerStats":
        organizer_stats(int(args[0]))

    elif function_name == "venueEvents":
        venue_events(int(args[0]))


if __name__ == "__main__":
    main()