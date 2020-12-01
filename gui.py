from dearpygui.core import (show_logger,
                            set_main_window_title,
                            start_dearpygui,
                            does_item_exist,
                            log_debug,
                            add_menu_item,
                            add_button,
                            add_text,
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
                              menu)

import db_interface
import data_pipeline
from datetime import datetime
from config import (ASSIGNMENT_FILE,
                    DRIVER_FILE,
                    ROUTES_FILE)
from os import path


TITLE = 'Our buses do not smell! Okay, maybe a little. But only in the summer. Oh alright, they smell damn awful in the summer. [SIGHING SOUND] [END OF AUTOMATED VOICE TRANSCRIPT]'

SELECTED_FOLDER_VAR = 'SELECTED_FOLDER_VAR'
FILES_FOUND_STR_VAR = 'FILES_FOUND_STR_VAR'

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
        prompt_text += '\nSome files are missing, please ensure that they are exist and are named correctly'

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

        with window('Import Data##Window', on_close=on_window_close):
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


def wipe_database(sender, data):
    db_interface.wipe_database()


with window('PrimaryWindow'):

    with menu_bar('MenuBar'):
        with menu('Windows'):
            add_menu_item('Import Data##menu',
                          callback=create_import_data_window)
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

start_dearpygui(primary_window='PrimaryWindow')
