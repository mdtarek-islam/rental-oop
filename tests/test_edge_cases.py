"""Edge cases: out of stock, invalid input and bill calculation."""
import pytest

import main
from cars import SUV, Hatchback, Sedan
from customer import VIP, Customer


# Out of stock.
def test_is_available_false_when_type_sold_out(shop):
    for _ in range(3):
        shop.handout_car("SUV")
    assert shop.is_available("SUV") is False
    assert shop.is_available("Sedan") is True


def test_is_available_false_for_unknown_type(shop):
    assert shop.is_available("Truck") is False


def test_handout_car_from_empty_stock_raises(empty_shop):
    with pytest.raises(ValueError):
        empty_shop.handout_car("Hatchback")


def test_add_to_stock_creates_distinct_car_objects(empty_shop):
    empty_shop.add_to_stock("Sedan", 3)
    cars = empty_shop.rental_shop_stock["Sedan"]
    assert len({id(car) for car in cars}) == 3
    assert all(isinstance(car, Sedan) for car in cars)


def test_add_to_stock_rejects_unknown_type(empty_shop):
    with pytest.raises(KeyError):
        empty_shop.add_to_stock("Truck", 1)


# Returns.
def test_is_returnable_rejects_no_car(shop):
    assert shop.is_returnable(None, None) is False


def test_is_returnable_rejects_mismatched_type(shop):
    assert shop.is_returnable("Hatchback", SUV()) is False
    assert len(shop.rental_shop_stock["Hatchback"]) == 4


def test_return_car_empties_garage():
    client = Customer("Ann")
    car = Hatchback()
    client.rent_car(car, "Hatchback", 2)
    details = client.return_car()
    assert details == {"car": car, "type": "Hatchback", "days rented": 2}
    assert client.get_car_details() == {"car": None, "type": None, "days rented": 0}


def test_upgrade_does_not_share_details_dict(shop):
    client = Customer("Ann")
    vip = shop.upgrade_customer(client)
    assert vip.get_car_details() is not client.get_car_details()


def test_downgrade_removes_only_the_vip_suffix(shop):
    vip = shop.upgrade_customer(Customer("Bob(VIP)x"))
    regular = shop.downgrade_vip_customer(vip)
    assert regular.get_customer_name() == "Bob(VIP)x"
    assert isinstance(vip, VIP)


# Invalid input.
def test_parse_car_type_normalises_case():
    assert main.parse_car_type("  hatchBACK ") == "Hatchback"
    assert main.parse_car_type("suv") == "SUV"
    assert main.parse_car_type("SEDAN") == "Sedan"


def test_expected_int_reprompts_until_number():
    feed = iter(["two", "2"])
    assert main.expected_int("x", input_func=lambda prompt="": next(feed)) == 2


def test_rental_days_must_be_positive(scripted, capsys):
    shop, client = scripted(["Ann", "1", "sedan", "0", "-4", "many", "5", "", "5"])
    out = capsys.readouterr().out
    assert "greater than zero" in out
    assert client.get_car_details()["days rented"] == 5


def test_loyalty_prompt_declined_keeps_status(scripted):
    _, client = scripted(["Ann", "4", "n", "5"])
    assert not client.is_vip()


# Bill calculation.
@pytest.mark.parametrize(
    "car, days, is_vip, rate, price",
    [
        (Hatchback(), 6, False, 30, 180),
        (Hatchback(), 7, False, 25, 175),
        (Sedan(), 1, False, 50, 50),
        (Sedan(), 10, False, 40, 400),
        (SUV(), 6, False, 100, 600),
        (SUV(), 14, False, 90, 1260),
        (Hatchback(), 3, True, 20, 60),
        (Sedan(), 9, True, 35, 315),
        (SUV(), 1, True, 80, 80),
    ],
)
def test_bill_calculation(shop, car, days, is_vip, rate, price):
    assert shop.get_rate(car, days, is_vip) == rate
    assert shop.get_price(rate, days) == price


def test_main_module_import_has_no_side_effects(capsys):
    import importlib

    importlib.reload(main)
    assert capsys.readouterr().out == ""
