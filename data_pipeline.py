# This is the bridge between the user_interface and db_interface
#
#
# first check for invalid characters
# then check id conflict
# then check assignment conflicts
# finally data is sent to the db_interface

import db_interface
import integrity_check
import input_parser


def load_drivers_to_database(filepath):
    driver_list = input_parser.read_csv(filepath, "driver")
    add_drivers(driver_list)


def load_routes_to_database(filepath):
    driver_list = input_parser.read_csv(filepath, "routes")
    add_routes(driver_list)


def load_assignments_to_database(filepath):
    driver_list = input_parser.read_csv(filepath, "assignment")
    add_assignments(driver_list)


def add_assignments(assignments):
    for assignment in assignments:
        add_assignment(assignment)


def add_drivers(drivers):
    for driver in drivers:
        add_driver(driver)


def add_routes(routes):
    for route in routes:
        add_route(route)


def add_assignment(assignment):
    if db_interface.find_one(assignment['driver_id'], 'drivers'):
        if integrity_check.check_assignment_conflicts(assignment):
            print("assignment conflict for: " + str(assignment))
        else:
            db_interface.add_assignment(assignment)
    else:
        print("Driver not found for assignment -%s\n" % assignment)


def add_driver(driver):
    if integrity_check.check_driver_conflicts(driver):
        print("driver id conflict")
    else:
        db_interface.add_driver(driver)


def add_route(route):
    if integrity_check.check_route_conflicts(route):
        print("route id conflict")
    else:
        db_interface.add_route(route)
