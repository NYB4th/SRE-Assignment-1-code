from typing import List, Dict, Any

# Named Constants for Discounts and Delivery Fees (PKR)
DISCOUNT_RATES: Dict[str, float] = {
    "student": 0.10,
    "staff": 0.05,
}

DELIVERY_FEES: Dict[str, float] = {
    "express": 250.0,
    "standard": 100.0,
}


def validate_items(items: List[Dict[str, Any]]) -> None:

    # Corrective fix: a negative price or quantity raises ValueError
    # instead of silently lowering the total
    for item in items:
        if item["qty"] < 0:
            raise ValueError(f"Quantity cannot be negative for item '{item['name']}'.")
        if item["price"] < 0:
            raise ValueError(f"Price cannot be negative for item '{item['name']}'.")


def calculate_subtotal(items: List[Dict[str, Any]]) -> float:

    # Calculate the sum total of all items before discounts or shipping
    subtotal = 0.0
    for item in items:
        subtotal += item["price"] * item["qty"]
    return subtotal


def calculate_discount(subtotal: float, customer_type: str) -> float:

    # Calculate the discount amount based on customer type.
    rate = DISCOUNT_RATES.get(customer_type, 0.0)
    return subtotal * rate


def calculate_delivery_fee(delivery: str) -> float:

    # Determine delivery fee based on selected delivery method
    return DELIVERY_FEES.get(delivery, 0.0)


def order_total(
    items: List[Dict[str, Any]], customer_type: str, delivery: str
) -> float:
    # Calculate the final order total including discounts and delivery charges
    validate_items(items)
    subtotal = calculate_subtotal(items)
    discount = calculate_discount(subtotal, customer_type)
    delivery_fee = calculate_delivery_fee(delivery)

    total = (subtotal - discount) + delivery_fee
    return round(total, 2)


def print_receipt(
    items: List[Dict[str, Any]], customer_type: str, delivery: str
) -> str:

    # Format and generate a printable order receipt string
    amount = order_total(items, customer_type, delivery)

    receipt_lines = ["ORDER RECEIPT"]
    for item in items:
        item_total = item["price"] * item["qty"]
        receipt_lines.append(f"{item['qty']} x {item['name']} = {item_total}")

    receipt_lines.append(f"Customer: {customer_type}")
    receipt_lines.append(f"Delivery: {delivery}")
    receipt_lines.append(f"Total: {amount}")

    return "\n".join(receipt_lines)


if __name__ == "__main__":
    sample = [
        {"name": "Notebook", "category": "book", "price": 300, "qty": 2},
        {"name": "USB Drive", "category": "electronics", "price": 800, "qty": 1},
    ]
    print(print_receipt(sample, "student", "standard"))
