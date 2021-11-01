import asyncio

from iot.message import MessageType


class HueLightDevice:
    async def connect(self) -> None:
        print("Connecting Hue Light.")
        await asyncio.sleep(0.5)
        print("Hue Light connected.")

    async def disconnect(self) -> None:
        print("Disconnecting Hue Light.")
        await asyncio.sleep(0.5)
        print("Hue Light disconnected.")

    async def send_message(self, message_type: MessageType, data: str = "") -> None:
        print(
            f"Hue Light handling message of type {message_type.name} with data [{data}]."
        )
        await asyncio.sleep(0.5)
        print("Hue Light received message.")


class SmartSpeakerDevice:
    async def connect(self) -> None:
        print("Connecting to Smart Speaker.")
        await asyncio.sleep(0.5)
        print("Smart Speaker connected.")

    async def disconnect(self) -> None:
        print("Disconnecting Smart Speaker.")
        await asyncio.sleep(0.5)
        print("Smart Speaker disconnected.")

    async def send_message(self, message_type: MessageType, data: str = "") -> None:
        print(
            f"Smart Speaker handling message of type {message_type.name} with data [{data}]."
        )
        await asyncio.sleep(0.5)
        print("Smart Speaker received message.")


class SmartToiletDevice:
    async def connect(self) -> None:
        print("Connecting to Smart Toilet.")
        await asyncio.sleep(0.5)
        print("Smart Toilet connected.")

    async def disconnect(self) -> None:
        print("Disconnecting Smart Toilet.")
        await asyncio.sleep(0.5)
        print("Smart Toilet disconnected.")

    async def send_message(self, message_type: MessageType, data: str = "") -> None:
        print(
            f"Smart Toilet handling message of type {message_type.name} with data [{data}]."
        )
        await asyncio.sleep(0.5)
        print("Smart Toilet received message.")
