ListResult = list[tuple[int, int]]


def what() -> ListResult:
    return [(x, y) for x in range(10) for y in range(5) if x * y > 10]


def better() -> ListResult:
    result: ListResult = []
    for x in range(10):
        for y in range(5):
            if x * y > 10:
                result.append((x, y))
    return result


def what_the():
    return (
        (x, y, z)
        for x in range(5)
        for y in range(5)
        if x != y
        for z in range(5)
        if y != z
    )


def main():
    print(what())
    print(better())
    for x in what_the():
        print(x)


if __name__ == "__main__":
    main()
