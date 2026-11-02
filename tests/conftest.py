"""Shared test fixtures for RentalOOP."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import main  # noqa: E402
from rental_shops import RentalShop  # noqa: E402


@pytest.fixture
def shop():
    """Return the shop that main.py builds: RentACar with 4, 3 and 3 cars."""
    return main.build_shop()


@pytest.fixture
def empty_shop():
    """Return a shop with no stock."""
    return RentalShop("EmptyShop")


@pytest.fixture
def scripted():
    """Return a factory that runs the CLI with scripted answers and no pauses."""

    def _run(answers):
        feed = iter(answers)

        def fake_input(prompt=""):
            print(prompt, end="")  # Echo the prompt, as a terminal does.
            return next(feed)

        shop = main.build_shop()
        client = main.run(input_func=fake_input, delay=0, shop=shop)
        return shop, client

    return _run
