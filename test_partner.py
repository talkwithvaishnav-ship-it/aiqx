import asyncio
from partner import get_trader_info

async def main():
    data = await get_trader_info("89898321")
    print(data)

asyncio.run(main())