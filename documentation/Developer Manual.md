
Query Connection:
This query requests the user to provide two city names and will query the database for any routes that go from the first city given to the second city given. If no routes exist it will return stating such.

Query Path: 
This query requests for two city names along with the single letter code for the day of departure. It begins by finding the shortest path based on traveling time for each route using Dijkstra's algorithm. It then begins to loop through each hop and tracks the time for traveling on a bus with time spent in a city waiting for the next route. If there exists multiple routes between two cities, it will evaluate them all and pick the quickest route based on time spent traveling on the bus. At the end of the route, if the total time is not more than the max time allowed for a path between two cities, it returns the route ID for each hop.