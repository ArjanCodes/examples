def process_data(data):
    return data.lower()  # Assumes data is a string


print(process_data("Hello"))  # Works
print(process_data(123))  # Runtime error
