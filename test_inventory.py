"""Comprehensive Unit Tests for Product Inventory Management System.

Tests calculate_total_price, apply_discount, and check_stock using pytest.
Covers standard scenarios, boundary conditions, invalid values, and type restrictions.
"""

import pytest
from inventory import apply_discount, calculate_total_price, check_stock


# ==============================================================================
# 1. Tests for calculate_total_price(price, quantity)
# ==============================================================================


def test_calculate_total_price_normal():
    """Test standard valid calculations."""
    assert calculate_total_price(100.0, 5) == 500.0
    assert calculate_total_price(49.99, 2) == 99.98
    assert calculate_total_price(10, 10) == 100.0


def test_calculate_total_price_zero_quantity():
    """Test boundary: zero quantity produces zero total."""
    assert calculate_total_price(500.0, 0) == 0.0


def test_calculate_total_price_zero_price():
    """Test boundary: zero price produces zero total."""
    assert calculate_total_price(0.0, 10) == 0.0


def test_calculate_total_price_zero_both():
    """Test boundary: zero price and zero quantity."""
    assert calculate_total_price(0, 0) == 0.0


@pytest.mark.parametrize(
    "price, quantity",
    [
        (-1.0, 5),
        (-500, 2),
        (-0.01, 1),
    ],
)
def test_calculate_total_price_negative_price(price, quantity):
    """Test that negative price raises ValueError."""
    with pytest.raises(ValueError, match="Price cannot be negative"):
        calculate_total_price(price, quantity)


@pytest.mark.parametrize(
    "price, quantity",
    [
        (100.0, -1),
        (50.0, -10),
    ],
)
def test_calculate_total_price_negative_quantity(price, quantity):
    """Test that negative quantity raises ValueError."""
    with pytest.raises(ValueError, match="Quantity cannot be negative"):
        calculate_total_price(price, quantity)


@pytest.mark.parametrize(
    "price, quantity",
    [
        ("100", 5),
        (None, 5),
        ([100], 5),
        (True, 5),  # Booleans must be rejected
        (False, 5),
    ],
)
def test_calculate_total_price_invalid_price_type(price, quantity):
    """Test that non-numeric or boolean price raises TypeError."""
    with pytest.raises(TypeError):
        calculate_total_price(price, quantity)


@pytest.mark.parametrize(
    "price, quantity",
    [
        (100.0, "5"),
        (100.0, 2.5),  # Fractional quantity must be rejected
        (100.0, None),
        (100.0, True),  # Booleans must be rejected
        (100.0, False),
    ],
)
def test_calculate_total_price_invalid_quantity_type(price, quantity):
    """Test that non-integer or boolean quantity raises TypeError."""
    with pytest.raises(TypeError):
        calculate_total_price(price, quantity)


# ==============================================================================
# 2. Tests for apply_discount(total, discount_percent)
# ==============================================================================


def test_apply_discount_normal():
    """Test normal discount calculations."""
    # 10% off 100 is 90
    assert apply_discount(100.0, 10.0) == 90.0
    # 25% off 200 is 150
    assert apply_discount(200.0, 25.0) == 150.0


def test_apply_discount_zero_discount():
    """Test boundary: 0% discount retains full total."""
    assert apply_discount(750.0, 0.0) == 750.0


def test_apply_discount_full_discount():
    """Test boundary: 100% discount results in zero total."""
    assert apply_discount(750.0, 100.0) == 0.0


def test_apply_discount_zero_total():
    """Test boundary: 0 total returns 0 regardless of discount."""
    assert apply_discount(0.0, 20.0) == 0.0


@pytest.mark.parametrize(
    "total, discount_percent",
    [
        (100.0, 100.1),
        (100.0, 150.0),
        (500.0, 200),
    ],
)
def test_apply_discount_greater_than_100(total, discount_percent):
    """Test that discount percent > 100 raises ValueError."""
    with pytest.raises(
        ValueError, match="Discount percentage must be between 0 and 100"
    ):
        apply_discount(total, discount_percent)


@pytest.mark.parametrize(
    "total, discount_percent",
    [
        (100.0, -0.1),
        (100.0, -10.0),
    ],
)
def test_apply_discount_negative_discount(total, discount_percent):
    """Test that negative discount percent raises ValueError."""
    with pytest.raises(
        ValueError, match="Discount percentage must be between 0 and 100"
    ):
        apply_discount(total, discount_percent)


def test_apply_discount_negative_total():
    """Test that negative total raises ValueError."""
    with pytest.raises(ValueError, match="Total cannot be negative"):
        apply_discount(-100.0, 10.0)


@pytest.mark.parametrize(
    "total, discount_percent",
    [
        ("100", 10.0),
        (100.0, "10"),
        (None, 10.0),
        (100.0, None),
        (True, 10.0),
        (100.0, False),
    ],
)
def test_apply_discount_invalid_types(total, discount_percent):
    """Test that non-numeric or boolean values raise TypeError."""
    with pytest.raises(TypeError):
        apply_discount(total, discount_percent)


# ==============================================================================
# 3. Tests for check_stock(available_stock, requested_quantity)
# ==============================================================================


def test_check_stock_available():
    """Test case when available stock is greater than requested quantity."""
    assert check_stock(10, 5) is True


def test_check_stock_exact_quantity():
    """Test case when available stock exactly equals requested quantity."""
    assert check_stock(5, 5) is True


def test_check_stock_insufficient_stock():
    """Test case when requested quantity exceeds available stock."""
    assert check_stock(3, 10) is False
    assert check_stock(0, 1) is False


def test_check_stock_zero_requested():
    """Test case when requested quantity is zero (always fulfillable)."""
    assert check_stock(5, 0) is True
    assert check_stock(0, 0) is True


@pytest.mark.parametrize(
    "stock, requested",
    [
        (-1, 5),
        (-10, 0),
    ],
)
def test_check_stock_negative_stock(stock, requested):
    """Test that negative available stock raises ValueError."""
    with pytest.raises(ValueError, match="Stock quantities cannot be negative"):
        check_stock(stock, requested)


@pytest.mark.parametrize(
    "stock, requested",
    [
        (10, -1),
        (5, -5),
    ],
)
def test_check_stock_negative_requested(stock, requested):
    """Test that negative requested quantity raises ValueError."""
    with pytest.raises(ValueError, match="Stock quantities cannot be negative"):
        check_stock(stock, requested)


@pytest.mark.parametrize(
    "stock, requested",
    [
        (10.5, 5),  # Stock must be integer
        (10, 5.5),  # Requested must be integer
        ("10", 5),
        (10, "5"),
        (None, 5),
        (10, None),
        (True, 5),  # Reject booleans
        (10, False),
    ],
)
def test_check_stock_invalid_types(stock, requested):
    """Test that non-integer or boolean values raise TypeError."""
    with pytest.raises(TypeError):
        check_stock(stock, requested)
