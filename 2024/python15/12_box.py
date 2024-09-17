from box import Box


def main():
    nested_data = {
        "is_active": True,
        "user": {
            "name": "Arjan",
            "address": {"city": "Utrecht", "postal_code": "3500"},
        },
    }

    my_box = Box(nested_data)
    print(my_box.user.address.city)  # Access using dot notation


if __name__ == "__main__":
    main()
