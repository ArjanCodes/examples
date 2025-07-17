from graphlib import TopologicalSorter

ts = TopologicalSorter[str]()


def main() -> None:
    # Tasks and their dependencies
    ts.add("compile", "fetch_sources")
    ts.add("test", "compile")
    ts.add("package", "test")
    ts.add("deploy", "package")
    ts.add("fetch_sources")

    order = list(ts.static_order())
    print("Execution order:", order)


if __name__ == "__main__":
    main()
