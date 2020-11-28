
import db_interface
from config import (DAY_OF_WEEK_VALUES,
                    FIRST_DAY_OF_WEEK,
                    MINUTES_IN_WEEK,
                    ROUTE_TYPE_VALID_DAYS)


def check_driver_conflicts(driver):
    return _check_driver_id_conflict(driver)


def check_route_conflicts(route):
    return _check_route_id_conflict(route)


def check_assignment_conflicts(assignment):
    '''returns False for no conflicts'''
    if _check_assignment_route_missing(assignment):
        return True
    if _check_assignment_route_type_mismatch(assignment):
        return True

    driver_assignments = db_interface.get_driver_assignments(
        assignment['driver_id'])
    if driver_assignments != None:
        for driver_assignment in driver_assignments:
            if _check_assignment_time_overlap_conflict(
                    driver_assignment, assignment):
                return True
    return False


def _return_day_number(day):
    return DAY_OF_WEEK_VALUES[day]


def _minute_of_week(day, hour, minute):
    return (_return_day_number(str(day)) * 1440) + (int(hour) * 60) + int(minute)


def _sort_driver_assignments(driver):
    '''Sorts assignments based on the minute of week the start'''
    pass


def _get_prev_assignment(assignment, driver):
    '''Get the previous assignment according to departure datetime

    note that _get_prev_assignment and _get_next_assignment 
    will return the same assignment if there is only one other assignment
    return None if no other assignments
    '''
    pass


def _get_next_assignment(assignment, driver):
    '''Get the next assignment according to departure datetime'''
    pass


def _check_not_enough_rest(assignment1, assignment2):
    '''Constraint 2. Enough rest, at least half of prev route
    returns False for no conflict
    '''
    pass


def _check_assignment_route_type_mismatch(assignment):
    '''returns False for no conflict'''
    route_number = assignment['route_number']
    route = db_interface.get_route(route_number)
    day = assignment['day_of_week']
    route_type_code = route['route_type_code']
    valid_days = ROUTE_TYPE_VALID_DAYS[route_type_code]

    if day in valid_days:
        return False
    else:
        print('ERROR, assignment day does not match route type: assignment: ' + str(assignment))
        print('  Valid days for this route are: ' + str(valid_days))
        return True


def _check_assignment_route_missing(assignment):
    '''returns False for no conflict'''
    route_number = assignment['route_number']
    route = db_interface.get_route(route_number)
    if not route:
        print('ERROR, route not found for assignment: ' + str(assignment))
        return True
    return False


def _check_c3(driver):
    '''Constraint 3. Enough time to reach next destination'''
    pass


def _check_c4(driver):
    '''Constraint 4. Reaches hometown, with rest'''
    pass


def _check_driver_id_conflict(driver):
    '''returns False for no conflicts'''
    return db_interface.find_one(driver['_id'], 'drivers')


def _check_route_id_conflict(route):
    '''returns False for no conflicts'''
    return db_interface.find_one(route['_id'], 'routes')


def _check_assignment_time_overlap_conflict(assignment1, assignment2):
    '''returns False for no conflicts'''
    route1 = db_interface.get_route(assignment1['route_number'])
    route2 = db_interface.get_route(assignment2['route_number'])
    assignment1_departure = _minute_of_week(
        assignment1['day_of_week'],
        route1['departure_time_hours'],
        route1['departure_time_minutes'])
    assignment1_arrival = assignment1_departure + _minute_of_week(FIRST_DAY_OF_WEEK,
                                                                  route1['travel_time_hours'],
                                                                  route1['travel_time_minutes'])
    assignment2_departure = _minute_of_week(
        assignment2['day_of_week'],
        route2['departure_time_hours'],
        route2['departure_time_minutes'])
    assignment2_arrival = assignment2_departure + _minute_of_week(FIRST_DAY_OF_WEEK,
                                                                  route2['travel_time_hours'],
                                                                  route2['travel_time_minutes'])
    if assignment1_departure < assignment2_departure:
        if assignment1_arrival > assignment2_departure:
            return True
        if assignment2_arrival > MINUTES_IN_WEEK:
            if (assignment2_arrival % MINUTES_IN_WEEK) > assignment1_departure:
                return True
    else:
        if assignment2_arrival > assignment1_departure:
            return True
        if assignment1_arrival > MINUTES_IN_WEEK:
            if (assignment1_arrival % MINUTES_IN_WEEK) > assignment2_departure:
                return True
    return False
