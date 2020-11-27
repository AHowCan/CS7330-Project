import db_interface


def check_driver_conflicts(driver):
    return _check_driver_id_conflict(driver)


def check_route_conflicts(route):
    return _check_route_id_conflict(route)


def check_assignment_conflicts(assignment):
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


def _sort_driver_assignments(driver):
    '''Sorts assignments Sunday, Monday, Tuesday etc.'''


def _check_c1(driver):
    '''Constraint 1. Cannot drive 2 routes at the same time'''
    pass


def _check_c2(driver):
    '''Constraint 2. Enough rest, at least half of prev route'''
    pass


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
