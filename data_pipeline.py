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
        print("driver id conflict - %s" % driver["_id"])
    else:
        db_interface.add_driver(driver)


def add_route(route):
    if _check_route_id_conflict(route):
        print("route id conflict - %s" % route["_id"])
    else:
        db_interface.add_route(route)


def _check_assignment_conflicts(assignment):
    '''returns False for no conflicts'''
    driver_assignments = db_interface.get_driver_assignments(
        assignment['driver_id'])
    if driver_assignments != None:
        for driver_assignment in driver_assignments:  
            if _check_assignment_time_overlap_conflict(
                driver_assignment, assignment):
                return True
    return False


def _check_driver_id_conflict(driver):
    '''returns False for no conflicts'''
    return db_interface.find_one(driver['_id'], 'drivers')


def _check_route_id_conflict(route):
    '''returns False for no conflicts'''
    return db_interface.find_one(route['_id'], 'routes')


def _check_assignment_time_overlap_conflict(assignment1, assignment2):
    '''returns False for no conflicts'''
    route1 = db_interface.get_route(assignment1["route_number"])
    route2 = db_interface.get_route(assignment2["route_number"])
    assignment1_departure = _minute_of_week(
                            assignment1["day_of_week"],
                            route1["departure_time_hours"],
                            route1["departure_time_minutes"])
    assignment1_arrival = assignment1_departure + _minute_of_week(0,
                          route1["travel_time_hours"],
                          route1["travel_time_minutes"])
    assignment2_departure = _minute_of_week(
                            assignment2["day_of_week"],
                            route2["departure_time_hours"],
                            route2["departure_time_minutes"])
    assignment2_arrival = assignment2_departure + _minute_of_week(0,
                          route2["travel_time_hours"],
                          route2["travel_time_minutes"])
    if assignment1_departure < assignment2_departure:
        if assignment1_arrival > assignment2_departure:
            return True
        if assignment2_arrival > 10080:
            if (assignment2_arrival % 10080) > assignment1_departure:
                return True
    else:
        if assignment2_arrival > assignment1_departure:
            return True
        if assignment1_arrival > 10080:
            if (assignment1_arrival % 10080) > assignment2_departure:
                return True
    return False


def _minute_of_week(day, hour, minute):
    return (return_day_number(str(day)) * 1440) + (int(hour) * 60) + int(minute)


def return_day_number(day):
    if day == 'M':
        return 0
    elif day == 'T':
        return 1
    elif day == 'W':
        return 2
    elif day == 'U':
        return 3
    elif day == 'F':
        return 4
    elif day == 'S':
        return 5
    elif day == 's':
        return 6
    else:
        return 0
    
