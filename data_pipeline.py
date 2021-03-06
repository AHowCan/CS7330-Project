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
import graph_controller
from logger import log, plog


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
        log('Driver not found for assignment -%s\n' % assignment)


def add_driver(driver):
    if integrity_check.check_driver_conflicts(driver):
        log('driver id conflict - %s' % driver['_id'])
    else:
        db_interface.add_driver(driver)


def add_route(route):
    if integrity_check.check_route_conflicts(route):
        log('route id conflict - %s' % route['_id'])
    else:
        db_interface.add_route(route)
        graph_controller.add_route(route)


def query_driver(driver_name):
    driver_name = input_parser.split_string_by_comma(driver_name, 2)
    if driver_name:
        return db_interface.get_driver_name(driver_name)
    else:
        return -1


def query_city(city_name):
    sorted_routes = []
    all_routes = db_interface.get_city_routes(city_name)
    sorted_route_ids = sort_route_time(all_routes)
    for route_id in sorted_route_ids:
        for route in all_routes:
            if route['_id'] == route_id[0]:
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
        driver = {'_id': assignments['_id'],
                  'first_name': assignments['first_name'],
                  'last_name': assignments['last_name']}
        assigned_drivers.append(driver)
    return route, assigned_drivers


def query_connection(cities):
    cities = input_parser.split_string_by_comma(cities, 2)
    if cities:
        connections = db_interface.get_connection(cities[0], cities[1])
        if connections:
            return connections
        else:
            return 0
    else:
        return -1


def query_path(response):
    response = input_parser.split_string_by_comma(response, 3)
    if response != -1 and response:
        # log(response)
        return graph_controller.get_path(
            response[0], response[1], response[2])
    elif response == -1:
        return -1
    else:
        return 0


def query_all_paths(city1, city2):
    graph_controller.return_all_paths(city1, city2)


def build_graph():
    graph_controller.build_graph()


def print_graph_details():
    print("----- Graph BEGIN-----")
    graph = graph_controller.get_graph()
    for node in graph:
        for detail in node:
            print(detail, end=" ")
        print(" ")
    print("----- Graph END -----")


def sort_route_time(dict_list):
    sorted_dict = {}
    for dictionary in dict_list:
        departure_time = (int(dictionary["departure_time_hours"]) * 60) + (
            int(dictionary["departure_time_minutes"]))
        sorted_dict[dictionary["_id"]] = departure_time
    sorted_dict = sorted(sorted_dict.items(), key=lambda item: item[1])
    return sorted_dict


def str_driver_pretty(driver):
    s = "Driver: %s %s, ID:%s, Age:%s, Home Town:%s, %s\n" % (
        driver['first_name'], driver['last_name'], driver['_id'], driver['age'], driver['city'], driver['state'])
    s += "\tAssignments:\n"
    if 'assignments' in driver.keys():
        assignments = driver['assignments']
        for assignment in assignments:
            s += ("\t\t- Route Number %s, Day of the week - %s\n" %
                  (assignment['route_number'], assignment['day_of_week']))
    else:
        s += "\t\tNo assignments\n\n"
    s += '\n'
    return s


def str_driver_brief(driver):
    return ("\tDriver ID:%s, Name: %s %s" %
            (driver['_id'], driver['first_name'], driver['last_name']))


def str_route_pretty(route):
    if 'name' not in route.keys():
        route['name'] = "None"
    return(
        "Route ID: %s, Name: %s, Departing %s, %s at %s:%s, and arriving at %s, %s after %s hours and %s minutes on day of week code:%s" % (
            route['_id'], route['name'], route['departure_city_name'], route[
                'departure_city_code'], route['departure_time_hours'], route['departure_time_minutes'],
            route['destination_city_name'], route['destination_city_code'], route['travel_time_hours'], route['travel_time_minutes'], route['route_type_code']))


def str_route_brief(route):
    return("\tRoute ID: %s %s, %s - %s, %s, leaving %s:%s, arriving after %s hours and %s minutes" % (
        route['_id'], route['departure_city_name'], route['departure_city_code'], route['destination_city_name'], route['destination_city_code'],
        route['departure_time_hours'], route['departure_time_minutes'], route['travel_time_hours'], route['travel_time_minutes']))
