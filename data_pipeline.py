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
    driver_list = input_parser.read_csv(filepath, 'driver')
    add_drivers(driver_list)


def load_routes_to_database(filepath):
    routes_list = input_parser.read_csv(filepath, 'routes')
    add_routes(routes_list)


def load_assignments_to_database(filepath):
    assignments_list = input_parser.read_csv(filepath, 'assignment')
    add_assignments(assignments_list)


def finalize():
    integrity_check.final_constraint_check()


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
            pass  # detailed errors will be emitted in the conflict checks
        else:
            db_interface.add_assignment(assignment)
    else:
        print('Driver not found for assignment -%s\n' % assignment)


def add_driver(driver):
    if integrity_check.check_driver_conflicts(driver):
        print('driver id conflict - %s' % driver['_id'])
    else:
        db_interface.add_driver(driver)


def add_route(route):
    if integrity_check.check_route_conflicts(route):
        print('route id conflict - %s' % route['_id'])
    else:
        db_interface.add_route(route)


def query_driver(driver_name):
    driver_name = input_parser.string_separation_check(driver_name)
    if driver_name:
        return db_interface.get_driver_name(driver_name)
    else:
        return -1


def query_city(city_name):
    sorted_routes = []
    all_routes = db_interface.get_city_routes(city_name)
    sorted_route_ids = input_parser.sort_route_time(all_routes)
    for route_id in sorted_route_ids:
        for route in all_routes:
            if route['_id'] == route_id:
                sorted_routes.append(route)
                break
    return sorted_routes


def query_route(route_id):
    route = db_interface.get_route(route_id)
    if not route:
        return 0
    assigned_drivers = []
    assignments_with_route_id = db_interface.get_route_assignments(route_id)
    if not assignments_with_route_id:
        return route, -2
    for assignments in assignments_with_route_id:
        driver = {'_id':assignments['_id'],
                  'first_name':assignments['first_name'],
                  'last_name':assignments['last_name']}
        assigned_drivers.append(driver)
    return route, assigned_drivers


def query_connection(cities):
    cities = input_parser.string_separation_check(cities)
    if cities:
        connections = db_interface.get_connection(cities[0], cities[1])
        if connections:
            return connections
        else:
            return 0
    else:
        return -1
