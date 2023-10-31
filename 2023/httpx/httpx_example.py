from typing import Any
import time
import httpx

BASE_URL = "https://httpbin.org"


def fetch_get() -> Any:
    response = httpx.get(f"{BASE_URL}/get")
    return response.json()


def fetch_post() -> Any:
    data_to_post = {"key": "value"}
    response = httpx.post(f"{BASE_URL}/post", json=data_to_post)
    return response.json()


def fetch_put() -> Any:
    data_to_put = {"key": "updated_value"}
    response = httpx.put(f"{BASE_URL}/put", json=data_to_put)
    return response.json()


def fetch_delete() -> Any:
    response = httpx.delete(f"{BASE_URL}/delete")
    return response.json()


def main() -> None:
    # record the starting time
    start = time.perf_counter()

    # GET
    print("GET:", fetch_get())

    # POST
    print("POST:", fetch_post())

    # PUT
    print("PUT:", fetch_put())

    # DELETE
    print("DELETE:", fetch_delete())

    # record the ending time
    end = time.perf_counter()
    print(f"Time taken: {end - start:.2f} seconds.")


if __name__ == "__main__":
    main()
