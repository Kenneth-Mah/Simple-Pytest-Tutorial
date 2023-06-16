# Files starting/ending with "test" will be picked up by pytest

from unittest.mock import Mock
from item_database import ItemDatabase
from shopping_cart import ShoppingCart
import pytest


# https://docs.pytest.org/en/6.2.x/fixture.html#fixtures
# By adding this annotation in front of this function, this function may now be used as an argument in your unit tests
@pytest.fixture
def cart():
    # All setup for the cart here...
    # Note: this fixture is run new for every time you run a unit test (i.e., it returns a new cart every time )
    return ShoppingCart(5) 


# Each function starting with "test" is a unit test

def test_can_add_item_to_cart(cart):
    cart.add("apple")

    # Here, if the statement is true, the test passes. Otherwise, the test fails
    assert cart.size() == 1


def test_when_item_added_then_cart_contains_item(cart):
    cart.add("apple")
    assert "apple" in cart.get_items()


def test_when_add_more_than_max_items_should_fail(cart):
    # Note that for this part of the code, NO error should be thrown
    for _ in range(5):
        cart.add("apple")

    # Here, the OverflowError is expected to be thrown. If that error is thrown, the test passes. If no error/another error is thrown, the test fails
    # Note where this line is written. Here, we are specifically checking that the error is thrown ONLY on the 6th iteration
    with pytest.raises(OverflowError):
        cart.add("apple")

# pytest test_shopping_cart.py                                  -> this tests this specific file
# pytest test_shopping_cart.py::test_can_get_total_price        -> this tests the following specific function
# pytest test_shopping_cart.py::test_can_get_total_price -s     -> this tests the following specific function and shows print statements

def test_can_get_total_price(cart):
    cart.add("apple")
    cart.add("orange")

    # https://docs.python.org/3/library/unittest.mock.html
    # You can mock objects (like DBs) using unittest.mock so that you can test functionality even if the actual object isn't implemented yet

    # In this example, ItemDatabase isn't implemented yet
    item_database = ItemDatabase()

    def mock_get_item(item: str):
        if item == "apple":
            return 1.0
        if item == "orange":
            return 2.0

    # side_effect takes in a function
    # This function takes in whatever the mock receives 
    # The mock will return whatever return value the function returns
    item_database.get = Mock(side_effect=mock_get_item)
    assert cart.get_total_price(item_database) == 3.0
