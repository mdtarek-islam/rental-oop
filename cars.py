# Car, Hatchback, Sedan, and SUV classes holding their daily rates.
class Car:
    """
    Base class representing a car with daily rates 
    for different rental durations.

    Assumptions:
        For simplicity, the only currency being handled is the Great British Pound (GBP/£).

    Attributes:
        below_week_rate (int): Daily rate for rentals taken for less than a week.
        week_or_more_rate (int): Daily rate for rentals lasting a week or longer.
        vip_rate (int): Discounted daily rate for customers with a loyalty programme.
    """

    def __init__(self, below_week_rate: int, week_or_more_rate: int, vip_rate: int) -> None:
        """
        Initialises a Car instance with specific daily rates for different scenarios.

        Parameters:
            below_week_rate (int): Daily rate for rentals shorter than a week.
            week_or_more_rate (int): Daily rate for rentals of a week or more.
            vip_rate (int): Special, discounted daily rate for VIP customers.
        """
        self.below_week_rate = below_week_rate
        self.week_or_more_rate = week_or_more_rate
        self.vip_rate = vip_rate

    def get_below_week_rate(self) -> int:
        """Returns the daily rate for rentals shorter than a week."""
        return self.below_week_rate

    def get_week_or_more_rate(self) -> int:
        """Returns the daily rate for rentals of a week or more."""
        return self.week_or_more_rate

    def get_vip_rate(self) -> int:
        """Returns the discounted daily rate for VIP customers."""
        return self.vip_rate


class Hatchback(Car):
    """
    Hatchback car class with predefined daily rates.

    Inherits all the methods from the Car class and sets 
    specific daily rates.
    """

    def __init__(self) -> None:
        """
        Initialises a Hatchback instance with the following rates:
            - less than 7 days at £30 per day;
            - 7 days or more at £25 per day;
            - a special rate of £20 per day for VIP customers.
        """
        super().__init__(30, 25, 20)


class Sedan(Car):
    """
    Sedan car class with predefined rates.

    Inherits methods from Car class and specifies
    the daily rates.
    """

    def __init__(self) -> None:
        """
        Initialises a Sedan instance with the following rates:
            - less than 7 days at £50 per day;
            - 7 days or more at £40 per day;
            - a special rate of £35 per day for VIP customers.
        """
        super().__init__(50, 40, 35)


class SUV(Car):
    """
    SUV car class with determined daily rates.

    Inherits methods from Car class and states
    the daily rates.
    """
    
    def __init__(self) -> None:
        """
        Initialises a SUV instance with the following rates:
            - less than 7 days at £100 per day;
            - 7 days or more at £90 per day;
            - a special rate of £80 per day for VIP customers.
        """
        super().__init__(100, 90, 80)
