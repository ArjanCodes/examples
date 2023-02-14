import sqlite3

from pypika import Order, Query, Table, functions

invoice = Table("Invoice")
customer = Table("Customer")
query = (
    Query.from_(invoice)
    .left_join(customer)
    .on(invoice.CustomerId == customer.CustomerId)
    .groupby(customer.CustomerId, customer.FirstName)
    .orderby(functions.Sum(invoice.Total), order=Order.desc)
    .limit(10)
    .select(
        customer.CustomerId,
        customer.FirstName,
        functions.Sum(invoice.Total).as_("Total"),
    )
)

con = sqlite3.connect(r"orm\database\sample_database.db")

cur = con.cursor()

sql = query.get_sql()

for row in cur.execute(sql):
    print(row)
