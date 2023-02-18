import sqlite3

from pypika import Order, Query, Table, functions


def main() -> None:
    invoice = Table("Invoice")
    customer = Table("Customer")
    query = (
        Query.from_(invoice)
        .left_join(customer)
        .on(invoice.customer_id == customer.id)
        .groupby(customer.id, customer.first_name)
        .orderby(functions.Sum(invoice.total), order=Order.desc)
        .limit(10)
        .select(
            customer.id,
            customer.first_name,
            functions.Sum(invoice.total).as_("total"),
        )
    )

    con = sqlite3.connect(r"orm\database\sample_database.db")

    cur = con.cursor()

    sql = query.get_sql()

    for row in cur.execute(sql):
        print(row)


if __name__ == "__main__":
    main()
