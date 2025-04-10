import random
import time


# Simulated API call that randomly succeeds or times out
def fetch_from_primary_api(city: str) -> dict[str, str]:
    if simulate_timeout():
        raise TimeoutError("Primary API timed out.")
    return {"status": "success", "data": f"Weather in {city} is sunny."}


def fetch_from_backup_api(city: str) -> dict[str, str]:
    if simulate_timeout():
        raise TimeoutError("Backup API timed out.")
    return {"status": "success", "data": f"Backup: Weather in {city} is cloudy."}


def simulate_timeout() -> bool:
    time.sleep(0.2)  # network delay
    return random.random() < 0.5


# Bad: using exceptions for expected control flow
def get_weather_forecast(city: str) -> dict[str, str]:
    try:
        return fetch_from_primary_api(city)
    except TimeoutError:
        try:
            return fetch_from_backup_api(city)
        except TimeoutError:
            return {"status": "error", "message": "Both APIs timed out."}


def main():
    result = get_weather_forecast("New York")
    print(result)


if __name__ == "__main__":
    main()
