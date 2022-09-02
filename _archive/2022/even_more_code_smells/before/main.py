from pos.order import Order
from pos.system import POSSystem


def main() -> None:
    # create the POS system and setup the payment processor
    system = POSSystem()
    system.setup_payment_processor("https://api.stripe.com/v2")

    # create the order
    order = Order(
        12345, "Arjan", "Sesame street 104", "1234", "Amsterdam", "hi@arjancodes.com"
    )
    order.create_line_item("Keyboard", 1, 5000)
    order.create_line_item("SSD", 1, 15000)
    order.create_line_item("USB cable", 2, 500)

    # register and process the order
    system.register_order(order)
    system.process_order(order)


if __name__ == "__main__":
    main()
