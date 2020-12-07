# Developer Manual

## Input parsing implementation notes:

- The functions `parse_routes` `parse_driver` `parse_assignment` loop through all the lines that have been tokenized by the built in python module `csv.reader`
- For errors in parsing, a custom Exception `ParseError` is raised, and that line is skipped.
- All leading and trailing whitespace is trimmed from tokens. 
- All tokens are checked against a whitelist of characters (`ALLOWED_CHARS` in `config.py`). All characters not in the whitelist are removed.

The input parser checks the following and will skip that line if check fails:

- wrong number of fields/tokens per line
- illegal chars in day_of_week (see config.py)
- only integers are allowed for departure / arrival times and the times must be sensible
- route_type_code only accepts '0' '1' '2'

The input parser will auto-correct input for the following:

- First (and only first) letter of city should be capitalized
- Same as above for driver names
- State code should all be capital letters
- All letters in route IDs should be capital

Special characters (ascii) are allowed for city/route/driver names. This should not be a problem since python will escape out special chars when needed and mongodb seems to support them, but include tests to verify this [!@#$%^&*()_-+=[]{};:'",<>./\|?~`].
Non-ascii characters are not allowed, have tests for this.



## Restrictions:

1) A driver cannot be driving more then one bus at a time. Whenever an assignment is given to a driver, it will first check if this new assignment overlaps any previous assignment routes. If an assignment is found, it will inform the user that there is a conflict with the new assignment.

2) A driver must be given enough rest (defined to be half the duration of his previous route before taking on the next assignment)

3) If the departure city of a driver’s next assignment is not the same as the destination of his current assignment. He/She can either take bus(es) from the company that will lead the driver to its next assignment (notice that connecting through multiple buses are allowed), or he/she has to be given 48 hours to reach the next assignment. For now only the 48 hour constraint is checked.

4) The driver should be assigned a route that reaches his/her hometown. Once the driver arrived at his hometown, he/she should be allowed at least 18 hours of rest before the next assignment. (If 18 hours is not enough rest based on condition 2, he/she need to be given more).

### Implementation notes for Restrictions 2) - 4):

- These are implemented in `class DriverConstraintCheck`.
- The reason that these are grouped together is because they share much of the same data, and the class encapsulates/caches that data.
- Without such caching there would be multiple duplicate queries to the database for these constraints, that are usually check together.
- Since the database only stores a reference to the routes and not all the information of the routes, the class will gather all the unique routes that a driver is assigned to.
- The class also calculates and stores the time in minutes since Sunday - for all the assignments of the driver.



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
EXAMPLE:
>John,Doe
    Driver: John Doe, ID:100A, Age:40, Home Town:Dallas, TX
        Assignments:
        - Route Number 1, Day of the week - M
        - Route Number 1, Day of the week - U
    Driver: John Doe, ID:101A, Age:20, Home Town:Houston, TX
        Assignments:
        No assignments

Query City:
This query requests the user to provide a name of a city. It will query the database for all routes that contains this city as a departure or destination. If no routes exist it will return stating such.

INPUT:City1
EXAMPLE:
>Dallas
Route ID: 1, Name: Route_1, Departing Dallas, TX at 7:0, and arriving at Houston, TX after 5 hours and 15 minutes on day of week code:0
Route ID: 4B7, Name: Express, Departing Dallas, TX at 15:30, and arriving at Houston, TX after 4 hours and 30 minutes on day of week code:1

Query Route:
You can query all the information for a specific route by providing the route ID as well as the drivers assigned to the route.

INPUT:route_number
EXAMPLE OUTPUT:
>1
Route ID: 1, Name: Route_1, Departing Dallas, TX at 7:0, and arriving at Houston, TX after 5 hours and 15 minutes on day of week code:0
	Driver ID:100A, Name: John Doe
	Driver ID:100B, Name: Jack Doe
	Driver ID:100C, Name: Mary Doe

Query Connection:
This query requests the user to provide two city names and will query the database for any routes that go from the first city given to the second city given. If no routes exist it will return stating such.
INPUT:City1,City2
EXAMPLE:
>Dallas,Houston
Route ID: 1, Name: Route_1, Departing Dallas, TX at 7:0, and arriving at Houston, TX after 5 hours and 15 minutes on day of week code:0
	Driver ID:100A, Name: John Doe
	Driver ID:100B, Name: Jack Doe
	Driver ID:100C, Name: Mary Doe
Route ID: 4B7, Name: Express, Departing Dallas, TX at 15:30, and arriving at Houston, TX after 4 hours and 30 minutes on day of week code:1
	Driver ID:100A, Name: John Doe
	Driver ID:100D, Name: Brad Doe
	Driver ID:B933, Name: George Lam


Query Path: 
This query requests for two city names along with the single letter code for the day of departure. It begins by finding the shortest path based on traveling time for each route using Dijkstra's algorithm. It then begins to loop through each hop and tracks the time for traveling on a bus with time spent in a city waiting for the next route. If there exists multiple routes between two cities, it will evaluate them all and pick the quickest route based on time spent traveling on the bus. At the end of the route, if the total time is not more than the max time allowed for a path between two cities, it returns the route ID for each hop.
INPUT:City1,City2,DayCode
EXAMPLE:
>Dallas,Waco,M
The Route is from Dallas, TX to Houston, TX from Houston, TX to Waco, TX  
	Route ID: 4B7 Dallas, TX - Houston, TX, leaving 15:30, arriving after 4 hours and 30 minutes
	Route ID: 2 Houston, TX - Waco, TX, leaving 23:0, arriving after 1 hours and 0 minutes

## GUI implementation notes

- It will help if you familiarize yourself with the `dearpygui` package before developing on the GUI
- Most implementation details are straightforward once you are familiar with the design patterns common to `dearpygui`
- For the following windows types - `ticketing_window`, `routes_window`, `drivers_window` - multiple windows can co-exist. These windows do not share data other than the database. 
  - This is accomplished using the `window_id` that increments for each new window.
  - All window components and variable names are then appended with the `window_id`. 
  - This allows components of the same window to communicate with each other while maintaining separate state across different windows.