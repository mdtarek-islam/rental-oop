# Procedural code for the rental platform.
"""
Command-line entry point for the RentalOOP car rental platform.

Run interactively with:
    python main.py

Skip the loading pauses with:
    python main.py --no-delay

Tests drive the same menu through run(), passing scripted answers
as input_func and a zero delay.
"""
import argparse
import time
from typing import Callable, Optional

from customer import Customer
from rental_shops import RentalShop

InputFunc = Callable[[str], str]

DEFAULT_DELAY = 0.5 # Seconds per loading step.


def load(delay: float = DEFAULT_DELAY) -> None:
    """
    Provides a short pause, simulating the loading of different webpages.
    Enables better user experience (UX), as information is not
    loaded suddenly.

    Parameters:
        delay (float): Seconds per step. Zero removes the pause.
    """
    for i in range(3):
        time.sleep(delay)
        print(".")
    time.sleep(delay)


def expected_int(answer: str, input_func: InputFunc = input) -> int:
    """
    Validates the user input to ensure it can be converted
    to an integer. If the input is not an integer, it requests
    the user to re-enter a valid number.

    Assumptions:
        The user eventually enters a whole number (integer).

    Parameters:
        answer (str): The user's input which is expected to be
            an integer.
        input_func (callable): Reads the next answer from the user.

    Returns:
        answer (int): A valid integer input from the user.
    """
    correct = False
    while not correct:
        try:
            answer = int(answer) # Attempt to convert input to an integer.
        except ValueError:
            # Failed conversion prompts the user to enter a valid number.
            answer = input_func(
                "You should enter a number, try again.\n\n"
                "Your choice: "
                )
        else:
            correct = True # Exit the loop.

    return answer


def expected_positive_int(answer: str, input_func: InputFunc = input) -> int:
    """
    Validates that the user input is a whole number greater than zero.
    Used for the number of rental days, so a bill can never be zero
    or negative.

    Parameters:
        answer (str): The user's input.
        input_func (callable): Reads the next answer from the user.

    Returns:
        int: A whole number of 1 or more.
    """
    number = expected_int(answer, input_func)
    while number < 1:
        number = expected_int(
            input_func(
                "Please enter a whole number of days greater than zero.\n"
                "Your choice: "
                ),
            input_func,
            )
    return number


def go_back(input_func: InputFunc = input, delay: float = DEFAULT_DELAY) -> None:
    """
    Pauses the program until the user presses the enter key to proceed.
    Useful for providing the user with time to read messages.

    Assumptions:
        The user eventually presses the enter key, as all other keys
        lead to nothing.
    """
    input_func("\n(Press ENTER key to go back.)")
    load(delay)


def parse_car_type(text: str) -> str:
    """
    Formats a typed car type to match the shop's stock keys,
    for example 'hatchBACK' becomes 'Hatchback' and 'suv' becomes 'SUV'.

    Parameters:
        text (str): The car type as typed by the user.

    Returns:
        str: The formatted car type.
    """
    car_type = text.strip().lower().title() # Ensure correct formatting.
    if car_type == "Suv": car_type = "SUV" # Special case as all letters are capital.
    return car_type


def build_shop() -> RentalShop:
    """
    Creates the 'RentACar' shop with 4 hatchbacks, 3 sedans and 3 SUVs.

    Assumption: For simplicity, only one shop exists in this platform.

    Returns:
        RentalShop: The stocked shop, still closed.
    """
    shop = RentalShop("RentACar")
    # Currently only 3 types of cars available: hatchback, sedan and SUV
    shop.add_to_stock("Hatchback", 4)
    shop.add_to_stock("Sedan", 3)
    shop.add_to_stock("SUV", 3) # Can add more car types later on.
    return shop


def rent_option(shop: RentalShop, client: Customer, input_func: InputFunc, delay: float) -> None:
    """Menu option 1: rent a car of a chosen type for a number of days."""
    if client.is_renting_a_car(): # Customer already has a car.
        print(
            "\nUnfortunately we only rent one car per customer.\n"
            f"We appreciate your compliance with the {shop.get_rental_shop_name()} company policy."
            )
    else:
        load(delay)
        car_type = parse_car_type(input_func("\nSelect car type: "))

        if shop.is_available(car_type):
            num_days = input_func(
                "For how many days do you want to rent?\n"
                "Your choice: "
                )
            num_days = expected_positive_int(num_days, input_func) # Whole days, 1 or more.
            car = shop.handout_car(car_type) # Retrieve car from shop stock.

            print("\nHanding the car over.")
            load(delay)
            client.rent_car(car, car_type, num_days) # Provide car rental details to the customer.

            rate = shop.get_rate(car, num_days, client.is_vip())
            print(
                f"You have rented a {car_type} car for {num_days} days.\n"
                f"You will be charged £{rate} per day.\n"
                "We hope that you enjoy our service!"
                )
        else: # Car type unavailable, either not sold or not currently in stock.
            print(
                f"\nUnfortunately no {car_type} is available.\n"
                "We apologise for any inconvenience caused.\n"
                "Please check our available cars to rent through the main menu."
                )

    go_back(input_func, delay) # Wait for user input to proceed.


def view_option(shop: RentalShop, input_func: InputFunc, delay: float) -> None:
    """Menu option 2: show the stock of each car type and the total."""
    print("Checking available cars.")
    load(delay)
    shop.display_stock() # Display stock of each car type and total stock.
    go_back(input_func, delay)


def return_option(shop: RentalShop, client: Customer, input_func: InputFunc, delay: float) -> None:
    """Menu option 3: return the rented car and display the bill."""
    if not client.is_renting_a_car(): # Nothing to return, so leave the garage untouched.
        print("\nUnfortunately you have no car to return.")
        go_back(input_func, delay)
        return

    details = client.return_car() # Retrieve rental details from the customer.
    car, car_type, num_days = details["car"], details["type"], details["days rented"]

    if shop.is_returnable(car_type, car): # Check if the car type is valid and can be returned.
        print("Retrieving the car.")
        load(delay)

        print(
            "Thank you for returning the car to us!\n"
            "\n"
            "Calculating the bill."
            )
        load(delay)

        # MVP behaviour (report section 4.3): the rate uses the status at return time.
        rate = shop.get_rate(car, num_days, client.is_vip())
        price = shop.get_price(rate, num_days)
        # Display the bill.
        print(
            "####################BILL####################\n"
            f"You have rented a {car_type} car for {num_days} days.\n"
            f"Your daily rate is £{rate}.\n"
            f"Amount to pay: £{price}\n"
            "Please pay the amount online or in-store.\n"
            "############################################\n"
            "\n"
            "Thank you for using our service!\n"
            "Have a good day!"
            )
    else: # The car type is invalid for this shop.
        client.rent_car(car, car_type, num_days) # Give the car back to the customer.
        print("\nUnfortunately this car cannot be returned to this shop.")

    go_back(input_func, delay)


def loyalty_option(shop: RentalShop, client: Customer, input_func: InputFunc, delay: float) -> Customer:
    """
    Menu option 4: join or leave the loyalty programme.

    Returns:
        Customer: The same client, or the upgraded or downgraded account.
    """
    print("\nRetrieving details.")
    load(delay)

    if client.is_vip(): # Check if the customer is already a VIP.
        print(
            "You are part of our loyalty programme!\n"
            "Enjoy our discounted rental rates!"
            )

        # Offer option to leave the loyalty programme.
        downgrade = input_func("Press y to downgrade: ").strip().lower()
        if downgrade == "y":
            print(f"Downgrading {client.get_customer_name()} and transferring details.")
            load(delay)

            client = shop.downgrade_vip_customer(client) # Regular customer.
            go_back(input_func, delay)
        else:
            load(delay) # Pause briefly and go back to the main menu.

    else: # The customer has not signed up.
        print(
            "You have not signed up for the loyalty programme.\n"
            "Join us to access exclusive benefits, including discounted rates!"
            )

        # Offer option to sign up to the loyalty programme.
        upgrade = input_func("Press y to upgrade: ").strip().lower()
        if upgrade == "y":
            print(f"Upgrading {client.get_customer_name()} and transferring details.")
            load(delay)

            client = shop.upgrade_customer(client) # VIP customer.
            go_back(input_func, delay)
        else:
            load(delay) # Pause briefly and go back to the main menu.

    return client


def run(
    input_func: InputFunc = input,
    delay: float = DEFAULT_DELAY,
    shop: Optional[RentalShop] = None,
) -> Customer:
    """
    Runs one session of the platform: log in, then loop over the menu
    until the user picks option 5.

    Parameters:
        input_func (callable): Reads each answer. Defaults to the keyboard.
        delay (float): Seconds per loading step. Zero for tests.
        shop (RentalShop): The shop to use. Defaults to build_shop().

    Returns:
        Customer: The customer account at the end of the session.
    """
    if shop is None:
        shop = build_shop()

    shop.open_shop()
    load(delay) # Short pause for better user experience.

    # Simple login by entering just a name.
    # Assumption: For simplicity, the user does not require any further information
    #   in order to log in to the rental platform.
    client_name = input_func("You are not logged in.\n"
                             "Please enter your name: "
                             )
    # Assumption: Customer is initially a regular customer who has not
    #   signed up to the loyalty programme.
    client = Customer(client_name) # Instantiate a new regular customer with the provided name.
    load(delay)

    # Main program loop.
    while shop.is_currently_open():
        option = input_func(
            f"{client.get_customer_name()}, what would you like to do?\n"
            "1) Rent a car.\n"
            "2) Check available cars.\n"
            "3) Return car.\n"
            "4) Loyalty programme.\n" # Enables upgrading and downgrading the customer status.
            "5) Exit.\n"
            "\n" # Blank line for readability.
            "Your choice: "
            )

        option = expected_int(option, input_func) # All options are integers.

        if option == 1:
            rent_option(shop, client, input_func, delay)
        elif option == 2:
            view_option(shop, input_func, delay)
        elif option == 3:
            return_option(shop, client, input_func, delay)
        elif option == 4: # Check or modify VIP status.
            client = loyalty_option(shop, client, input_func, delay)
        elif option == 5: # Exit the program.
            shop.close_shop()
            load(delay) # Short delay for friendly exit message.
        else: # Handle invalid options.
            print("Invalid option, choose between the available choices (1 to 5).")

    return client


def main(argv: Optional[list] = None) -> int:
    """
    Parses command-line flags and starts an interactive session.

    Returns:
        int: Exit status, 0 on a normal exit.
    """
    parser = argparse.ArgumentParser(description="RentalOOP car rental platform.")
    parser.add_argument(
        "--no-delay",
        action="store_true",
        help="skip the loading pauses between screens",
        )
    args = parser.parse_args(argv)
    try:
        run(delay=0 if args.no_delay else DEFAULT_DELAY)
    except (KeyboardInterrupt, EOFError): # Ctrl+C or closed input still exits gracefully.
        print("\nThank you for stopping by! See you soon!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
