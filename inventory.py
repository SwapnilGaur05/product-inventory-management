"""Product Inventory Management System.

Demonstrates functions, input validation, exception handling,
logging, and inventory business operations.
"""

import logging
import os

# Configure application logging to application.log
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "application.log")

logging.basicConfig(
    filename=LOG_FILE,
    filemode="w",
    level=logging.DEBUG,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger("InventorySystem")


def calculate_total_price(price: float, quantity: int) -> float:
    """Calculate the total price of a product order.

    Formula:
        total = price * quantity

    Validation:
        - Price must be numeric (int or float).
        - Price cannot be negative.
        - Quantity must be an integer.
        - Quantity cannot be negative.
        - Zero quantity is valid (represents a zero-quantity line item).
        - Explicitly rejects booleans (since in Python, bool is a subclass of int).

    Args:
        price (float | int): Unit price of the product.
        quantity (int): Number of units requested.

    Returns:
        float: Calculated total price rounded to 2 decimal places.

    Raises:
        TypeError: If price or quantity is a boolean or not of expected type.
        ValueError: If price or quantity is negative.
    """
    logger.debug(
        "calculate_total_price called with price=%r, quantity=%r", price, quantity
    )

    if isinstance(price, bool) or isinstance(quantity, bool):
        err_msg = "Price and quantity must not be boolean values."
        logger.error("TypeError in calculate_total_price: %s", err_msg)
        raise TypeError(err_msg)

    if not isinstance(price, (int, float)):
        err_msg = f"Price must be a numeric value, got {type(price).__name__}."
        logger.error("TypeError in calculate_total_price: %s", err_msg)
        raise TypeError(err_msg)

    if not isinstance(quantity, int):
        err_msg = f"Quantity must be an integer, got {type(quantity).__name__}."
        logger.error("TypeError in calculate_total_price: %s", err_msg)
        raise TypeError(err_msg)

    if price < 0:
        err_msg = f"Price cannot be negative, got {price}."
        logger.error("ValueError in calculate_total_price: %s", err_msg)
        raise ValueError(err_msg)

    if quantity < 0:
        err_msg = f"Quantity cannot be negative, got {quantity}."
        logger.error("ValueError in calculate_total_price: %s", err_msg)
        raise ValueError(err_msg)

    total = round(float(price * quantity), 2)
    logger.info(
        "Total price calculated successfully: Price ₹%.2f × %d = ₹%.2f",
        price,
        quantity,
        total,
    )
    return total


def apply_discount(total: float, discount_percent: float) -> float:
    """Calculate the discounted total price after applying a percentage discount.

    Formula:
        discounted_total = total - (total * discount_percent / 100)

    Validation:
        - Total must be numeric and non-negative.
        - Discount percent must be numeric and between 0 and 100 inclusive.
        - Explicitly rejects booleans.
        - Gracefully handles zero discount (returns full total).
        - Gracefully handles 100% discount (returns 0.0).

    Args:
        total (float | int): Total order amount before discount.
        discount_percent (float | int): Percentage discount to apply (0 to 100).

    Returns:
        float: Discounted total price rounded to 2 decimal places.

    Raises:
        TypeError: If total or discount_percent is a boolean or not numeric.
        ValueError: If total is negative or discount_percent is outside [0, 100].
    """
    logger.debug(
        "apply_discount called with total=%r, discount_percent=%r",
        total,
        discount_percent,
    )

    if isinstance(total, bool) or isinstance(discount_percent, bool):
        err_msg = "Total and discount percentage must not be boolean values."
        logger.error("TypeError in apply_discount: %s", err_msg)
        raise TypeError(err_msg)

    if not isinstance(total, (int, float)):
        err_msg = f"Total must be a numeric value, got {type(total).__name__}."
        logger.error("TypeError in apply_discount: %s", err_msg)
        raise TypeError(err_msg)

    if not isinstance(discount_percent, (int, float)):
        err_msg = f"Discount percentage must be a numeric value, got {type(discount_percent).__name__}."
        logger.error("TypeError in apply_discount: %s", err_msg)
        raise TypeError(err_msg)

    if total < 0:
        err_msg = f"Total cannot be negative, got {total}."
        logger.error("ValueError in apply_discount: %s", err_msg)
        raise ValueError(err_msg)

    if not (0 <= discount_percent <= 100):
        err_msg = f"Discount percentage must be between 0 and 100 inclusive, got {discount_percent}."
        logger.error("ValueError in apply_discount: %s", err_msg)
        raise ValueError(err_msg)

    discount_amount = total * (discount_percent / 100.0)
    discounted_total = round(float(total - discount_amount), 2)
    logger.info(
        "Discount applied successfully: Total ₹%.2f with %.1f%% discount = Final ₹%.2f",
        total,
        discount_percent,
        discounted_total,
    )
    return discounted_total


def check_stock(available_stock: int, requested_quantity: int) -> bool:
    """Determine whether the requested quantity can be fulfilled from available stock.

    Validation:
        - Both available_stock and requested_quantity must be non-negative integers.
        - Explicitly rejects booleans.

    Args:
        available_stock (int): Units of product currently in stock.
        requested_quantity (int): Units of product requested.

    Returns:
        bool: True if available_stock >= requested_quantity, False otherwise.

    Raises:
        TypeError: If either argument is a boolean or not an integer.
        ValueError: If either argument is negative.
    """
    logger.debug(
        "check_stock called with available_stock=%r, requested_quantity=%r",
        available_stock,
        requested_quantity,
    )

    if isinstance(available_stock, bool) or isinstance(requested_quantity, bool):
        err_msg = "Stock values must not be boolean values."
        logger.error("TypeError in check_stock: %s", err_msg)
        raise TypeError(err_msg)

    if not isinstance(available_stock, int):
        err_msg = (
            f"Available stock must be an integer, got {type(available_stock).__name__}."
        )
        logger.error("TypeError in check_stock: %s", err_msg)
        raise TypeError(err_msg)

    if not isinstance(requested_quantity, int):
        err_msg = f"Requested quantity must be an integer, got {type(requested_quantity).__name__}."
        logger.error("TypeError in check_stock: %s", err_msg)
        raise TypeError(err_msg)

    if available_stock < 0 or requested_quantity < 0:
        err_msg = (
            f"Stock quantities cannot be negative: available={available_stock}, "
            f"requested={requested_quantity}."
        )
        logger.error("ValueError in check_stock: %s", err_msg)
        raise ValueError(err_msg)

    is_available = available_stock >= requested_quantity
    if is_available:
        logger.info(
            "Stock check PASSED: Requested %d units available (In stock: %d).",
            requested_quantity,
            available_stock,
        )
    else:
        logger.warning(
            "Stock check FAILED: Requested %d exceeds available stock %d.",
            requested_quantity,
            available_stock,
        )

    return is_available


def run_demonstration():
    """Execute runnable demonstration showing all core requirements and edge cases."""
    print("=" * 60)
    print("        PRODUCT INVENTORY MANAGEMENT SYSTEM")
    print("=" * 60)

    logger.info("Inventory demonstration operation started.")

    # 1. Standard calculation & available stock
    product_name = "Laptop"
    price = 50000.0
    quantity = 2
    discount_pct = 10.0
    stock = 5
    req_qty = 2

    total = calculate_total_price(price, quantity)
    final_price = apply_discount(total, discount_pct)
    in_stock = check_stock(stock, req_qty)

    print(f"\nProduct: {product_name}")
    print(f"Price: ₹{price:.0f}")
    print(f"Quantity: {quantity}")
    print(f"Total Price: ₹{total:.0f}")
    print(f"Discount: {discount_pct:.0f}%")
    print(f"Final Price: ₹{final_price:.0f}")
    print(f"Available Stock: {stock}")
    print(f"Requested Quantity: {req_qty}")
    print(f"Stock Available: {'Yes' if in_stock else 'No'}")

    # 2. Insufficient stock demonstration
    print("\n" + "-" * 60)
    print("DEMO: Stock Unavailable Case")
    stock_p2 = 3
    req_p2 = 10
    print("Product: Smartphone")
    print(f"Available Stock: {stock_p2}")
    print(f"Requested Quantity: {req_p2}")
    stock_avail_p2 = check_stock(stock_p2, req_p2)
    print(f"Stock Available: {'Yes' if stock_avail_p2 else 'No'}")

    # 3. Exception handling demonstration
    print("\n" + "-" * 60)
    print("DEMO: Graceful Input Validation and Exception Handling")

    # Case A: Negative Price
    try:
        print("\n[Test A] Attempting calculate_total_price(-500, 2):")
        calculate_total_price(-500, 2)
    except ValueError as e:
        print(f"  --> Caught expected ValueError: {e}")

    # Case B: Invalid Discount > 100%
    try:
        print("\n[Test B] Attempting apply_discount(1000, 150):")
        apply_discount(1000, 150)
    except ValueError as e:
        print(f"  --> Caught expected ValueError: {e}")

    # Case C: Boolean Passed as Numeric
    try:
        print("\n[Test C] Attempting calculate_total_price(True, 5):")
        calculate_total_price(True, 5)
    except TypeError as e:
        print(f"  --> Caught expected TypeError: {e}")

    print("\n" + "=" * 60)
    print("Demonstration successfully finished.")
    print(f"Audit log generated at: {LOG_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    run_demonstration()
