# this file parses and checks for input errors

import csv
from config import (DAY_OF_WEEK_VALUES, US_STATE_CODES,
                    ROUTE_TYPE_VALID_DAYS, ALLOWED_CHARS,
                    ROUTE_NUM_TOKENS,
                    DRIVER_NUM_TOKENS,
                    ASSIGNMENT_NUM_TOKENS,
                    MAX_DEPARTURE_HOURS, MAX_TRAVEL_HOURS)
from logger import log, plog


class ParseError(Exception):
    pass


def _sanitize_day_of_week(day):
    if day not in DAY_OF_WEEK_VALUES:
        raise ParseError('ERROR, invalid day code, skipping: ' +
                         day)
    return day


def _sanitize_route_type(route_type):
    if route_type not in ROUTE_TYPE_VALID_DAYS.keys():
        raise ParseError('ERROR, invalid route type code, skipping: ' +
                         route_type)
    return route_type


def _sanitize_hours(hours, max_hours):
    try:
        int_hours = int(hours)
        if int_hours < 0 or int_hours > max_hours:
            raise ValueError
        return hours
    except ValueError:
        raise ParseError('ERROR, invalid hours, skipping: ' +
                         hours)


def _sanitize_minutes(minutes):
    try:
        int_minutes = int(minutes)
        if int_minutes < 0 or int_minutes > 60:
            raise ValueError
        return minutes
    except ValueError:
        raise ParseError('ERROR, invalid minutes, skipping: ' +
                         minutes)


def _sanitize_age(age):
    try:
        int_age = int(age)
        if int_age < 0:
            raise ValueError
        return age
    except ValueError:
        raise ParseError('ERROR, invalid age, skipping: ' +
                         age)


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


def _sanitize_tokens(tokens):
    tokens = [token.strip() for token in tokens]
    for i, token in enumerate(tokens):
        tokens[i] = ''.join([c for c in token if c in ALLOWED_CHARS])
    return tokens


def _check_correct_num_tokens(line_list, num_tokens):
    correct = len(line_list) == num_tokens
    if not correct:
        raise ParseError('ERROR, wrong number of tokens for input line, skipping: ' +
                         ''.join(line_list))


def _sanitize_city_code(city_code):
    city_code_upper = city_code.upper()
    if city_code_upper not in US_STATE_CODES:
        raise ParseError('ERROR, invalid city code, skipping: ' +
                         city_code)
    return city_code_upper


def parse_routes(read_csv):
    routes_list = []
    for idx, row in enumerate(read_csv):
        try:
            _check_correct_num_tokens(row, ROUTE_NUM_TOKENS)
            row = _sanitize_tokens(row)
            routes = {}
            routes['_id'] = row[0]
            routes['name'] = row[1].upper()
            routes['departure_city_name'] = row[2].capitalize()
            routes['departure_city_code'] = _sanitize_city_code(row[3])
            routes['destination_city_name'] = row[4].capitalize()
            routes['destination_city_code'] = _sanitize_city_code(row[5])
            routes['route_type_code'] = _sanitize_route_type(row[6])
            routes['departure_time_hours'] = _sanitize_hours(
                row[7], MAX_DEPARTURE_HOURS)
            routes['departure_time_minutes'] = _sanitize_minutes(row[8])
            routes['travel_time_hours'] = _sanitize_hours(
                row[9], MAX_TRAVEL_HOURS)
            routes['travel_time_minutes'] = _sanitize_minutes(row[10])

            routes_list.append(routes)
        except ParseError as e:
            log(f'ERROR parsing line {idx}: {", ".join(row)}')
            log(e)
    return routes_list


def parse_driver(read_csv):
    driver_list = []
    for idx, row in enumerate(read_csv):
        try:
            _check_correct_num_tokens(row, DRIVER_NUM_TOKENS)
            row = _sanitize_tokens(row)
            driver = {}
            driver['_id'] = row[0]
            driver['first_name'] = row[1].capitalize()
            driver['last_name'] = row[2].capitalize()
            driver['age'] = _sanitize_age(row[3])
            driver['city'] = row[4].capitalize()
            driver['state'] = _sanitize_city_code(row[5])
            driver_list.append(driver)
        except ParseError as e:
            log(f'ERROR parsing line {idx}: {", ".join(row)}')
            log(e)
    return driver_list


def parse_assignment(read_csv):
    assignment_list = []
    for idx, row in enumerate(read_csv):
        try:
            _check_correct_num_tokens(row, ASSIGNMENT_NUM_TOKENS)
            row = _sanitize_tokens(row)
            assignment = {}
            assignment['driver_id'] = row[0]
            assignment['route_number'] = row[1].upper()
            assignment['day_of_week'] = _sanitize_day_of_week(row[2])
            assignment_list.append(assignment)
        except ParseError as e:
            log(f'ERROR parsing line {idx}: {", ".join(row)}')
            log(e)
    return assignment_list
