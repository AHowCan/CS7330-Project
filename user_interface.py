import csv
from pprint import pprint

"""
TODO: 
- Need to add file name validation, create directory for input_data
- call db_interface to input data into db :: pending db_interface.
- Input validation and testing

"""

def begin_UI():
    while(True):
        print("\n\tWelcome to the Bus Network System\n\n" \
                        "Please make one of the following selections, 1 or 2.\n" \
                        "At anytime tyoe 'quit' to exit, or 'back' to go to the previous selection.\n" \
                        "1) Add data\n" \
                        "2) Query database")
        response = get_input_and_validation()

        if response == "1":
            while(True):
                print("Would you like to add a driver or route?\n" \
                        "1) Drivers\n" \
                        "2) Routes\n" \
                        "3) Driver Assignments")
                response = get_input_and_validation(["3"])

                if response == "1":
                    print("Please enter file name for drivers.")
                    file_name = input(">")
                    if file_name != "back" and file_name != "quit":
                        driver_list = read_csv(file_name, "driver")
                        pprint(driver_list)
                    elif file_name == "quit":
                        return exit_ui()

                elif response == "2":
                    print("Please enter file name for routes.")
                    file_name = input(">")
                    if file_name != "back" and file_name != "quit":
                        route_list = read_csv(file_name, "route")
                        pprint(route_list)
                    elif file_name == "quit":
                        return exit_ui()
                elif response == "3":
                    print("Please enter file name for driver assignments.")
                    file_name = input(">")
                    if file_name != "back" and file_name != "quit":
                        assignment_list = read_csv(file_name, "assignment")
                        pprint(assignment_list)
                    elif file_name == "quit":
                        return exit_ui()

                elif response == "back":
                    print('\n')
                    break
                elif response == "quit":
                    return exit_ui()

        elif response == "2":
            while(True):
                print("What would you like to query?")
                
                print("--- BACKING OUT ---")
                break

        elif response == "quit":
            return exit_ui()

def read_csv(file_name, file_type):
    with open(file_name) as csv_file:
        read_csv = csv.reader(csv_file, delimiter=',')
        if file_type == "driver":
            driver_list = []
            for row in read_csv:
                driver = {}
                driver["id"] = row[0]
                driver["last_name"] = row[1]
                driver["first_name"] = row[2]
                driver["age"] = row[3]
                driver["city"] = row[4]
                driver["state"] = row[5]
                driver_list.append(driver)
            return driver_list

        elif file_type == "route":
            route_list = []
            for row in read_csv:
                route = {}
                if len(row) == 9: # Used if route name is given
                    route["number"] = row[0]
                    route["name"] = row[1]
                    route["departure_city_name"] = row[2]
                    route["departure_city_code"] = row[3]
                    route["destination_city_name"] = row[4]
                    route["destination_city_code"] = row[5]
                    route["route_type_code"] = row[6]
                    route["travel_time_hours"] = row[7]
                    route["travel_time_minutes"] = row[8]
                elif len(row) == 8: # No route name given
                    route["number"] = row[0]
                    route["name"] = ""
                    route["departure_city_name"] = row[1]
                    route["departure_city_code"] = row[2]
                    route["destination_city_name"] = row[3]
                    route["destination_city_code"] = row[4]
                    route["route_type_code"] = row[5]
                    route["travel_time_hours"] = row[6]
                    route["travel_time_minutes"] = row[7]
                route_list.append(route)
            return route_list

        elif file_type == "assignment":
            assignment_list = []
            for row in read_csv:
                assignment = {}
                assignment["driver_id"] = row[0]
                assignment["route_number"] = row[1]
                assignment["day_of_week"] = row[2]
                assignment_list.append(assignment)
            return assignment_list

        else:
            print("Exception :: Unknown file type")
            return -1

def exit_ui():
    # Use for clean exits
    print("EXITING...")

    return 0 

def get_input_and_validation(additional_input = []):
    checks = ["1", "2", "back", "quit"]
    for check in additional_input:
        checks.append(check)

    response = input(">")
    while(True):
        for valid in checks:
            if response == valid:
                return response
        print("Unknown response...\n" \
                "Try again")
        response = input(">")





