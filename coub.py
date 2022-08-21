import aiohttp
import asyncio

from loguru import logger


async def subscribe_coub(worker: str, queue: asyncio.Queue) -> None:
    while not queue.empty():
        email = await queue.get()

        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://coub-gtw.coub.com/marketplace/public/api/v1/emails",
                json={"email": email}
            ) as resp:
                if resp.status == 200:
                    logger.success(
                        f"{worker} - {email} successfully registered")
                else:
                    logger.error(f"{worker} - {email} - error!")


async def main(emails):
    queue = asyncio.Queue()

    for email in emails:
        queue.put_nowait(email)

    tasks = [asyncio.create_task(subscribe_coub(
             f"Worker {i}", queue)) for i in range(5)]

    await asyncio.gather(*tasks)