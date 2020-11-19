import csv
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


"""
TODO:
- call db_interface to input data into db :: pending db_interface.
- Input validation and testing

"""


def begin_UI():
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
            load_data_canvas()

        elif response == "5":
            load_data_custom()

        elif response == "6":
            wipe_database()


def read_csv(file_name, file_type):
    with open(file_name, encoding='utf-8') as csv_file:
        read_csv = csv.reader(csv_file, delimiter=',')
        if file_type == "driver":
            return parse_driver(read_csv)
        elif file_type == "routes":
            return parse_routes(read_csv)
        elif file_type == "assignment":
            return parse_assignment(read_csv)
        else:
            print("Exception :: Unknown file type")
            return -1


def exit_ui():
    # Use for clean exits
    print("EXITING...")
    sys.exit([0])


def get_input_and_validation(additional_input=[]):
    checks = ["1", "2", "3", "4", "5", "6", "back", "quit", "help"]
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
          "\n"
          "At any time type\n"
          "'quit' quit program\n"
          "'back' go to previous selection\n"
          "'help' show help\n"
          )


def prompt_add_data():
    while(True):
        print("Would you like to add a driver or routes?\n"
              "1) Drivers\n"
              "2) Routes\n"
              "3) Driver Assignments")
        response = get_input_and_validation(["3"])

        global_response_check(response)

        if response == "1":
            print("Please enter file name for drivers.")
            file_name = input(">")
            global_response_check(file_name)
            while(not path.exists(file_name) and file_name != "back"):
                print("File not found.\nPlease enter file name for drivers.")
                file_name = input(">")
                global_response_check(file_name)
            if file_name != "back":
                driver_list = read_csv(file_name, "driver")
                data_pipeline.add_drivers(driver_list)

        elif response == "2":
            print("Please enter file name for routes.")
            file_name = input(">")
            global_response_check(file_name)
            while(not path.exists(file_name) and file_name != "back"):
                print("File not found.\nPlease enter file name for routes.")
                file_name = input(">")
                global_response_check(file_name)
            if file_name != "back":
                routes_list = read_csv(file_name, "routes")
                data_pipeline.add_routes(routes_list)

        elif response == "3":
            print("Please enter file name for driver assignments.")
            file_name = input(">")
            global_response_check(file_name)
            while(not path.exists(file_name) and file_name != "back"):
                print("File not found.\nPlease enter file name for driver assignments.")
                file_name = input(">")
                global_response_check(file_name)
            if file_name != "back":
                assignment_list = read_csv(file_name, "assignment")
                pprint(assignment_list)

        elif response == "back":
            print_help()
            break


def global_response_check(response):
    if response == "help":
        print_help()
    elif response == "quit":
        exit_ui()


def prompt_query():
    while(True):
        print('not implemented')
        break


def summary():
    print('not implemented')


def load_data_canvas():
    load_data_from_folder(CANVAS_DATA_PATH)


def load_data_custom():
    load_data_from_folder(CUSTOM_DATA_PATH)


def load_data_from_folder(folder):
    '''files in folder must match 
    ASSIGNMENT_FILE
    DRIVER_FILE
    ROUTES_FILE
    in config.py
    '''
    driver_list = read_csv(folder + DRIVER_FILE, "driver")
    data_pipeline.add_drivers(driver_list)

    routes_list = read_csv(folder + ROUTES_FILE, "routes")
    data_pipeline.add_routes(routes_list)

    # assignments need to be added last since they need the above data
    assignment_list = read_csv(folder + ASSIGNMENT_FILE, "assignment")
    data_pipeline.add_assignments(assignment_list)


def wipe_database():
    db_interface.wipe_database()


def parse_routes(read_csv):
    routes_list = []
    for row in read_csv:
        routes = {}
        if len(row) == 11:
            routes["_id"] = row[0]
            routes["name"] = row[1]
            routes["departure_city_name"] = row[2]
            routes["departure_city_code"] = row[3]
            routes["destination_city_name"] = row[4]
            routes["destination_city_code"] = row[5]
            routes["route_type_code"] = row[6]
            routes["departure_time_hours"] = row[7]
            routes["departure_time_minutes"] = row[8]
            routes["travel_time_hours"] = row[9]
            routes["travel_time_minutes"] = row[10]
        else:
            return -1
        routes_list.append(routes)
    return routes_list


def parse_driver(read_csv):
    driver_list = []
    for row in read_csv:
        driver = {}
        driver["_id"] = row[0]
        driver["last_name"] = row[1]
        driver["first_name"] = row[2]
        driver["age"] = row[3]
        driver["city"] = row[4]
        driver["state"] = row[5]
        driver_list.append(driver)
    return driver_list


def parse_assignment(read_csv):
    assignment_list = []
    for row in read_csv:
        assignment = {}
        assignment["driver_id"] = row[0]
        assignment["route_number"] = row[1]
        assignment["day_of_week"] = row[2]
        assignment_list.append(assignment)
    return assignment_list


if __name__ == "__main__":
    begin_UI()
