from telethon import TelegramClient
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
import asyncio
import os
import datetime

bot_token = os.environ["BOT_TOKEN"]
group_id = int(os.environ["GROUP_ID"])  # Format: -100xxxxxxxxxx

async def clear_chat(client):
    deleted_accounts = 0
    total_scanned = 0

    async for user in client.iter_participants(group_id):
        total_scanned += 1
        if user.deleted:
            try:
                deleted_accounts += 1
                await client(EditBannedRequest(
                    channel=group_id,
                    user_id=user.id,
                    banned_rights=ChatBannedRights(
                        until_date=datetime.timedelta(seconds=60),
                        view_messages=True
                    )
                ))
            except Exception as e:
                print(f"Failed to kick user {user.id}: {e}")

    if deleted_accounts:
        print(f"{deleted_accounts} deleted account(s) has been removed from this group 🚫👻")
    else:
        print(f"No deleted account found from {total_scanned} scanned users from this group 🚫👻")

async def main():
    async with TelegramClient('bot', api_id=0, api_hash='none').start(bot_token=bot_token) as client:
        await clear_chat(client)

if __name__ == "__main__":
    asyncio.run(main())
