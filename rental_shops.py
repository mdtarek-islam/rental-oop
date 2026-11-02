# RentalShop class for rental transactions with a customer.
from customer import Customer, VIP # Aggregation, the customer and rental shop classes exist individually.
from cars import Car, Hatchback, Sedan, SUV # Composition, the classes only exist in this class.


class RentalShop:
    """
    A class to represent a car rental shop. Allows for rental transactions between the
    user and the shop, as well as signing in or out of the loyalty programme and display
    the stock of available cars.

    Attributes:
        rental_shop_name (str).
        available_car_types (dict): A dictionary which maps car type names to their
            class definitions, so each stocked car is a new instance.
        rental_shop_stock (dict): A dictionary mapping car type names to a list of available
            cars in the rental shop garage.
        vip_customers (list): A list of customers' names who are signed up to the shop's
            loyalty programme.
        is_open (bool): True if the shop is open, False if the shop is closed.
    """

    def __init__(self, rental_shop_name: str) -> None:
        """
        Initialises a RentalShop instance with the shop's name, the car types 
        they sell, empty stock and a predefined list of customers who are members
        of the loyalty programme.

        Assumptions:
            Only three car types are sold in the rental shops: hatchbacks,
                sedans and SUVs.
            Existing VIPs are named Customer1, Customer2 and Customer3, avoiding
                real names, with the '(VIP)' tag added as the identifier.

        Parameters:
            rental_shop_name (str).
        """
        self.rental_shop_name = rental_shop_name
        self.available_car_types = {
            "Hatchback": Hatchback,
            "Sedan": Sedan,
            "SUV": SUV
            } # Currently only three types of cars are sold on this platform.
        self.rental_shop_stock = {
            "Hatchback":[],
            "Sedan":[],
            "SUV":[]
            } # The stock is initially empty.
        self.vip_customers = [
            "Customer1(VIP)", 
            "Customer2(VIP)", 
            "Customer3(VIP)"
            ] # Assume 3 VIP customers exist.
        self.is_open = False # Shop is initially closed.

    def get_rental_shop_name(self) -> str:
        """Returns the shop's name."""
        return self.rental_shop_name

    def is_currently_open(self) -> bool:
        """Returns True while the shop is open for the session."""
        return self.is_open

    def open_shop(self) -> None:
        """Opens the shop and prints a welcome message."""
        print(f"Welcome to {self.rental_shop_name}!") # Friendly welcome message for better UX(User Experience).
        self.is_open = True

    def close_shop(self) -> None:
        """Closes the shop and prints a goodbye message."""
        print("\nThank you for stopping by! See you soon!") # Friendly exit message, improves UX.
        self.is_open = False
    
    # Private method, working only within the class.
    def __add_car(self, car_type: str, car: Car) -> None:
        """
        Adds a car to the stock for a specific car type.
        
        Parameters:
            car_type (str).
            car: The car object to add to the list.
        """
        self.rental_shop_stock[car_type].append(car)

    def is_returnable(self, car_type: str, car: Car) -> bool:
        """
        Checks if the car can be returned, if possible, adds it
        back to the shop's stock. The car must be an instance of
        the class this shop maps to the given car type.

        Parameters:
            car_type (str): the type of car to return to the rental shop.
            car: The car object being returned.

        Returns:
            bool: True if the car was successfully added back,
                False if there is no car, the car type does not exist,
                or the car does not match the car type.
        """
        car_class = self.available_car_types.get(car_type)
        if car is None or car_class is None: # No car held, or type not sold here.
            return False
        if not isinstance(car, car_class): # Car type must match the shop's inventory.
            return False
        self.__add_car(car_type, car)
        return True # The car can be returned and is successfully added.

    def add_to_stock(self, car_type: str, amount: int) -> None:
        """
        Adds a specified number of cars to the stock for a specific
        car type.

        Parameters:
            car_type (str): The type of car to add to the rental shop's stock.
            amount (int): The number of cars to add to the garage.

        Raises:
            KeyError: If the shop does not sell the car type.
        """
        car_class = self.available_car_types[car_type]
        for _ in range(amount):
            self.__add_car(car_type, car_class()) # A new, separate car each time.

    def display_stock(self) -> None:
        """
        Displays a summary of the stock for each type of car, including
        the total stock count.
        """
        sum_of_cars = 0
        stock_summary = "| "

        # Iterate through the stock dictionary to build the stock summary text.
        for car_type in self.rental_shop_stock:
            amount_of_cars = len(self.rental_shop_stock[car_type])
            stock_summary += car_type + ": " + str(amount_of_cars) + " | "
            sum_of_cars += amount_of_cars
        
        print(
            "\n################STOCK################\n"
            + stock_summary 
            + f"\nTotal: {sum_of_cars}\n"
            "#####################################"
            )

    def handout_car(self, car_type: str) -> Car:
        """
        Removes and returns a car from stock of the specified type.

        Assumptions:
            Following the LIFO (Last-In First-Out) approach, the last
            car added to the stock will be the first one to be rented.
            This is carried out for simplicity.

        Parameters:
            car_type (str): The type of car to rent out.

        Returns:
            The car object that was rented out.

        Raises:
            ValueError: If no car of this type is in stock.
        """
        if not self.is_available(car_type):
            raise ValueError(f"No {car_type} is available.")
        return self.rental_shop_stock[car_type].pop() # Returns the last car from the list (LIFO).
    
    def is_available(self, car_type: str) -> bool:
        """
        Checks if there are any cars available in the garage for the specific
        car type.

        Parameters:
            car_type (str): The type of car to check availability for.

        Returns:
            bool: True if at least one car of the type is in stock, otherwise False.
        """
        try:
            return len(self.rental_shop_stock[car_type]) > 0 # True if at least one car of that type is in stock.
        except KeyError: # Type of car is not sold in this shop.
            return False
    
    def get_rate(self, car: Car, num_days: int, is_vip: bool) -> int:
        """
        Retrieves the rate for renting a car based on the rental duration
        and the VIP status of the customer.

        Assumptions:
            The rate is kept as an integer value.
            For simplicity, the only currency involved is £.

        Parameters:
            car: The car object being rented.
            num_days (int): The number of days the car is rented for.
            is_vip (bool): Indicates if the customer is part of the
                loyalty programme.

        Returns:
            int: The rental rate for the customer type and 
                specified duration (£/day).
        """
        if is_vip: # Special rate no matter how many days.
            return car.get_vip_rate()
        
        if num_days < 7: # Conditional rate for regular customers.
            return car.get_below_week_rate()
        else:
            return car.get_week_or_more_rate()    

    def get_price(self, rate: int, num_days: int) -> int:
        """
        Calculates the total price of a rental from the rate 
        and length of time the car is rented for.

        Parameters:
            rate (int): The daily rate for renting the car.
            num_days (int): The number of days the car will or
                is rented for.

        Returns:
            int: The total price of the rental, in £.
        """
        return rate * num_days   

    def upgrade_customer(self, client: Customer) -> VIP:
        """
        Signs the customer up to the loyalty programme, 
        adding them to the VIP list.

        Parameters:
            client (Customer): The customer being upgraded to VIP.

        Returns:
            vip_client (VIP): A new VIP object with the customer's details transferred.
        """
        print("You have now joined our loyalty programme!")
        vip_customer_name = client.get_customer_name() + "(VIP)" # Add VIP tag.
        vip_client = VIP(vip_customer_name)
        vip_client.transfer_customer_details(client)
        self.vip_customers.append(vip_customer_name)
        return vip_client    

    def downgrade_vip_customer(self, vip_client: VIP) -> Customer:
        """
        Downgrade a VIP customer back to a regular customer status,
        as they have decided to leave the loyalty programme, removing
        the VIP privileges.

        Assumptions:
            All VIP customers have a '(VIP)' tag at the end of their name.

        Parameters:
            vip_client (VIP): The VIP customer being downgraded.

        Returns:
            client (Customer): A new Customer object with the VIP's
                details transferred.
        """
        print(
            "We are sorry to have you leave our loyalty programme...\n"
            "You are welcome to sign up again anytime!"
            )
        vip_customer_name = vip_client.get_customer_name()
        client = Customer(vip_customer_name.removesuffix("(VIP)")) # Remove the VIP tag.
        client.transfer_vip_customer_details(vip_client)
        if vip_customer_name in self.vip_customers:
            self.vip_customers.remove(vip_customer_name)
        return client
