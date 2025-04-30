import random
import time


# Simulated API call that randomly succeeds or times out
def fetch_from_primary_api(city: str) -> dict[str, str]:
    if simulate_timeout():
        return {"status": "error", "message": "Primary API timed out."}
    return {"status": "success", "data": f"Weather in {city} is sunny."}


def fetch_from_backup_api(city: str) -> dict[str, str]:
    if simulate_timeout():
        return {"status": "error", "message": "Backup API timed out."}
    return {"status": "success", "data": f"Backup: Weather in {city} is cloudy."}


def simulate_timeout() -> bool:
    time.sleep(0.2)  # network delay
    return random.random() < 0.5


# Good: using return values for expected control flow
def get_weather_forecast(city: str) -> dict[str, str]:
    result = fetch_from_primary_api(city)
    if result["status"] == "error":
        result = fetch_from_backup_api(city)
    if result["status"] == "error":
        return {"status": "error", "message": "Both APIs timed out."}
    return result


def main():
    result = get_weather_forecast("New York")
    print(result)


if __name__ == "__main__":
    main()
