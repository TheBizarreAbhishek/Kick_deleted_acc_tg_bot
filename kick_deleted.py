from telethon import TelegramClient
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
import asyncio
import datetime
import os

api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
group = os.environ["GROUP_USERNAME"]

async def clear_chat(client):
    deleted_accounts = 0
    total_scanned = 0

    async for user in client.iter_participants(group):
        total_scanned += 1
        if user.deleted:
            try:
                deleted_accounts += 1
                await client(EditBannedRequest(group, user, ChatBannedRights(
                   until_date=datetime.timedelta(minutes=1),
                   view_messages=True
                )))
            except Exception as exc:
                print(f"Failed to kick one deleted account because: {str(exc)}")

    if deleted_accounts:
        print(f"{deleted_accounts} deleted account(s) has been removed from this group 🚫👻")
    else:
        print(f"No deleted account found from {total_scanned} scanned users from this group 🚫👻")

async def main():
    async with TelegramClient("deleteacc", api_id, api_hash) as client:
        await clear_chat(client)

if __name__ == "__main__":
    asyncio.run(main())
