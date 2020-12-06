
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

EXAMPLE INPUT:John,Doe

Query City:
You can query a city by providing the name to get all the routes that depart or arrives there in chronological order. The route information is below.





Query Connection:
You can query for all the direct routes between two cities by giving the name of the two cities. It will display the route along with it's info. If there are multiple routes, it will display them all. Below is the route information provided.
    - Route ID
    - Route Name if applicable
    - Departure city name
    - Departure city code
    - Destination city name
    - Destination city code
    - Route type code
    - Departure hour of the day
    - Departure minute of the hour
    - The amount of hours to reach the destination
    - The amount of minutes for the last hour to reach the destination

EXAMPLE:Dallas,Houston

Query Path:
You can query for a path that leads from one city to another. You will need to provide the departing city, destination city and the day of the week in code format, see the above section for the codes. They do not have to be directly connected cities. If they are not, it will return the routes needed to get to the final destination.

EXAMPLE:Dallas,Houston,M