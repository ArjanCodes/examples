def main():
    greet = "Hi"

    # Adding spaces to the left
    print(f"{greet:>10}")

    # Various alignment options
    print(f"{greet:_^10}")
    print(f"{greet:_<10}")
    print(f"{greet:_>10}")

    print(f"{3.4:10}")  # numbers are right aligned
    print(f"{3820.45:2}")  # value can be larger than the width

    print(f"{100.345736:.2f}")  # .2f is the number of decimal places

    print(f"{1000000:,.2f}")  # grouping thousands
    print(f"{1000000:_.2f}")  # grouping thousands

    print(f"{0.34576:%}")  # percentage
    print(f"{0.34576:.2%}")  # percentage with precision


if __name__ == "__main__":
    main()
