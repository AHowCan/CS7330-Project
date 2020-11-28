# this file parses and checks for input errors

import csv
from config import (DAY_OF_WEEK_VALUES)


def _is_day_of_week_valid(day):
    return day in DAY_OF_WEEK_VALUES.keys()


def _is_state_code_valid(state):
    pass


def _is_route_type_code_valid(route_type):
    pass


def name_separation_check(driver_name):
    if "," in driver_name:
        first_name = driver_name.split(',')[0]
        last_name = driver_name.split(',')[1]
        return first_name, last_name
    else:
        return -1


def read_csv(file_name, file_type):
    with open(file_name, encoding='utf-8-sig') as csv_file:
        read_csv = csv.reader(csv_file, delimiter=',')
        if file_type == 'driver':
            return parse_driver(read_csv)
        elif file_type == 'routes':
            return parse_routes(read_csv)
        elif file_type == 'assignment':
            return parse_assignment(read_csv)
        else:
            print('Exception :: Unknown file type')
            return -1


def parse_routes(read_csv):
    routes_list = []
    for row in read_csv:
        routes = {}
        if len(row) == 11:
            routes['_id'] = row[0]
            routes['name'] = row[1]
            routes['departure_city_name'] = row[2]
            routes['departure_city_code'] = row[3]
            routes['destination_city_name'] = row[4]
            routes['destination_city_code'] = row[5]
            routes['route_type_code'] = row[6]
            routes['departure_time_hours'] = row[7]
            routes['departure_time_minutes'] = row[8]
            routes['travel_time_hours'] = row[9]
            routes['travel_time_minutes'] = row[10]
        else:
            return -1
        routes_list.append(routes)
    return routes_list


def parse_driver(read_csv):
    driver_list = []
    for row in read_csv:
        driver = {}
        driver['_id'] = row[0]
        driver['first_name'] = row[1]
        driver['last_name'] = row[2]
        driver['age'] = row[3]
        driver['city'] = row[4]
        driver['state'] = row[5]
        driver_list.append(driver)
    return driver_list


def parse_assignment(read_csv):
    assignment_list = []
    for row in read_csv:
        assignment = {}
        assignment['driver_id'] = row[0]
        assignment['route_number'] = row[1]
        assignment['day_of_week'] = row[2]
        assignment_list.append(assignment)
    return assignment_list


def sort_route_time(dict_list):
    sorted_dict = {}
    for dictonary in dict_list:
        departure_time = (int(dictonary["departure_time_hours"]) * 60) + (
                          int(dictonary["departure_time_minutes"]))
        sorted_dict[dictonary["_id"]] = departure_time
    sorted(sorted_dict.items(), key=lambda item: item[1])
    return sorted_dict