from pos.customer import Customer
from pos.line_item import LineItem
from pos.order import Order
from pos.payment import StripePaymentProcessor
from pos.system import POSSystem


def main() -> None:
    # create the POS system and setup the payment processor
    payment_processor = StripePaymentProcessor.create("https://api.stripe.com/v2")
    system = POSSystem(payment_processor)

    # create the customer
    customer = Customer(
        id=12345,
        name="Arjan",
        address="Sesame street 104",
        postal_code="1234",
        city="Amsterdam",
        email="hi@arjancodes.com",
    )

    # create the order
    order = Order(customer)
    order.add_line_item(LineItem("Keyboard", 1, 5000))
    order.add_line_item(LineItem("SSD", 1, 15000))
    order.add_line_item(LineItem("USB cable", 2, 500))

    # register the order in the POS system
    system.register_order(order)

    # process the order
    system.process_order(order)


if __name__ == "__main__":
    main()
