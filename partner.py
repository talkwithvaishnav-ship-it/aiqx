from telethon_client import client
from parser import parse_partner_reply

BOT_USERNAME = "@QuotexPartnerBot"

async def get_trader_info(trader_id):

    await client.start()

    async with client.conversation(BOT_USERNAME, timeout=20) as conv:

        await conv.send_message(str(trader_id))

        response = await conv.get_response()

        print("========== RAW REPLY ==========")
        print(repr(response.text))
        print("================================")

        return parse_partner_reply(response.text)