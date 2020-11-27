# TODO

[Donald] Make some more mock data (we are not testing all constraints/conflicts)
    - Routes with long travel times (docs say the upper limit is 72 hours)
    - Cases where the driver is assigned an assignment that he cannot take because he has not finished the previous multi-day assignment (Constraint 1)
    - Cases where the driver is not given enough rest (Constraint 2)
    - Driver cannot reach next assignment in time (Constraint 3)
    - Driver does not have assignment to home town (Constraint 4)
    - Driver did not get enough rest at hometown (Constraint 4)
    - Invalid characters / incorrect number of fields on a line.

[Donald] Check for Invalid characters / incorrect number of fields.

DONE - [Austin] Constraint 1: A driver cannot be driving more than one bus that travel at the same time.(current implementation does not take travel time into consideration)

[Tony] Constraint 2: A driver must be given enough rest (defined to be half the duration of his previous route before taking on the next assignment)

[Tony] Constraint 3: If the departure city of a driver’s next assignment is not the same as the destination of his current assignment. He/She can either take bus(es) from the company that will lead the driver to its next assignment (notice that connecting through multiple buses are allowed), or he/she has to be given 48 hours to reach the next assignment.

[Tony] Constraint 4: The driver should be assigned a route that reaches his/her hometown. Once the driver arrived at his hometown, he/she should be allowed at least 18 hours of rest before the next assignment. (If 18 hours is not enough rest based on condition 2, he/she need to be given more).

[Austin] Query 1: The program should get the name of a driver (first and last), and print out the driver’s information, together with the route that the driver is assigned to. (If there is multiple drivers that satisfies the query, print them all (one after the other)).

[Austin] Query 2 The program should get the name of a city, and print out all the routes that go through the city (separate departure and destination, order by time: assume Sunday 00:00 am is the starting time).

[Austin] Query 3 The program should get the route of a bus and print out all information about the route, including the name and ID of the driver that is assigned to it.

[Austin] Query 4 The program should get the name of two cities, and response if there is a bus route that go from the first city directly to the second. If so, print all info about that route (as the previous query). If there is more than one, print them all (one after the other)

[Tony] Bonus 1 Query 5 The program should get the name of two cities, and a day of the week (Sunday/Monday … etch.) and response if there is a way to get from the first city to the second, either by a single bus route, or by connecting buses, leaving on that day of the week. If connection is used, the total time from departure to arrival should be less than or equal to 72 hours. For each possible routes, list all the bus routes that is used. You should show departure and arrival time for the bus route. For example:
Chicago, IL to Cleveland, OH
Route 78 Chicago IL – Cleveland OH, leaving Monday 7:15am, arriving Monday 12:15pm
Route 73 Chicago IL – Detroit MI, leaving Monday 8:15 am, arriving Monday 10:20 am
Route A36 Detroit MI – Cincinnati OH, leaving Monday 11:35 am, arriving Monday 5:10 pm
Route 88OH Cincinnati OH – Cleveland OH, leaving Tuesday 8:15 am, arriving Tuesday 12:05 pm

[Donald] Bonus 2 GUI Provide a GUI interface to your program. If you want, you can leverage the web browser as the GUI. Functionality is the most important part, aesthetics counts only a minor part of the grade

[Tony] Developer Manual

[Donald] User Manual

[Tony] Video
