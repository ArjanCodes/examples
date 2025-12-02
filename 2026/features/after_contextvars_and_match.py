# example_contextvars_and_match.py
import asyncio
import contextvars
import random

request_id = contextvars.ContextVar("request_id", default="unknown")


def log(msg: str):
    print(f"[Request {request_id.get()}] {msg}")


def classify_amount(amount: float) -> str:
    match amount:
        case x if x < 0:
            return "invalid"
        case 0:
            return "zero"
        case x if x > 10_000:
            return "large"
        case _:
            return "normal"


async def process_user(user_id: int):
    log(f"Processing user {user_id}")
    amount = random.choice([-10, 0, 42, 50_000])
    log(f"Amount {amount} → {classify_amount(amount)}")
    await asyncio.sleep(0.2)


async def handle_request(req_id: str, user_id: int):
    token = request_id.set(req_id)
    try:
        await process_user(user_id)
    finally:
        request_id.reset(token)


async def main():
    await asyncio.gather(
        handle_request("abc123", 1),
        handle_request("xyz789", 2),
    )


if __name__ == "__main__":
    asyncio.run(main())
