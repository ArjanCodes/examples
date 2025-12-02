# before_contextvars_and_match.py
import asyncio
import random


# BEFORE: request_id passed manually
async def process_user(user_id: int, request_id: str):
    print(f"[Request {request_id}] Processing user {user_id}")
    amount = random.choice([-10, 0, 42, 50_000])
    print(f"[Request {request_id}] Amount {amount} → {classify_amount_before(amount)}")
    await asyncio.sleep(0.2)


# BEFORE: nested if/elif
def classify_amount_before(amount: float) -> str:
    if amount < 0:
        return "invalid"
    elif amount == 0:
        return "zero"
    elif amount > 10_000:
        return "large"
    else:
        return "normal"


# BEFORE: all state manually threaded into calls
async def handle_request(request_id: str, user_id: int):
    await process_user(user_id, request_id)


async def main():
    await asyncio.gather(
        handle_request("abc123", 1),
        handle_request("xyz789", 2),
    )


if __name__ == "__main__":
    asyncio.run(main())
