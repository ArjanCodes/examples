import pickle


def main():
    # Save an object
    my_data = {"name": "Arjan", "age": 30}
    with open("data.pkl", "wb") as file:
        pickle.dump(my_data, file)

    # Load the object back
    with open("data.pkl", "rb") as file:
        loaded_data = pickle.load(file)
    print(loaded_data)


if __name__ == "__main__":
    main()
