from typing import Any
import time
import requests

BASE_URL = "https://httpbin.org"


def fetch_get(session: requests.Session) -> Any:
    response = session.get(f"{BASE_URL}/get")
    return response.json()


def fetch_post(session: requests.Session) -> Any:
    data_to_post = {"key": "value"}
    response = session.post(f"{BASE_URL}/post", json=data_to_post)
    return response.json()


def fetch_put(session: requests.Session) -> Any:
    data_to_put = {"key": "updated_value"}
    response = session.put(f"{BASE_URL}/put", json=data_to_put)
    return response.json()


def fetch_delete(session: requests.Session) -> Any:
    response = session.delete(f"{BASE_URL}/delete")
    return response.json()


def main() -> None:
    # record the starting time
    start = time.perf_counter()

    with requests.Session() as session:
        # GET
        print(fetch_get(session))

        # POST
        print(fetch_post(session))

        # PUT
        print(fetch_put(session))

        # DELETE
        print(fetch_delete(session))

    # record the ending time
    end = time.perf_counter()
    print(f"Time taken: {end - start:.2f} seconds.")


if __name__ == "__main__":
    main()
