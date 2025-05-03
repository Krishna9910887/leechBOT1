from pyrogram.handlers import MessageHandler
from pyrogram.filters import command
from pyrogram.types import Message
from time import time

from bot import bot, LOGGER
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.message_utils import sendMessage, editMessage, deleteMessage
from bot.helper.ext_utils.bot_utils import get_readable_time

async def purge_message(_, message: Message):
    reply_to = message.reply_to_message
    msg = await sendMessage('<i>Deleting messages, please wait...</i>', message)
    if not reply_to:
        await editMessage('Reply to a message to purge from.', msg)
        return

    try:
        # Collect message IDs to delete (from reply_to.id to message.id)
        message_ids = list(range(reply_to.id, message.id))
        # Delete messages in the chat
        await bot.delete_messages(chat_id=message.chat.id, message_ids=message_ids)
        # Delete the original command message and update status
        await deleteMessage(message)
        await editMessage(
            f'Purged messages successfully in {get_readable_time(time() - message.date.timestamp()) or "0s"}.',
            msg
        )
    except Exception as e:
        LOGGER.error(f"Error purging messages: {e}")
        await editMessage(f'Failed to purge messages: {str(e)}', msg)

# Register the handler
bot.add_handler(
    MessageHandler(
        purge_message,
        filters=command(BotCommands.PurgeCommand) & CustomFilters.owner
    )
)