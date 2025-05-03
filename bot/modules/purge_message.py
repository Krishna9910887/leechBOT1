#!/usr/bin/env python3
from pyrogram.handlers import MessageHandler
from pyrogram.filters import command
from time import time
from asyncio import gather

from bot import bot, LOGGER
from bot.helper.telegram_helper.message_utils import sendMessage, editMessage, deleteMessage
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.ext_utils.bot_utils import new_task
from bot.helper.ext_utils.status_utils import get_readable_time


@new_task
async def purge_message(client, message):
    """Purge messages from the replied-to message up to the command message."""
    start_time = time()
    reply_to = message.reply_to_message
    msg = await sendMessage('<i>Deleting messages, please wait...</i>', message)
    
    if not reply_to:
        await editMessage('Reply to a message to purge from.', msg)
        return

    try:
        # Collect message IDs to delete (from reply_to.id to message.id - 1)
        message_ids = range(reply_to.id, message.id)
        # Delete messages in batches to avoid API limits
        await client.delete_messages(
            chat_id=message.chat.id,
            message_ids=message_ids
        )
        # Delete the command message itself
        await deleteMessage(message)
        # Update the status message with the time taken
        elapsed_time = get_readable_time(time() - start_time)
        await editMessage(f'Purged messages successfully in {elapsed_time}.', msg)
    except Exception as e:
        LOGGER.error(f"Purge error: {e}")
        await editMessage(f'Failed to purge messages: {str(e)}', msg)


# Register the purge_message handler
bot.add_handler(
    MessageHandler(
        purge_message,
        filters=command(BotCommands.PurgeCommand) & CustomFilters.sudo
    )
)