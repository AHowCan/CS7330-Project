# why config.py and not config.json or yml?
# json and yml mainly reduce power to the user
# since this is a student project this does not matter, so just plain py is one less hoop to jump over
from local_config import USE_LOCAL_CONFIG

TEST_DB_URI = 'mongodb+srv://test_user:ZhvWpinMdYkZ1yzv@cluster0.0qxsh.mongodb.net/bus_network?retryWrites=true&w=majority'

DB_NAME = 'bus_network'
COL_DRIVERS = 'drivers'
COL_ROUTES = 'routes'

CANVAS_DATA_PATH = 'data_canvas/'
CUSTOM_DATA_PATH = 'data_custom/'

# easily switch between canvas and custom data
DATA_PATH_TO_USE = CUSTOM_DATA_PATH

ASSIGNMENT_FILE = 'Assignment.csv'
DRIVER_FILE = 'Driver.csv'
ROUTES_FILE = 'Routes.csv'

# used for sorting assignment days
DAY_OF_WEEK_VALUES = {'s': 0, 'M': 1, 'T': 2, 'W': 3, 'U': 4, 'F': 5, 'S': 6}
FIRST_DAY_OF_WEEK = 's'
WEEKDAYS = ['M', 'T', 'W', 'U', 'F']
WEEKENDS = ['S', 's']
MINUTES_IN_WEEK = 7 * 24 * 60

ROUTE_TYPE_VALID_DAYS = {'0': WEEKDAYS + WEEKENDS,
                         '1': WEEKDAYS,
                         '2': WEEKENDS
                         }

# the larger this is, the less rest time drivers get (in minutes)
REST_TIME_EPSILON = 0.1

if USE_LOCAL_CONFIG:
    from local_config import *
