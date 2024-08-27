from neo4j import GraphDatabase, ManagedTransaction

URI = "bolt://localhost:7687"
DRIVER = GraphDatabase.driver(URI, auth=("neo4j", "password"))


def add_friend(tx: ManagedTransaction, name: str, friend_name: str) -> None:
    tx.run(
        "CREATE (a:Person {name: $name})-[:FRIEND]->(b:Person {name: $friend_name})",
        name=name,
        friend_name=friend_name,
    )


def main() -> None:
    with DRIVER.session() as session:
        session.write_transaction(add_friend, "Alice", "Bob")

    with DRIVER.session() as session:
        result = session.run(
            "MATCH (a:Person)-[:FRIEND]->(b:Person) RETURN a.name, b.name"
        )
        for record in result:
            print(f"{record['a.name']} is friends with {record['b.name']}")

    DRIVER.close()


if __name__ == "__main__":
    main()
