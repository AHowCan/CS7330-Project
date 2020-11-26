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
    if db_interface.find_one(assignment['driver_id'], 'drivers'):
        if _check_assignment_conflicts(assignment):
            print("assignment conflict for: " + str(assignment))
        else:
            db_interface.add_assignment(assignment)
    else:
        print("Driver not found for assignment -%s\n" % assignment)


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
    driver_assignments = db_interface.get_driver_assignments(
        assignment['driver_id'])
    if driver_assignments != None:
        for driver_assignment in driver_assignments:
            if driver_assignment['day_of_week'] == assignment['day_of_week']:
                if driver_assignment['route_number'] != assignment['route_number']:
                    return True
                else:
                    print("Duplicate assignment for driver")
                    return True
    return False


def _check_driver_id_conflict(driver):
    '''returns False for no conflicts'''
    return db_interface.find_one(driver['_id'], 'drivers')


def _check_route_id_conflict(route):
    '''returns False for no conflicts'''
    return db_interface.find_one(route['_id'], 'routes')
