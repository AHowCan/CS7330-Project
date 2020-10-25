Database bus_network:
  Collection drivers:
    _id: string, 5 character max (unique)
    name_last: string
    name_first: string
    age: int
    hometown_city: string (unique by state)
    hometown_state: string, 2 letters
    routes: array of Trip objects
      Trip Object:
        route_id: string, 5 character max, comes from routes collection (unique)
        day_of_week: char
  Collection routes:
    _id: string, 5 character max (unique)
    name: string (may be empty)
    departure_city: string (unique by state)
    departure_state: string, 2 letters
    destination_city: string (unique by state)
    destination_state: string, 2 letters
    type_id: int ( 0, 1, or 2)
    travel_hours: int
    travel_minutes: int
    departure_hour: int
    departure_minutes: int
