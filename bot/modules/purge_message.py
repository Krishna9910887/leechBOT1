from pyrogram import Client
from pyrogram.types import Message
from bot.helper.telegram_helper.message_utils import sendMessage, editMessage, deleteMessage
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.filters import CustomFilters
from asyncio import gather
from time import time
from bot.helper.ext_utils.bot_utils import get_readable_time

async def purge_message(client: Client, message: Message):
    reply_to = message.reply_to_message
    start_time = time()
    msg = await sendMessage('<i>Deleting messages, please wait...</i>', message)
    
    if not reply_to:
        await editMessage('Reply to a message to purge from.', msg)
        return

    async def _delete(mid, nolog=True):
        try:
            await client.delete_messages(message.chat.id, mid)
        except Exception as e:
            LOGGER.error(f"Failed to delete message {mid}: {e}")

    await gather(*[_delete(mid) for mid in range(reply_to.id, message.id + 1)])
    await gather(
        deleteMessage(message),
        editMessage(
            f'Purged messages successfully in {get_readable_time(time() - start_time) or "0s"}.',
            msg
        )
    )

# Add handler to the bot
bot.add_handler(
    MessageHandler(
        purge_message,
        filters=command(BotCommands.PurgeCommand) & CustomFilters.owner
    )
)