from dearpygui.core import (show_logger,
                            set_main_window_title,
                            start_dearpygui,
                            does_item_exist,
                            log_debug,
                            add_menu_item,
                            add_button,
                            add_text,
                            add_combo,
                            add_listbox,
                            add_same_line,
                            select_directory_dialog,
                            set_value,
                            get_value,
                            configure_item,
                            delete_item)

from dearpygui.simple import (window,
                              show_about,
                              show_metrics,
                              show_documentation,
                              show_debug,
                              menu_bar,
                              menu,
                              child,
                              group)

import db_interface
import data_pipeline
from datetime import datetime
from config import (ASSIGNMENT_FILE,
                    DRIVER_FILE,
                    ROUTES_FILE,
                    DAY_STRING_TO_CHAR)
from os import path
from pprint import pformat


TITLE = 'Our buses do not smell! Okay, maybe a little. But only in the summer. Oh alright, they smell damn awful in the summer. [SIGHING SOUND] [END OF AUTOMATED VOICE TRANSCRIPT]'

SELECTED_FOLDER_VAR = 'SELECTED_FOLDER_VAR'
FILES_FOUND_STR_VAR = 'FILES_FOUND_STR_VAR'

g_window_counter = 0

set_value(FILES_FOUND_STR_VAR, 'No files found')
set_value(SELECTED_FOLDER_VAR, 'None')


def on_window_close(sender, data):
    delete_item(sender)


def set_selected_folder(sender, data):
    folder = path.join(data[0], data[1])
    set_value(SELECTED_FOLDER_VAR, folder)
    # check if files exist in folder
    found_assignment_file = path.exists(path.join(folder, ASSIGNMENT_FILE))
    found_driver_file = path.exists(path.join(folder, DRIVER_FILE))
    found_routes_file = path.exists(path.join(folder, ROUTES_FILE))

    def found_or_missing(found):
        if found:
            return 'Found'
        else:
            return 'Missing'
    prompt_text = f'{found_or_missing(found_assignment_file)}: {ASSIGNMENT_FILE}\n{found_or_missing(found_driver_file)}: {DRIVER_FILE}\n{found_or_missing(found_routes_file)}: {ROUTES_FILE}'
    all_files_found = found_assignment_file and found_driver_file and found_routes_file
    configure_item('Import Files##btn', enabled=all_files_found)
    if not all_files_found:
        prompt_text += '\nSome files are missing, please ensure that they exist and are named correctly'

    set_value(FILES_FOUND_STR_VAR, prompt_text)


def select_folder(sender, data):
    select_directory_dialog(callback=set_selected_folder)


def import_data(sender, data):
    folder = get_value(SELECTED_FOLDER_VAR)
    data_pipeline.load_drivers_to_database(path.join(folder, DRIVER_FILE))
    data_pipeline.load_routes_to_database(path.join(folder, ROUTES_FILE))
    data_pipeline.load_assignments_to_database(
        path.join(folder, ASSIGNMENT_FILE))
    data_pipeline.finalize()


def create_import_data_window(sender, data):
    if(does_item_exist('Import Data##Window')):
        log_debug('Import Data window already exists')
    else:

        with window('Import Data##Window', on_close=on_window_close, width=400):
            add_button('Select Folder##btn',
                       callback=select_folder)
            add_same_line()
            add_button('Import Files##btn', callback=import_data,
                       enabled=False)
            add_text('Selected Folder:')
            add_text(name='Selected Folder##txt',
                     source=SELECTED_FOLDER_VAR)
            add_text(
                name='Selected Folder##{FILES_FOUND_STR_VAR}', source=FILES_FOUND_STR_VAR)
            set_value(FILES_FOUND_STR_VAR, 'No files found')
            set_value(SELECTED_FOLDER_VAR, 'None')


def create_drivers_window(sender, data):
    global g_window_counter
    window_id = str(g_window_counter)
    with window('Drivers##Window'+window_id,
                width=800,
                height=800,
                x_pos=20,
                y_pos=20,
                on_close=on_window_close):
        driver_names = [driver['first_name']+','+driver['last_name']
                        for driver in db_interface.get_all_drivers()]
        add_combo('Drivers##Combo'+window_id,
                  items=driver_names, callback=update_driver_info_panel, callback_data=window_id)
        with child('Driver Details##'+window_id):
            add_text('DriverDetails##txt'+window_id)
    g_window_counter += 1


def update_driver_info_panel(sender, data):
    window_id = data
    driver_fullname = get_value(sender)
    driver_fullname = split_with_comma(driver_fullname)
    driver_info = pformat(db_interface.get_driver_name(driver_fullname))
    set_value('DriverDetails##txt'+window_id, driver_info)


def create_routes_window(sender, data):
    global g_window_counter
    window_id = str(g_window_counter)
    with window('Routes##Window'+window_id,
                width=800,
                height=800,
                x_pos=20,
                y_pos=20,
                on_close=on_window_close):
        route_ids = [route['_id']
                     for route in db_interface.get_all_routes()]
        add_combo('Routes##Combo'+window_id,
                  items=route_ids, callback=update_routes_info_panel, callback_data=window_id)
        with child('Route Details##'+window_id):
            add_text('RouteDetails##txt'+window_id)
            set_value('RouteDetails##txt'+window_id, '')

    g_window_counter += 1


def update_routes_info_panel(sender, data):
    window_id = data
    route_id = get_value(sender)
    route_and_assignments = data_pipeline.query_route(route_id)
    route_info = pformat(route_and_assignments)
    set_value('RouteDetails##txt'+window_id, route_info)


def print_data(sender, data):
    print(f'get_value(sender): {get_value(sender)}')
    print(f'sender : {sender}')
    print(f'data : {data}')


def split_with_comma(s):
    return s.split(',')


def update_routes_from_city_selection(sender, data):
    window_id = data
    departure_city = get_value('Departure##'+window_id)
    destination_city = get_value('Destination##'+window_id)
    departure_day = get_value('Departure Day##'+window_id)
    routes = []
    routes_display = []
    if departure_city and not destination_city:
        routes = db_interface.get_city_routes_departure_destination(
            *split_with_comma(departure_city), 'departure')
    if destination_city and not departure_city:
        routes = db_interface.get_city_routes_departure_destination(
            *split_with_comma(destination_city), 'destination')
    if departure_city and destination_city and not departure_day:
        routes = db_interface.get_connection_city_state(
            *split_with_comma(departure_city),
            *split_with_comma(destination_city))

    if departure_city and destination_city and departure_day:
        departure = split_with_comma(departure_city)[0]
        destination = split_with_comma(destination_city)[0]
        day = DAY_STRING_TO_CHAR[departure_day]
        routes = data_pipeline.query_path(f'{departure},{destination},{day}')

    routes = list(routes)
    routes_sorted = data_pipeline.sort_route_time(routes)
    routes = {route['_id']: route for route in routes}
    routes_display = []
    for sort in routes_sorted:
        idx = sort[0]
        route = routes[idx]
        routes_display.append([
            route['_id'],
            route['name'],
            route['departure_city_name'],
            route['destination_city_name']])

    configure_item('Routes##'+window_id, items=routes_display)
    routes = pformat(routes)
    set_value('Details##txt'+window_id, routes)


def create_ticketing_window(sender, data):
    global g_window_counter
    window_id = str(g_window_counter)
    with window('Ticketing##Window'+window_id,
                width=800,
                height=800,
                x_pos=20,
                y_pos=20,
                on_close=on_window_close):

        with group('City Selector##'+window_id, width=200):
            departure_cities = [city[0]+','+city[1]
                                for city in db_interface.get_distinct_cities('departure')]
            departure_cities.insert(0, '')
            destination_cities = [city[0]+','+city[1]
                                  for city in db_interface.get_distinct_cities('destination')]
            destination_cities.insert(0, '')
            days = list(DAY_STRING_TO_CHAR.keys())
            days.insert(0, '')
            add_combo('Departure##'+window_id,
                      items=departure_cities, callback=update_routes_from_city_selection, callback_data=window_id)
            add_combo('Destination##'+window_id,
                      items=destination_cities, callback=update_routes_from_city_selection, callback_data=window_id)
            add_combo('Departure Day##'+window_id,
                      items=days, callback=update_routes_from_city_selection, callback_data=window_id)

        add_same_line(spacing=50)
        add_listbox('Routes##'+window_id, width=300,
                    items=[], callback=print_data)
        with child('Details##'+window_id):
            add_text('Details##txt'+window_id)
    g_window_counter += 1


def wipe_database(sender, data):
    db_interface.wipe_database()


def begin_gui():
    with window('PrimaryWindow'):
        with menu_bar('MenuBar'):
            with menu('Windows'):
                add_menu_item('Import Data##menu',
                              callback=create_import_data_window)
                add_menu_item('Drivers##menu',
                              callback=create_drivers_window)
                add_menu_item('Routes##menu',
                              callback=create_routes_window)
                add_menu_item('Ticketing##menu',
                              callback=create_ticketing_window)
                add_menu_item('[dev] Logger',
                              callback=show_logger)
                add_menu_item('[dev] Metrics',
                              callback=show_metrics)
                add_menu_item('[dev] Debug',
                              callback=show_debug)
            with menu('DB Admin'):
                add_menu_item('Clear Database', callback=wipe_database)

    set_main_window_title(TITLE)

    create_import_data_window(None, None)
    create_ticketing_window(None, None)

    data_pipeline.build_graph()

    start_dearpygui(primary_window='PrimaryWindow')


if __name__ == '__main__':
    begin_gui()
