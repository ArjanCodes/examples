- You can talk to a database using raw SQL queries, you can use something a bit more advanced such as a SQL query builder, or you can use an ORM, which completely abstracts away the database communication.
- Each one of these approaches has its pros and cons. If you don’t know about them, you risk picking the wrong technology for your project and unfortunately it’s a huge pain to switch later on.
- I want to help you avoid that by comparing these 3 options today and show you a few practical examples. So you can make a more informed decision about which option fits best for your project.
- I do have a personal favorite though…
- Before we start, if you want to become better at reviewing code and detecting problems much sooner, I have a free workshop on Code Diagnosis. You can join by going to arjan.codes/diagnosis. In this workshop I teach you a 3-factor framework and show you how to apply it to actual production code. It’s about half an hour, very simple and to the point. Just go to arjan.codes/diagnosis to join - I’ve also put the link in the description.

## Definitions

- Let’s first cover the main options.

### raw SQL

- A SQL query is defined as either a pure string or a `.sql` file that is read as a string. It is sent purely to some database connection in order to be interpreted and executed.

### ORM

- ORM = Object Relational Mapping
- It’s a layer that connects object-oriented programming (OOP) to relational databases, where tables are represented as classes, fields as their attributes or properties and query statement

### SQL query builder

- packages or interfaces to encapsulate the SQL queries construction. It produces the SQL command without the need of writing it manually like raw SQL.

## Going deep

### raw SQL

- It’s the most flexible way compared with the two others.
- Writing raw SQL queries enforces you to learn SQL language.
- Small queries are easily parametrized using f-strings, but it’s prone to SQL injection attacks (here you can explain it briefly):
  - SQL injection attack is a web security vulnerability that allows an attacker to interfere with the queries that an application makes to its database.
  - A hacker could simply introduce other SQL statements or change the actual to retrieve valuable and confidential data or deleted it inadvertently.
- As the size of queries grows, constructing them manually can be cumbersome. And also keeping them as a pure strings in Python becomes hard to maintain.
- It’s possible to create `.sql` files to better organize the project. But parametrizing them becomes more complex.
- It’s possible to parametrize `.sql` files we can use Jinja templates, but it doesn’t solve the prone of SQL injection attacks problem.

### ORM

- The logic behind ORM is being able to write queries and manipulate data using an object-oriented paradigm. Tables are represented as classes, fields as their attributes or properties and query statements are translated into methods.
- It might save a lot of time for whom don’t write in SQL much. On the other hand, doesn’t enforces you to learn SQL language (and keeps you in your comfort zone, maybe?)
- For those who know more SQL than OOP, ORM can be time-consuming to learn at the beginning, especially about the ORM configuration.
- There is a lack of flexibility because ORM is available in Python frameworks, and they might not have the methods you need to build your SQL operations within their classes, or if they have, it could be complex to do it. Examples are window functions in SQL language.
- ORM brings the advantage of extra protection against SQL injection attacks. The protection layer is hidden under the hoods inside the frameworks.
- It may handle the floating point programming issue depending on the framework.
- ORM varies slightly depending on the framework used, and it could be hard to change it. Below are some ORM Python frameworks examples:
  - **The Django ORM:** built into the Django web framework. This ORM is tightly integrated with the rest of the Django framework, making it easy to use for developers who are already familiar with Django.
  - **SQLAlchemy:** a toolkit, including ORM, that provides a set of high-level APIs to interact with databases. It provides a flexible and powerful way to interact with databases, while still giving developers access to the full power of SQL. It is a popular choice among Python developers due to its scalability, flexible API, and large community.
  - **Peewee:** simple and expressive ORM for Python that is built on top of SQLite, MySQL, and PostgreSQL. It provides a high-level, Pythonic API for interacting with databases, and is designed to be easy to use and maintain. It’s also well-suited for small to medium-sized projects, but may not be the best choice for larger and more complex projects.
  - **PonyORM:** provides a high-level, Pythonic API for interacting with databases. It supports SQLite, MySQL, and PostgreSQL, and provides features for performance optimization and connection pooling. Easy to use with a simple and intuitive API.
  - **SQLObject:** another simple ORM for Python. However, it has not been actively developed for several years and may not be the best choice for new projects.
- For data science projects, especially in the experimentation phase, ORM is unfeasible, as columns (features) are created and removed in the process in order to get the best model. This would require changing the code in order to attend to the data fields.

### SQL query builder

- The middle point between flexibility and security.
- It avoids SQL injection attacks and keeps flexibility and control over the SQL query, as it’s not encapsulated.
- Keeps the flexibility of writing raw SQL files together with parametrization on code and the security layer of ORM.
- It’s possible to customize functions to build complex queries that are either hard or impossible to build in ORM
- It does not handle floating points as ORM does

## Code example

- The ORM for code examples SQLAlchemy was chosen. Here are the two main reasons:
  - SQLAlchemy is the most flexible one, with a large community behind it. It’s well documented, so it's easy to find and learn new topics (remember that ORM is all about learning the new toolkit?)
  - Django ORM is recommended to be used together with Django, and here is not the case.
  - Peewee and PonyORM are great for starting projects, but they are not as scalable as SQLAlchemy.
  - SQLObject is no longer maintained.
- ********\*\*\*\*********Database:********\*\*\*\********* there is an `orm\database\sample_database.db` that is used in all code examples. It is the sample present in DBeaver Community Edition that can be downloaded for free. It was built in SQLite
- Query: the same query command was used in all examples:

```sql
-- What are the top 10 profitable customers at the company?
SELECT
	c.CustomerId,
	c.FirstName,
	SUM(i.Total) AS Total
FROM Invoice i
LEFT JOIN Customer c ON i.CustomerId = c.CustomerId
GROUP BY c.CustomerId, c.FirstName
ORDER BY TOTAL DESC
LIMIT 10;
```

- `**raw_sql.py` →\*\* the SQL is used directly as an f-string, parametrized (SQL injection attack) and sent to SQLite to be executed.
- `**raw_sql_file.py` →\*\* the SQL was read from a file, parametrized with Jinja2 and sent to SQLite to be executed.
- `**orm.py**` → the model was built using SQLAlchemy (reasons above) and all the available methods were used to retrieve the same information.
- `**sql_query_builder.py` →\*\* I’ve used pypika to build the SQL query. It is sent to SQLite afterwards just like the `raw_sql.py`
- **Comments:**
  - Notice that only the ORM version using SQLAlchemy could handle the floating point bringing the result as a `Decimal` instead of a common `float` and its programming issues. This was set at the class definition, where it’s possible to define `Numeric(10,2)` with both precision and scale.

## Final thoughts

- Just using raw SQL is the most flexible but there are inconveniences such as that constructing the queries is more cumbersome (especially if you need to do that dynamically based on what a user does in a GUI) and there’s the risk of injection attacks if you’re not careful
- ORMs are nice but you will lose some of the flexibility of SQL. Also, each ORM is slightly different so it’s not as general as SQL. And some ORMs will deal differently with object relationships and how they’re modeled in the database. That might lead to problem with migrations if you ever need to switch
- A SQL query builder is a nice in between solution that avoid injection attacks, but still gives you quite a bit of control over how you interact with the database.
