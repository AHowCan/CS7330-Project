# This is the bridge between the user_interface and db_interface
#
#
# first check for invalid characters
# then check id conflict
# then check assignment conflicts
# finally data is sent to the db_interface

import db_interface


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
    if _check_assignment_conflicts(assignment):
        print("assignment conflict")
    else:
        db_interface.add_assignment(assignment)


def add_driver(driver):
    if _check_driver_id_conflict(driver):
        print("driver id conflict")
    else:
        db_interface.add_driver(driver)


def add_route(route):
    if _check_route_id_conflict(route):
        print("route id conflict")
    else:
        db_interface.add_route(route)


def _check_assignment_conflicts(assignment):
    '''returns False for no conflicts'''
    #print("not implemented")
    return False


def _check_driver_id_conflict(driver):
    '''returns False for no conflicts'''
    #print("not implemented")
    return False


def _check_route_id_conflict(route):
    '''returns False for no conflicts'''
    #print("not implemented")
    return False
