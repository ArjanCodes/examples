from pymilvus import Collection, CollectionSchema, DataType, FieldSchema, connections


def main() -> None:
    # Connect to Milvus server
    connections.connect()

    # Define a schema for the collection
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
        FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=128),
    ]
    schema = CollectionSchema(fields, "Vector collection example")

    # Create a collection
    collection = Collection("example_collection", schema)

    # Insert data (random example)
    import numpy as np

    vectors = np.random.random([1000, 128]).astype(np.float32)
    ids = list(range(1000))
    collection.insert([ids, vectors])

    # Query data
    collection.load()
    results = collection.search(
        vectors[:1],
        "vector",
        param={"metric_type": "L2", "params": {"nprobe": 10}},
        limit=3,
    )

    for hit in results[0]:
        print(f"Hit ID: {hit.id}, Distance: {hit.distance}")


if __name__ == "__main__":
    main()
