# this file parses and checks for input errors

import csv
from config import (DAY_OF_WEEK_VALUES, US_STATE_CODES,
                    ROUTE_TYPE_VALID_DAYS, ALLOWED_ID_CHARS, ID_REPLACE_CHAR,
                    ROUTE_NUM_TOKENS,
                    DRIVER_NUM_TOKENS,
                    ASSIGNMENT_NUM_TOKENS,)
from logger import log, plog


class ParseError(Exception):
    pass


def _is_day_of_week_valid(day):
    return day in DAY_OF_WEEK_VALUES.keys()


def _is_state_code_valid(state):
    return state in US_STATE_CODES


def _is_route_type_code_valid(route_type):
    return route_type in ROUTE_TYPE_VALID_DAYS.keys()


def split_string_by_comma(string_value, expected_splits):
    split_string = []
    if expected_splits != len(string_value.split(',')):
        return -1
    else:
        for i in range(len(string_value.split(','))):
            split_string.append(string_value.split(',')[i])
        return split_string


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


def sanitize_tokens(tokens):
    tokens = [token.strip() for token in tokens]
    for i, token in enumerate(tokens):
        tokens[i] = ''.join([c for c in token if c not in ALLOWED_ID_CHARS])
    return tokens


def _check_correct_num_tokens(line_list, num_tokens):
    correct = len(line_list) == num_tokens
    if not correct:
        raise ParseError('ERROR, wrong number of tokens for input line, skipping: ' +
                         ''.join(line_list))


def _correct_city_code(city_code):
    city_code_upper = city_code.upper()
    if city_code_upper not in US_STATE_CODES:
        raise ParseError('ERROR, invalid city code, skipping: ' +
                         city_code)


def parse_routes(read_csv):
    routes_list = []
    for row in read_csv:
        try:
            _check_correct_num_tokens(row, ROUTE_NUM_TOKENS)
            row = sanitize_tokens(row)
            routes = {}
            routes['_id'] = row[0]
            routes['name'] = row[1].upper()
            routes['departure_city_name'] = row[2].capitalize()
            routes['departure_city_code'] = row[3]
            routes['destination_city_name'] = row[4]
            routes['destination_city_code'] = row[5]
            routes['route_type_code'] = row[6]
            routes['departure_time_hours'] = row[7]
            routes['departure_time_minutes'] = row[8]
            routes['travel_time_hours'] = row[9]
            routes['travel_time_minutes'] = row[10]

            routes_list.append(routes)
        except ParseError as e:
            log(e)
    return routes_list


def parse_driver(read_csv):
    driver_list = []
    for row in read_csv:
        try:
            _check_correct_num_tokens(row, DRIVER_NUM_TOKENS)
            row = sanitize_tokens(row)
            driver = {}
            driver['_id'] = row[0]
            driver['first_name'] = row[1]
            driver['last_name'] = row[2]
            driver['age'] = row[3]
            driver['city'] = row[4]
            driver['state'] = row[5]
            driver_list.append(driver)
        except ParseError as e:
            log(e)
    return driver_list


def parse_assignment(read_csv):
    assignment_list = []
    for row in read_csv:
        try:
            _check_correct_num_tokens(row, ASSIGNMENT_NUM_TOKENS)
            row = sanitize_tokens(row)
            assignment = {}
            assignment['driver_id'] = row[0]
            assignment['route_number'] = row[1]
            assignment['day_of_week'] = row[2]
            assignment_list.append(assignment)
        except ParseError as e:
            log(e)
    return assignment_list
