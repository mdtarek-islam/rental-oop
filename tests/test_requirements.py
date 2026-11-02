"""One test per requirement in rental_oop.pdf (Appendix A, Appendix B, section 2)."""
import time

import main
from cars import SUV, Hatchback, Sedan
from customer import VIP, Customer

INITIAL = {"Hatchback": 4, "Sedan": 3, "SUV": 3}


def stock_counts(shop):
    return {car_type: len(cars) for car_type, cars in shop.rental_shop_stock.items()}


# Section 2.1.1: main.py initialises RentACar with 4 hatchbacks, 3 sedans and 3 SUVs.
def test_s211_main_initialises_rentacar_with_initial_stock(shop):
    assert shop.get_rental_shop_name() == "RentACar"
    assert stock_counts(shop) == INITIAL


# Section 2.1.1: each car type sets its own daily rates.
def test_s211_car_subclasses_define_daily_rates():
    assert (Hatchback().get_below_week_rate(), Hatchback().get_week_or_more_rate(), Hatchback().get_vip_rate()) == (30, 25, 20)
    assert (Sedan().get_below_week_rate(), Sedan().get_week_or_more_rate(), Sedan().get_vip_rate()) == (50, 40, 35)
    assert (SUV().get_below_week_rate(), SUV().get_week_or_more_rate(), SUV().get_vip_rate()) == (100, 90, 80)


# Section 2.1.2: the VIP subclass overrides is_vip.
def test_s212_vip_overrides_is_vip():
    assert Customer("Ann").is_vip() is False
    assert VIP("Ann(VIP)").is_vip() is True


# A.2.1 Rent a Car: rental under a week uses the below-week daily rate.
def test_a21_rent_a_car_below_week_rate(scripted, capsys):
    shop, client = scripted(["Ann", "1", "hatchback", "3", "", "5"])
    assert client.get_car_details()["type"] == "Hatchback"
    assert client.get_car_details()["days rented"] == 3
    assert "charged £30 per day" in capsys.readouterr().out


# A.2.1 Rent a Car: rental of a week or more uses the weekly daily rate.
def test_a21_rent_a_car_week_or_more_rate(scripted, capsys):
    shop, client = scripted(["Ann", "1", "sedan", "7", "", "5"])
    assert client.is_renting_a_car()
    assert "charged £40 per day" in capsys.readouterr().out


# A.2.2 View Available Cars: show the count per type and the total.
def test_a22_view_available_cars_shows_counts_and_total(scripted, capsys):
    scripted(["Ann", "2", "", "5"])
    out = capsys.readouterr().out
    assert "| Hatchback: 4 | Sedan: 3 | SUV: 3 |" in out
    assert "Total: 10" in out


# A.2.2 View Available Cars: the view reflects a rental.
def test_a22_view_available_cars_after_rental(scripted, capsys):
    shop, _ = scripted(["Ann", "1", "suv", "2", "", "2", "", "5"])
    out = capsys.readouterr().out
    assert "| Hatchback: 4 | Sedan: 3 | SUV: 2 |" in out
    assert "Total: 9" in out


# A.2.3 Return a Car: the returned car goes back into stock.
def test_a23_return_a_car_updates_stock(scripted):
    shop, client = scripted(["Ann", "1", "suv", "2", "", "3", "", "5"])
    assert stock_counts(shop) == INITIAL
    assert not client.is_renting_a_car()


# A.2.3 Return a Car: the bill equals the daily rate times the days rented.
def test_a23_return_a_car_displays_bill(scripted, capsys):
    scripted(["Ann", "1", "suv", "8", "", "3", "", "5"])
    out = capsys.readouterr().out
    assert "Your daily rate is £90." in out
    assert "Amount to pay: £720" in out


# A.2.4 Exit Platform: option 5 closes the shop and ends the loop.
def test_a24_exit_platform_gracefully(scripted, capsys):
    shop, _ = scripted(["Ann", "5"])
    assert shop.is_currently_open() is False
    assert "Thank you for stopping by!" in capsys.readouterr().out


# A.2.5 Loyalty Programme Discount: joining gives the VIP rate.
def test_a25_loyalty_join_gives_discounted_rate(scripted, capsys):
    shop, client = scripted(["Ann", "4", "y", "", "1", "hatchback", "3", "", "3", "", "5"])
    out = capsys.readouterr().out
    assert client.is_vip()
    assert client.get_customer_name() == "Ann(VIP)"
    assert "Ann(VIP)" in shop.vip_customers
    assert "Amount to pay: £60" in out


# A.2.5 Loyalty Programme Discount: leaving restores regular rates.
def test_a25_loyalty_leave_restores_regular_rate(scripted, capsys):
    shop, client = scripted(["Ann", "4", "y", "", "4", "y", "", "1", "hatchback", "3", "", "5"])
    assert not client.is_vip()
    assert client.get_customer_name() == "Ann"
    assert "Ann(VIP)" not in shop.vip_customers
    assert "charged £30 per day" in capsys.readouterr().out


# A.2.5 and section 2.1.3: upgrade and downgrade keep the current rental.
def test_a25_loyalty_change_keeps_rented_car(shop):
    client = Customer("Ann")
    car = shop.handout_car("Sedan")
    client.rent_car(car, "Sedan", 4)
    vip = shop.upgrade_customer(client)
    assert vip.get_car_details()["car"] is car
    regular = shop.downgrade_vip_customer(vip)
    assert regular.get_car_details() == {"car": car, "type": "Sedan", "days rented": 4}


# A.3.1 Usability: an invalid option gives a clear message and the menu stays open.
def test_a31_usability_invalid_option_message(scripted, capsys):
    shop, _ = scripted(["Ann", "9", "abc", "2", "", "5"])
    out = capsys.readouterr().out
    assert "Invalid option" in out
    assert "You should enter a number" in out


# A.3.2 Performance: rent, view and return each finish within 10 seconds, pauses included.
def test_a32_performance_operations_under_10_seconds():
    answers = iter(["Ann", "1", "hatchback", "3", "", "2", "", "3", "", "5"])
    start = time.perf_counter()
    main.run(input_func=lambda prompt="": next(answers), delay=0.01)
    assert time.perf_counter() - start < 10
    # The default pause is 4 steps of 0.5 s, so each screen stays well under 10 s.
    assert main.DEFAULT_DELAY * 4 * 3 < 10


# A.3.3 Reliability: stock stays consistent across many rent and return cycles.
def test_a33_reliability_stock_consistency(shop):
    for _ in range(25):
        for car_type in INITIAL:
            client = Customer("Ann")
            client.rent_car(shop.handout_car(car_type), car_type, 2)
            details = client.return_car()
            assert shop.is_returnable(details["type"], details["car"])
    assert stock_counts(shop) == INITIAL
    every_car = [car for cars in shop.rental_shop_stock.values() for car in cars]
    assert len({id(car) for car in every_car}) == 10


# A.4.2 Constraint: in-memory storage only, so a new shop starts from the same stock.
def test_a42_in_memory_storage_resets_per_session(scripted):
    scripted(["Ann", "1", "suv", "2", "", "5"])
    assert stock_counts(main.build_shop()) == INITIAL


# B.4.1 No Car (Type) Available: an empty or unknown type gives the message.
def test_b41_no_car_type_available(capsys):
    shop = main.build_shop()
    shop.rental_shop_stock["SUV"].clear()
    feed = iter(["Ann", "1", "suv", "", "1", "truck", "", "5"])
    client = main.run(input_func=lambda prompt="": next(feed), delay=0, shop=shop)
    out = capsys.readouterr().out
    assert "Unfortunately no SUV is available." in out
    assert "Unfortunately no Truck is available." in out
    assert not client.is_renting_a_car()


# B.4.3 No Car to Return: returning without a rental gives the message and leaves stock alone.
def test_b43_no_car_to_return(scripted, capsys):
    shop, _ = scripted(["Ann", "3", "", "5"])
    assert "you have no car to return" in capsys.readouterr().out
    assert stock_counts(shop) == INITIAL


# B.4.4 Rent One Car per Customer: a second rental is refused.
def test_b44_rent_one_car_per_customer(scripted, capsys):
    shop, client = scripted(["Ann", "1", "sedan", "2", "", "1", "", "5"])
    assert "we only rent one car per customer" in capsys.readouterr().out
    assert stock_counts(shop)["Sedan"] == 2
    assert client.get_car_details()["type"] == "Sedan"


# Section 4.3 known issue: the bill uses the customer status at return time (MVP behaviour).
def test_s43_known_issue_bill_uses_status_at_return(scripted, capsys):
    scripted(["Ann", "1", "hatchback", "3", "", "4", "y", "", "3", "", "5"])
    assert "Amount to pay: £60" in capsys.readouterr().out
