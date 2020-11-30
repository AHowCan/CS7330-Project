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
    #1) Get shortest path -> compare node one to day of leaving (weekend or weekday)
    #2) Traverse list and add times when each leaves, if less then 72 return list
    #3) If node_list is more then 72, increase node1-2 connection weight >> 1
    #4) Recalculate shortest path, repeat

    connections = BUS_ROUTE_GRAPH.get_shortest_path(city1, city2)
    if connections != None:
        print("Shortest path - %s" % connections)
    else:
        print("Still None...")
        return 0
    connections_list = []
    alt_route_exists = []
    time_keeper = 0
    current_day = day_of_week
    prev_route = None
    for i in range(len(connections) - 1):
        links = db_interface.get_connection(connections[i], connections[i+1])
        links_list = []
        for link in links:
            links_list.append(link)
        if len(links) > 1:
            alt_route_exists.append(i)
        j = None
        for j in range(len(links_list)):
            schedule = links_list[j]['route_type_code']
            if day_of_week in config.ROUTE_TYPE_VALID_DAYS[schedule]:
                connections_list.append(links_list[j]['_id'])
                time_keeper += (int(links_list[j]['travel_time_hours']) * 60) + (int(links_list[j]['travel_time_minutes']))
                break
        if (i-1) >= 0:
            connection1_depart = get_departure_minute_of_day(links_list[j])
            connection0_arrival = get_arrival_minute_of_day(prev_route)
            if connection1_depart > connection0_arrival:
                time_keeper += (connection1_depart - connection0_arrival)
            else:
                if not route_runs_on_next_day(links_list[j], current_day):
                    time_keeper += 99999999999 # add a lot of time to time_keeper, to trigger new route
                else:
                    time_keeper += config.MINUES_IN_DAY - connection0_arrival
                    time_keeper += connection1_depart
                current_day = get_next_day(current_day)
        prev_route = links_list[j]
        if time_keeper > config.MAX_MINUTES_IN_CONNECTION:
            if len(alt_route_exists):
                #redo
                return -1
            else:
                # No route exists
                return 0
    #print(time_keeper)
    return connections_list

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
            return days[j+1]


def route_runs_on_next_day(next_route, current_day):
    route_type_code = next_route['route_type_code']
    next_day = get_next_day(current_day)
    if next_day in config.ROUTE_TYPE_VALID_DAYS[route_type_code]:
        return 1
    else:
        return 0