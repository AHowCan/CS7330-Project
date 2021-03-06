import copy
import db_interface
from config import (DAY_OF_WEEK_VALUES,
                    FIRST_DAY_OF_WEEK,
                    MINUTES_IN_WEEK,
                    ROUTE_TYPE_VALID_DAYS,
                    TIME_EPSILON,
                    MINUTES_TO_SWITCH_CITIES,
                    HOMETOWN_REST_MINUTES)
from logger import log, plog


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
        log('ERROR, assignment day does not match route type: assignment: ' + str(assignment))
        log('  Valid days for this route are: ' + str(valid_days))
        return True


def _check_assignment_route_missing(assignment):
    '''returns False for no conflict'''
    route_number = assignment['route_number']
    route = db_interface.get_route(route_number)
    if not route:
        log('ERROR, route not found for assignment: ' + str(assignment))
        return True
    return False


def _check_driver_id_conflict(driver):
    '''returns False for no conflicts'''
    return db_interface.find_one(driver['_id'], 'drivers')


def _check_route_id_conflict(route):
    '''returns False for no conflicts'''
    return db_interface.find_one(route['_id'], 'routes')


def _get_departure_minute_of_week(assignment, route):
    return _minute_of_week(assignment['day_of_week'],
                           route['departure_time_hours'],
                           route['departure_time_minutes'])


def _get_arrival_minute_of_week(assignment, route):
    total_travel_time_minutes = int(
        route['travel_time_hours']) * 60 + int(route['travel_time_minutes'])
    return _get_departure_minute_of_week(assignment, route) + total_travel_time_minutes


def _check_assignment_time_overlap_conflict(assignment1, assignment2):
    '''returns False for no conflicts'''
    route1 = db_interface.get_route(assignment1['route_number'])
    route2 = db_interface.get_route(assignment2['route_number'])
    assignment1_departure = _get_departure_minute_of_week(assignment1, route1)
    assignment1_arrival = _get_arrival_minute_of_week(assignment1, route1)
    assignment2_departure = _get_departure_minute_of_week(assignment2, route2)
    assignment2_arrival = _get_arrival_minute_of_week(assignment2, route2)
    any_errors = False
    if assignment1_departure < assignment2_departure:
        if assignment1_arrival > assignment2_departure:
            any_errors = True
        if assignment2_arrival > MINUTES_IN_WEEK:
            if (assignment2_arrival % MINUTES_IN_WEEK) > assignment1_departure:
                any_errors = True
    else:
        if assignment2_arrival > assignment1_departure:
            any_errors = True
        if assignment1_arrival > MINUTES_IN_WEEK:
            if (assignment1_arrival % MINUTES_IN_WEEK) > assignment2_departure:
                any_errors = True
    if any_errors:
        log('ERROR: assignments overlap')
        log('  Assignment_1: ' + str(assignment1))
        log('  Assignment_2: ' + str(assignment2))
    return any_errors


class DriverConstraintCheck:
    '''It is probably safe to assume that the information for one driver can fit in memory
    Several constraints use the same data and this class encapsulates that'''

    def __init__(self, driver):
        # self.driver_ext is driver extended info
        self.driver_ext = copy.deepcopy(driver)
        self.driver_original = driver
        if 'assignments' not in self.driver_ext:
            self.driver_ext['assignments'] = []
        self.routes = self._get_unique_routes()  # cache driver routes
        self._extend_assignments_with_minute_of_week()
        self._sort_assignments()

    def check_all_constraints(self):
        self._pairwise_assignment_checks()
        self._hometown_check()

    def _get_unique_routes(self):
        unique_routes_numbers = set()
        for assignment in self.driver_ext['assignments']:
            unique_routes_numbers.add(assignment['route_number'])
        unique_routes = {}
        for route_number in unique_routes_numbers:
            unique_routes[route_number] = db_interface.get_route(route_number)
        return unique_routes

    def _extend_assignments_with_minute_of_week(self):
        for assignment in self.driver_ext['assignments']:
            route = self._get_route_of_assignment(assignment)
            departure_minute = _get_departure_minute_of_week(assignment, route)
            arrival_minute = _get_arrival_minute_of_week(assignment, route)
            assignment['departure_minute'] = departure_minute
            assignment['arrival_minute'] = arrival_minute

    def _clear_extended_info(self, assignment):
        assignment_clear = assignment.copy()
        del assignment_clear['departure_minute']
        del assignment_clear['arrival_minute']
        return assignment_clear

    def _sort_assignments(self):
        '''sort based on departure_minute'''
        self.driver_ext['assignments'].sort(
            key=lambda assignment: assignment['departure_minute'])

    def _get_route_of_assignment(self, assignment):
        route_number = assignment['route_number']
        return self.routes[route_number]

    def _check_not_enough_rest_between_assignments(self, assignment1, assignment2, loop):
        assignment1_duration = assignment1['arrival_minute'] - \
            assignment1['departure_minute']
        rest_time = assignment2['departure_minute'] - \
            assignment1['arrival_minute']
        if loop:  # looped to the next week
            rest_time += MINUTES_IN_WEEK
        if rest_time >= (assignment1_duration / 2 - TIME_EPSILON):
            return False

        log('ERROR: driver: {} not getting enough rest.'.format(
            self.driver_ext['_id']))
        log('  Assignment_1: ' +
            str(self._clear_extended_info(assignment1)))
        log('  Assignment_2: ' +
            str(self._clear_extended_info(assignment2)))
        return True

    def _pairwise_assignment_checks(self):
        '''Constraint 2. Enough rest, at least half of prev route
        Constraint 3. Can reach next assignment
        returns False for no conflict
        '''
        assignments = self.driver_ext['assignments']
        num_assignments = len(assignments)

        # all pairwise constraints are met if there are only 1 or less assignments
        if num_assignments <= 1:
            return False

        assignments_idx = list(range(num_assignments))
        # this is so that the indexing loop back to the first one for the last check
        assignments_idx.append(0)
        any_errors = False
        for i in range(num_assignments):
            assignment1 = assignments[assignments_idx[i]]
            assignment2 = assignments[assignments_idx[i+1]]
            loop = False
            if i == num_assignments - 1:
                loop = True
            if self._check_not_enough_rest_between_assignments(assignment1, assignment2, loop):
                any_errors = True
            if self._check_cant_reach_next_assignment(assignment1, assignment2, loop):
                any_errors = True
        return any_errors

    def _check_cant_reach_next_assignment(self, assignment1, assignment2, loop):
        '''assignment1 comes before assignment2
        return False for no conflict'''
        route1 = self.routes[assignment1['route_number']]
        route2 = self.routes[assignment2['route_number']]
        if (route1['destination_city_name'] == route2['departure_city_name']) \
                and (route1['destination_city_code'] == route2['departure_city_code']):
            return False
        time_between_assignments = assignment2['departure_minute'] - \
            assignment1['arrival_minute']
        if loop:
            time_between_assignments += MINUTES_IN_WEEK
        if time_between_assignments >= MINUTES_TO_SWITCH_CITIES - TIME_EPSILON:
            return False

        log('ERROR: Driver {} can\'t reach next assignment in time'.format(
            self.driver_ext['_id']))
        log('  Assignment_1: ' +
            str(self._clear_extended_info(assignment1)))
        log('  Assignment_2: ' +
            str(self._clear_extended_info(assignment2)))
        return True

    def _hometown_check(self):
        '''since the instructions don't specify, 
        assume that ONE 18 hour rest per week is enough
        return False for no conflict'''
        home_city = self.driver_ext['city']
        home_state = self.driver_ext['state']
        rest_requirement_met = False
        reaches_home = False

        assignments = self.driver_ext['assignments']
        num_assignments = len(assignments)
        assignments_idx = list(range(num_assignments))
        # this is so that the indexing loop back to the first one for the last check
        assignments_idx.append(0)

        for i in range(num_assignments):
            assignment1 = assignments[assignments_idx[i]]
            assignment2 = assignments[assignments_idx[i+1]]
            loop = False
            if i == num_assignments - 1:
                loop = True
            route_before_rest = self.routes[assignment1['route_number']]
            rest_city = route_before_rest['destination_city_name']
            rest_state = route_before_rest['destination_city_code']
            if home_city == rest_city and home_state == rest_state:
                reaches_home = True
                rest_minutes = assignment2['departure_minute'] - \
                    assignment1['arrival_minute']
                if rest_minutes >= HOMETOWN_REST_MINUTES - TIME_EPSILON:
                    rest_requirement_met = True
                    return False
        if not reaches_home:
            log('ERROR: Driver never reaches home city.')
            log('Driver:')
            plog(self.driver_original)
        else:
            log('ERROR: Driver reaches home city but does not get enough leave time.')
            log('Driver:')
            plog(self.driver_original)
        return True


def final_constraint_check():
    '''perform final constraint check
    since some constraints require all data to be loaded to make sense'''
    for driver in db_interface.get_all_drivers():
        constraint_checker = DriverConstraintCheck(driver)
        constraint_checker.check_all_constraints()
