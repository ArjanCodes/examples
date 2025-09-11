def risky_function(value: str) -> int:
    if value == "int":
        return int("not a number")  # raises ValueError
    elif value == "key":
        return {"a": 1}["b"]  # raises KeyError
    else:
        raise RuntimeError("Something else went wrong")

def main() -> None:
    try:
        risky_function("key")
    except ValueError, KeyError:
        print("Caught either ValueError or KeyError")
    except RuntimeError as e:
        print(f"Caught a runtime error: {e}")

if __name__ == "__main__":
    main()