def main() -> None:
    names = ["Arjan", "Marieke", "Pim", "Sanne", "Daan", "Eva", "Lars"]

    for i in range(len(names)):
        print(i, names[i])

    # or more pythonic
    for index, name in enumerate(names):
        print(index, name)

if __name__ == "__main__":
    main()