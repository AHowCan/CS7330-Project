# Used for sorting and controlling the graph of all the routes. 
# Graph library for https://github.com/msaxena2/PyGraphLib
#
# 

import PyGraphLib
import db_interface
import config

BUS_ROUTE_GRAPH = PyGraphLib.graph()


def get_neighbors(node):
    return BUS_ROUTE_GRAPH.get_all_neighbors(node)


def build_graph():
    routes = db_interface.get_all_routes()
    for route in routes:
        add_route(route)


def get_graph():
    nodes = BUS_ROUTE_GRAPH.get_all_data()
    graph = []
    for node in nodes:
        node_details = []
        node_details.append(node)
        node_details.append("-")
        node_details.append(get_neighbors(node))
        graph.append(node_details)
    return graph


def add_route(route):
    city1 = route["departure_city_name"]
    city2 = route["destination_city_name"]

    if not BUS_ROUTE_GRAPH.get_node_data(city1):
        BUS_ROUTE_GRAPH.add_new_node(city1, city1)
    if not BUS_ROUTE_GRAPH.get_node_data(city2):
        BUS_ROUTE_GRAPH.add_new_node(city2, city2)
    BUS_ROUTE_GRAPH.add_connection(city1, city2)


def get_path(city1, city2, day_of_week):
    # Needs to complete path in 72 hours.
    #1) Get shortest path -> compare node one to next for the day of leaving (weekend or weekday)
    #2) Traverse list and add times when each leaves, if less then 72 return list
    #3) If node_list is more then 72, increase node1-2 connection weight >> 1
    #4) Recalculate shortest path, repeat

    time_keeper = 0
    route_list = []
    current_day = day_of_week
    prev_route = None
    connections = BUS_ROUTE_GRAPH.get_shortest_path(city1, city2)
    if connections != None:
        print("Shortest path - %s" % connections)
    else:
        print("Still None...")
        return 0
    for i in range(len(connections) - 1):
        links = db_interface.get_connection(connections[i], connections[i+1])
        links_list = []
        for link in links:
            links_list.append(link)
        lowest_time = [config.MAX_MINUTES_IN_CONNECTION] * len(links_list)
        for j in range(len(links_list)):
            schedule = links_list[j]['route_type_code']
            if day_of_week in config.ROUTE_TYPE_VALID_DAYS[schedule]:
                lowest_time[j] = (int(links_list[j]['travel_time_hours']) * 60) + (int(links_list[j]['travel_time_minutes']))
        if (i-1) >= 0:
            for j in range(len(links_list)):    
                if lowest_time[j] < config.MAX_MINUTES_IN_CONNECTION:
                    connection1_depart = get_departure_minute_of_day(links_list[j])
                    connection0_arrival = get_arrival_minute_of_day(prev_route)
                    if connection1_depart > connection0_arrival:
                        lowest_time[j] += (connection1_depart - connection0_arrival)
                    else:
                        if not route_runs_on_next_day(links_list[j], current_day):
                            lowest_time[j] += config.MAX_MINUTES_IN_CONNECTION
                        else:
                            lowest_time[j] += config.MINUES_IN_DAY - connection0_arrival
                            lowest_time[j] += connection1_depart
        current_day = get_next_day(current_day)
        quickest_time = config.MAX_MINUTES_IN_CONNECTION
        quickest_route = -1
        for j in range(len(links_list)):
            if lowest_time[j] < quickest_time:
                quickest_time = lowest_time[j]
                quickest_route = j
        prev_route = links_list[quickest_route]
        route_list.append(prev_route)
        time_keeper += quickest_time
    if time_keeper > config.MAX_MINUTES_IN_CONNECTION:
            return 0
    print(time_keeper)
    return route_list

def get_departure_minute_of_day(route):
    return int(route['departure_time_hours']) * 60 + int(
               route['departure_time_minutes'])


def get_arrival_minute_of_day(route):
    return int(route['departure_time_hours']) * 60 + int(
               route['departure_time_minutes']) + int(
               route['travel_time_hours']) * 60 + int(
               route['travel_time_minutes'])


def get_next_day(current_day):
    days = config.ROUTE_TYPE_VALID_DAYS['0']
    for j in range(len(days)):
        if days[j] == current_day:
            return days[(j+1) % 7]


def route_runs_on_next_day(next_route, current_day):
    route_type_code = next_route['route_type_code']
    next_day = get_next_day(current_day)
    if next_day in config.ROUTE_TYPE_VALID_DAYS[route_type_code]:
        return 1
    else:
        return 0