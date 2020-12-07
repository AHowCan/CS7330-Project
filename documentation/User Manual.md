Team 0: Bus Network System
User Manual
v1.0
---------------------------------

Purpose:
The system is used to keep track of routes between cities, the drivers for the buses and their assignments. To provide an easy querying tool to retrieve this information. Drivers, routes and assignments can all be entered in by provided the names of the CSV files.


Adding Data:

You can add data by providing the file names for drivers, routes and assignments.
EXAMPLE INPUT:
>driver.csv,routes.csv,assignments.csv


Query Options:

Query Driver:
You can query the info of a driver by providing the first and last name of the driver. It will provide the following details about that driver. 
    - Driver ID
    - First name
    - Last name
    - Age
    - Hometown city name
    - Hometown state name
    - Assignments:
        - Route ID
        - Day of the week

INPUT:FIRSTNAME,LASTNAME
EXAMPLE OUTPUT:
>John,Doe
    Driver: John Doe, ID:100A, Age:40, Home Town:Dallas, TX
        Assignments:
        - Route Number 1, Day of the week - M
        - Route Number 1, Day of the week - U
    Driver: John Doe, ID:101A, Age:20, Home Town:Houston, TX
        Assignments:
        No assignments

Query City:
You can query a city by providing the name to get all the routes that depart or arrive there in chronological order. The route information is below and will be given for each route.
    - Route ID
    - Name of Route
    - Departing city and state code
    - Departing time
    - Destination city and state code
    - travel time

INPUT:City1
EXAMPLE OUTPUT:
>Dallas
Route ID: 1, Name: Route_1, Departing Dallas, TX at 7:0, and arriving at Houston, TX after 5 hours and 15 minutes on day of week code:0
Route ID: 4B7, Name: Express, Departing Dallas, TX at 15:30, and arriving at Houston, TX after 4 hours and 30 minutes on day of week code:1

Query Route:
You can query all the information for a specific route by providing the route ID as well as the drivers assigned to the route. The following is the information for the route.
    - Route ID
    - Name of Route
    - Departing city and state code
    - Departing time
    - Destination city and state code
    - travel time
    - Driver ID and name

INPUT: Route_number
EXAMPLE OUTPUT:
>1
Route ID: 1, Name: Route_1, Departing Dallas, TX at 7:0, and arriving at Houston, TX after 5 hours and 15 minutes on day of week code:0
	Driver ID:100A, Name: John Doe
	Driver ID:100B, Name: Jack Doe
	Driver ID:100C, Name: Mary Doe

Query Connection:
You can query for all the direct routes between two cities by giving the name of the two cities. It will display the route along with it's info. If there are multiple routes, it will display them all. Below is the route information provided.
    - Route ID
    - Route Name if applicable
    - Departure city name and state code
    - Destination city name and state code
    - Route type code
    - Departure hour of the day and minute of the hour
    - The amount of hours to reach the destination and the remaining minutes

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
You can query for a path that leads from one city to another. You will need to provide the departing city, destination city and the day of the week in code format, see below for the codes. They do not have to be directly connected cities. If they are not, it will return the routes needed to get to the final destination.

INPUT:City1,City2,DayCode
EXAMPLE:
>Dallas,Waco,M
The Route is from Dallas, TX to Houston, TX from Houston, TX to Waco, TX  
	Route ID: 4B7 Dallas, TX - Houston, TX, leaving 15:30, arriving after 4 hours and 30 minutes
	Route ID: 2 Houston, TX - Waco, TX, leaving 23:0, arriving after 1 hours and 0 minutes



Other Notes:

At any time you will be able to type the following for their corresponding action.
back - which will return you to the previous decision
help - to see these options again
quit - to exit the program

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