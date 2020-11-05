"""
TODO:
    Austin
        - Continue with creating user interactions
        - Create method for reading CSV file
        - Class definitions for driver and route

"""

def begin_UI():
    print("\n\tWelcome to the Bus Network System\n\n" \
                    "Please make one of the following selections, 1 or 2...\n" \
                    "1) Add data\n" \
                    "2) Query database")
    response = get_input_and_validation()

    if response == "1":
        print("Would you like to add a driver or route?\n" \
                "1) Driver\n" \
                "2) Route")
        response = response = get_input_and_validation()

        # TODO: Call method to read csv for driver or route

    elif response == "2":
        print("What would you like to query?")


def get_input_and_validation():
    response = input(">")
    while response != "1" and response != "2":
        print("Unknown response...\n" \
                "Try again")
        response = input(">")

    return response 



