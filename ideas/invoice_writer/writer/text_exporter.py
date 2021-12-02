from writer.invoice import Invoice


class TextExporter:
    def export(self, invoice: Invoice):
        total = 0
        print("Invoice for:")
        print(invoice.customer.name)
        print(invoice.customer.address)
        print(invoice.customer.phone)
        print(invoice.customer.email)
        print(f"\nPrinted on {invoice.date}")
        print("-" * 50)
        print("{:<20}{:>10}{:>10}{:>10}".format("Item", "Price", "Qty", "Total"))
        print("-" * 50)
        for item in invoice.items:
            subtotal = item.subtotal()
            total += subtotal
            print(
                f"{item.description:<20}{item.price/100:>10.2f}{item.quantity:>10}{subtotal/100:>10.2f}"
            )
        print("-" * 50)
        print(
            "{:<20}{:>10}{:>10}{:>10.2f}".format("Total", "", "", invoice.total() / 100)
        )
        print(
            "{:<20}{:>10}{:>10}{:>10.2f}".format(
                "VAT", "", "", invoice.total_vat() / 100
            )
        )
        print("=" * 50)
