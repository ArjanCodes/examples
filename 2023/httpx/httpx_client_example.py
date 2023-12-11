from typing import Any
import time
import httpx

BASE_URL = "https://httpbin.org"


def fetch_get(client: httpx.Client) -> Any:
    response = client.get(f"{BASE_URL}/get")
    return response.json()


def fetch_post(client: httpx.Client) -> Any:
    data_to_post = {"key": "value"}
    response = client.post(f"{BASE_URL}/post", json=data_to_post)
    return response.json()


def fetch_put(client: httpx.Client) -> Any:
    data_to_put = {"key": "updated_value"}
    response = client.put(f"{BASE_URL}/put", json=data_to_put)
    return response.json()


def fetch_delete(client: httpx.Client) -> Any:
    response = client.delete(f"{BASE_URL}/delete")
    return response.json()


def main() -> None:
    # record the starting time
    start = time.perf_counter()

    with httpx.Client() as client:
        # GET
        print("GET:", fetch_get(client))

        # POST
        print("POST:", fetch_post(client))

        # PUT
        print("PUT:", fetch_put(client))

        # DELETE
        print("DELETE:", fetch_delete(client))

    # record the ending time
    end = time.perf_counter()
    print(f"Time taken: {end - start:.2f} seconds.")


if __name__ == "__main__":
    main()
