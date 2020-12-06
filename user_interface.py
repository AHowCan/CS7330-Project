from pprint import pprint
import sys
from os import path
import data_pipeline
import db_interface
from config import (CANVAS_DATA_PATH,
                    CUSTOM_DATA_PATH,
                    ASSIGNMENT_FILE,
                    DRIVER_FILE,
                    ROUTES_FILE
                    )


def begin_UI():
    data_pipeline.build_graph()
    print_help()
    while(True):
        response = get_input_and_validation()

        global_response_check(response)

        if response == "1":
            prompt_add_data()

        elif response == "2":
            prompt_query()

        elif response == "3":
            summary()

        elif response == "4":
            dev_load_data_canvas()

        elif response == "5":
            dev_load_data_custom()

        elif response == "6":
            wipe_database()

        elif response == "7":
            print_graph_details()


def exit_ui():
    # Use for clean exits
    print("EXITING...")
    sys.exit([0])


def get_input_and_validation(additional_input=[]):
    checks = ["1", "2", "3", "4", "5", "6", "7", "back", "quit", "help"]
    for check in additional_input:
        checks.append(check)

    response = input(">")
    while(True):
        for valid in checks:
            if response == valid:
                return response
        print_help()
        print("Unknown response...\n"
              "Try again")
        response = input(">")


def print_help():
    print("\n\tWelcome to the Bus Network System\n\n"
          "Please make one of the following selections\n"
          "1) Add data\n"
          "2) Query database\n"
          "3) Database summary\n"
          "4) [dev] Load data_canvas to database\n"
          "5) [dev] Load data_custom to database\n"
          "6) [dev] Wipe database\n"
          "7) [dev] Print graph details\n"
          "\n"
          "At any time type\n"
          "'quit' quit program\n"
          "'back' go to previous selection\n"
          "'help' show help\n"
          )


def prompt_add_data():
    while(True):
        check_files_existence = True
        while(check_files_existence):
            print("Provide the set of file names.\nExample "
                  ">driver.csv,routes.csv,assignments.csv")
            response = input(">")
            global_response_check(response)
            if response == "back":
                print_help()
                return 0

            dataset_str = response.split(',')
            if path.exists(dataset_str[0]):
                if path.exists(dataset_str[1]):
                    if path.exists(dataset_str[2]):
                        check_files_existence = False
                    else:
                        pass
                        print("Unable to find \"" + dataset_str[2] + "\"")
                else:
                    print("Unable to find \"" + dataset_str[1] + "\"")
            else:
                print("Unable to find \"" + dataset_str[0] + "\"")
        data_pipeline.load_drivers_to_database(dataset_str[0])
        data_pipeline.load_routes_to_database(dataset_str[1])
        data_pipeline.load_assignments_to_database(dataset_str[2])
        data_pipeline.finalize()
        print_help()
        return 0


def global_response_check(response):
    if response == "help":
        print_help()
    elif response == "quit":
        exit_ui()


def prompt_query():
    while(True):
        print("\nPlease select from the following.\n"
              "1) Query driver\n"
              "2) Query city routes\n"
              "3) Query route\n"
              "4) Query route between cities\n"
              "5) Query path on specific day")
        response = input(">")
        global_response_check(response)
        if response == "back":
            print_help()
            return 0

        if response == "1":
            query_driver()

        elif response == "2":
            query_city()

        elif response == "3":
            query_route()

        elif response == "4":
            query_connection()

        elif response == "5":
            query_path()


def summary():
    print('not implemented')
    print()


def dev_load_data_canvas():
    load_data_from_folder(CANVAS_DATA_PATH)


def dev_load_data_custom():
    load_data_from_folder(CUSTOM_DATA_PATH)


def load_data_from_folder(folder):
    '''files in folder must match 
    ASSIGNMENT_FILE
    DRIVER_FILE
    ROUTES_FILE
    in config.py
    '''
    data_pipeline.load_drivers_to_database(folder + DRIVER_FILE)
    data_pipeline.load_routes_to_database(folder + ROUTES_FILE)
    # assignments need to be added last since they need the above data
    data_pipeline.load_assignments_to_database(folder + ASSIGNMENT_FILE)
    data_pipeline.finalize()


def wipe_database():
    db_interface.wipe_database()


def query_driver():
    print("Provide the first and last name seperated by a comma.")
    response = input(">")
    global_response_check(response)
    if response == "back":
        print_help()
        return 0
    results = data_pipeline.query_driver(response)
    if results != -1 and results:
        for result in results:
            # pprint(result)
            if True:    # Feel free to change if GUI needs the output in different format
                cli_print_driver(result)
    elif not results:
        print("Unable to find driver.")
    else:
        print("Error in response")


def query_city():
    print("Provide the name of a city.")
    response = input(">")
    global_response_check(response)
    if response == "back":
        print_help()
        return 0
    result = data_pipeline.query_city(response)
    if result:
        for route in result:
            # pprint(route)
            if True:
                cli_print_route(route)
    elif not result:
        print("Unable to find a city with routes.")


def query_route():
    print("Provide a route ID.")
    response = input(">")
    global_response_check(response)
    if response == "back":
        print_help()
        return 0
    result = data_pipeline.query_route(response)
    if result:
        # pprint(result[0])
        if True:
            cli_print_route(result[0])
        if result[1] == -2:
            print("Unable to find assignments for route ID %s" % response)
        else:
            driver_assignments = result[1]
            for driver in driver_assignments:
                # pprint(driver)
                if True:
                    cli_print_driver_brief(driver)
    else:
        print("Unable to find route ID %s" % response)


def query_connection():
    print("Provide the names of the two cities, separated by a comma.")
    response = input(">")
    global_response_check(response)
    if response == "back":
        print_help()
        return 0
    result = data_pipeline.query_connection(response)
    if result != -1 and result:
        for connection in result:
            result = data_pipeline.query_route(connection['_id'])
            if result:
                # pprint(result[0])
                if True:
                    cli_print_route(result[0])
                if result[1] == -2:
                    print(
                          "Unable to find assignments for route %s" % connection['_id'])
                else:
                    driver_assignments = result[1]
                    for driver in driver_assignments:
                        # pprint(driver)
                        if True:
                            cli_print_driver_brief(driver)
            else:
                print("Unable to find route ID %s" % connection['_id'])
    elif not result:
        print("Unable to find connection for %s" % response)
    else:
        print("Error in response - %s" % response)

def query_path():
    print(
          "Provide the names of the two cities, separated by a comma and a day of the week.")
    response = input(">")
    global_response_check(response)
    if response == "back":
        print_help()
        return 0
    result = data_pipeline.query_path(response)
    if result != -1 and result:
        print("The Route is", end =" ")
        for connection in result:
            print("from %s, %s to %s, %s" % (
                                             connection['departure_city_name'], connection['departure_city_code'],
                                             connection['destination_city_name'], connection['destination_city_code']), end=" ")
        print(" ")
        for connection in result:
            # print("Route ID - %s" % connection)
            if True:
                cli_print_route_brief(connection)
    elif result == -1:
        print("Error in response")
    else:
        print("No path found")

def cli_print_driver(driver):
    print("Driver: %s %s, ID:%s, Age:%s, Home Town:%s, %s" %(
                                                             driver['first_name'],driver['last_name'], driver['_id'],driver['age'],driver['city'],driver['state']))
    print("\tAssignments:")
    if 'assignments' in driver.keys():
        assignments = driver['assignments']
        for assignment in assignments:
            print("\t\t- Route Number %s, Day of the week - %s" % (assignment['route_number'],assignment['day_of_week']))
    else:
        print("\t\tNo assignments")
    print(" ")

def cli_print_driver_brief(driver):
    print("\tDriver ID:%s, Name: %s %s" % (driver['_id'], driver['first_name'], driver['last_name']))

def cli_print_route(route):
    if 'name' not in route.keys():
        route['name'] = "None"
    print(
          "Route ID: %s, Name: %s, Departing %s, %s at %s:%s, and arriving at %s, %s after %s hours and %s minutes on day of week code:%s" % (
           route['_id'], route['name'], route['departure_city_name'], route['departure_city_code'],route['departure_time_hours'],route['departure_time_minutes'],
           route['destination_city_name'], route['destination_city_code'], route['travel_time_hours'],route['travel_time_minutes'],route['route_type_code']))

def cli_print_route_brief(route):
    print("\tRoute ID: %s %s, %s - %s, %s, leaving %s:%s, arriving after %s hours and %s minutes" % (
          route['_id'], route['departure_city_name'], route['departure_city_code'], route['destination_city_name'], route['destination_city_code'],
          route['departure_time_hours'], route['departure_time_minutes'], route['travel_time_hours'], route['travel_time_minutes']))

def print_graph_details():
    print("1")
    data_pipeline.print_graph_details()

if __name__ == "__main__":
    begin_UI()
