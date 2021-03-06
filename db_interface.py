import pymongo

from config import DB_NAME, TEST_DB_URI, COL_DRIVERS, COL_ROUTES, DB_URI
from connect import Connect

from pprint import pprint
from logger import log, plog

# generally never use globals, except in class projects
CLIENT = Connect.get_connection()
DB = CLIENT[DB_NAME]
DRIVERS_COLLECTION = DB[COL_DRIVERS]
ROUTES_COLLECTION = DB[COL_ROUTES]


def get_client_connection():
    client = Connect.get_connection()
    return client


def add_assignment(assignment):
    driver_id = assignment['driver_id']
    a = assignment.copy()
    del a['driver_id']
    DRIVERS_COLLECTION.update(
        {'_id': driver_id}, {'$push': {'assignments': a}})


def add_driver(driver):
    DRIVERS_COLLECTION.insert_one(driver)


def add_route(route):
    ROUTES_COLLECTION.insert_one(route)


def find_one(query, db_collection):
    if db_collection == 'drivers':
        if DRIVERS_COLLECTION.find_one(query, {'_id': 1}) != None:
            return True
    elif db_collection == 'routes':
        if ROUTES_COLLECTION.find_one(query, {'_id': 1}) != None:
            return True
    return False


def get_driver_assignments(driver_id):
    driver = DRIVERS_COLLECTION.find_one(driver_id)
    if 'assignments' in driver.keys():
        return driver['assignments']
    else:
        return None


def get_driver(driver_id):
    driver = DRIVERS_COLLECTION.find_one(driver_id)
    return driver


def get_driver_name(driver_name):
    driver_list = []
    drivers = DRIVERS_COLLECTION.find(
        {'first_name': driver_name[0],
         'last_name': driver_name[1]})
    for driver in drivers:
        driver_list.append(driver)
    return driver_list


def get_all_routes():
    ''' note that find() returns a "cursor", which is lazy
    so this is not actually storing the whole collection in memory'''
    return ROUTES_COLLECTION.find()


def get_all_drivers():
    return DRIVERS_COLLECTION.find()


def get_all_driver_ids():
    ids = DRIVERS_COLLECTION.find({}, {'_id': 1})
    ids = [i['_id'] for i in ids]
    return ids


def get_route(route_id):
    route = ROUTES_COLLECTION.find_one(route_id)
    return route


def get_distinct_cities(departure_or_destination):
    '''will return departure/destination cities with states
    e.g.
    [['Richardson', 'TX'], ['Dallas', 'TX'], ['Houston', 'TX'], ['Waco', 'TX']]
    '''
    d = departure_or_destination
    if d not in ['departure', 'destination']:
        log("ERROR, departure_or_destination must be one of 'departure','destination'")
        return []

    cities = ROUTES_COLLECTION.aggregate([{
        '$group': {
            '_id': {
                f'{d}_city_name': f'${d}_city_name',
                f'{d}_city_code': f'${d}_city_code'
            }
        }
    }
    ])
    cities = [
        [city['_id'][f'{d}_city_name'], city['_id'][f'{d}_city_code']]
        for city in cities]
    return cities


def get_connection(city1, city2):
    connections = ROUTES_COLLECTION.find({'departure_city_name': city1,
                                          'destination_city_name': city2})
    return list(connections)


def get_connection_city_state(city1, state1, city2, state2):
    connections = ROUTES_COLLECTION.find({'departure_city_name': city1,
                                          'departure_city_code': state1,
                                          'destination_city_name': city2,
                                          'destination_city_code': state2})
    return list(connections)


def get_route_assignments(route_id):
    route_assignments = []
    assignments = DRIVERS_COLLECTION.find(
        {'assignments.route_number': route_id})
    if not assignments:
        return 0
    for assignment in assignments:
        route_assignments.append(assignment)
    return route_assignments


def get_city_routes(city_name):
    all_routes = []
    routes = ROUTES_COLLECTION.find({'departure_city_name': city_name})
    for route in routes:
        all_routes.append(route)
    routes = ROUTES_COLLECTION.find({'destination_city_name': city_name})
    for route in routes:
        all_routes.append(route)
    return all_routes


def get_city_routes_departure_destination(city, state, departure_or_destination):
    d = departure_or_destination
    if d not in ['departure', 'destination']:
        log("ERROR, departure_or_destination must be one of 'departure','destination'")
        return []
    return ROUTES_COLLECTION.find({f'{d}_city_name': city, f'{d}_city_code': state})


def wipe_database():
    DRIVERS_COLLECTION.remove()
    ROUTES_COLLECTION.remove()
