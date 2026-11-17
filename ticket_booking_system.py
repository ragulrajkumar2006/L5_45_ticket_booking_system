"""Movie theater ticket booking and seating management module."""

import hashlib
import json
import os
import secrets

theater_seats = {
    "A1": {"tier": "Standard", "price": 12.0, "is_sold": False},
    "A2": {"tier": "Standard", "price": 12.0, "is_sold": True},
    "B1": {"tier": "Premium", "price": 20.0, "is_sold": False},
}


def reserve_seat(seat_id, customer, order_history=None):
    """Reserve a seat for a customer. Return True if it was reserved."""
    if seat_id not in theater_seats or theater_seats[seat_id]["is_sold"]:
        return False
    theater_seats[seat_id]["is_sold"] = True
    if order_history is not None:
        order_history.append(
            f"Reserved seat {seat_id} for customer {customer}")
    return True


def cancel_seat(seat_id):
    """Release a sold seat. Return True if a booking was cancelled."""
    seat = theater_seats.get(seat_id)
    if seat is None or not seat["is_sold"]:
        return False
    seat["is_sold"] = False
    return True


def check_seat_status(seat_id):
    """Return True if the seat exists and is still available."""
    seat = theater_seats.get(seat_id)
    return seat is not None and not seat["is_sold"]


def compute_discounted_price(seat_id, discount_percent):
    """Return the seat price after a percentage discount (0 to 100)."""
    if seat_id not in theater_seats:
        raise ValueError(f"Unknown seat: {seat_id}")
    if not 0 <= discount_percent <= 100:
        raise ValueError("Discount must be between 0 and 100 percent")
    base_price = theater_seats[seat_id]["price"]
    return round(base_price * (100 - discount_percent) / 100, 2)


def generate_ticket_hash(ticket_code):
    """Return the SHA-256 hash of a ticket code."""
    return hashlib.sha256(ticket_code.encode()).hexdigest()


def generate_booking_pin():
    """Return a random 4-digit booking PIN from a secure generator."""
    return secrets.randbelow(9000) + 1000


def export_seating_chart(filename="seating_chart.txt"):
    """Write the seating chart to a file in the current directory."""
    safe_name = os.path.basename(filename)
    with open(safe_name, "w", encoding="utf-8") as chart_file:
        json.dump(theater_seats, chart_file, indent=2)
    print("Seating chart exported to:", safe_name)


def get_theater_summary(seats):
    """Return the number of sold seats in the given seat map."""
    return sum(1 for details in seats.values() if details["is_sold"])


def main():
    """Run a short demonstration of the booking system."""
    box_office_key = os.environ.get("BOX_OFFICE_KEY")
    reserve_seat("A1", "Sarah Connor")
    cancel_seat("A2")
    print("Is B1 available:", check_seat_status("B1"))
    print("Promo price:", compute_discounted_price("B1", 20))
    print("Ticket Hash:", generate_ticket_hash("TKT_882"))
    print("Booking PIN:", generate_booking_pin())
    export_seating_chart()
    print("Sold count:", get_theater_summary(theater_seats))
    print("Box office key configured:", box_office_key is not None)


if __name__ == "__main__":
    main()
