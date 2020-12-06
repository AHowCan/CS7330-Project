# Developer Manual

## Overview

### config.py

### connect.py

### data_pipeline.py

### db_interface.py

### graph_controller.py

### gui.py

### input_parser.py

### local_config.py

### logger.py

### main.py

### user_interface.py


Restrictions:
1) A driver cannot be driving more then one bus at a time. Whenever an assignment is given to a driver, it will first check if this new assignment overlaps any previous assignment routes. If an assignment is found, it will inform the user that there is a conflict with the new assignment.

2)

3)

4)


When querying or inputing data, you may need to use a code for the day of the week or the route code for when the route runs. Below are the following codes and what they correspond to.

The following is a one letter code that corresponds to the day of the week.
Day of week codes:
    M = Monday
    T = Tuesday
    W = Wednesday
    U = Thursday
    F = Friday
    S = Saturday
    s = Sunday

The following route codes corresponds what part of the week it will run.
Route Codes:
    0 = Daily
    1 = Weekdays only
    2 = Weekends only


Query Options:

Query Driver:
This query requests the user to provide the first and last name of a driver, separated by a comma. It will print out all drivers that match the the first and last name and all details for each. If no drivers match the first and last name, it will return stating such.
INPUT:FIRSTNAME,LASTNAME
EXAMPLE:John,Doe

Query City:
This query requests the user to provide a name of a city. It will query the database for all routes that contains this city as a departure or destination. If no routes exist it will return stating such.
INPUT:City1
EXAMPLE:Dallas

Query Connection:
This query requests the user to provide two city names and will query the database for any routes that go from the first city given to the second city given. If no routes exist it will return stating such.
INPUT:City1,City2
EXAMPLE:Dallas,Houston

Query Path: 
This query requests for two city names along with the single letter code for the day of departure. It begins by finding the shortest path based on traveling time for each route using Dijkstra's algorithm. It then begins to loop through each hop and tracks the time for traveling on a bus with time spent in a city waiting for the next route. If there exists multiple routes between two cities, it will evaluate them all and pick the quickest route based on time spent traveling on the bus. At the end of the route, if the total time is not more than the max time allowed for a path between two cities, it returns the route ID for each hop.
INPUT:City1,City2,DayCode
EXAMPLE:Dallas,Houston,M