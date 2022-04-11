import importlib, traceback, html, json
import re
from typing import Optional, List
from telegram import Message, Chat, User,ChatAction,Update
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, Filters, MessageHandler, CallbackQueryHandler,Defaults,CallbackContext,ConversationHandler
from telegram.ext.dispatcher import run_async, DispatcherHandlerStop
from telegram.utils.helpers import escape_markdown

from bot.modules import ALL_MODULES
from bot import(
    dispatcher,
    updater,
    LOGGER,
    SUDO_USERS,
    SUPPORT_CHANNEL,
    LOG_CHANNEL
)


IMPORTED={}

VALIDATE,IN_GROUP=range(2)


for module_name in ALL_MODULES:
    imported_module=importlib.import_module('bot.modules.'+module_name)
    if not hasattr(imported_module,"__mod_name__") :   
        imported_module.__mod_name__=imported_module.__name__
    
    if not imported_module.__mod_name__.lower() in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()]=imported_module
    else:
        raise Exception("Can't load with same name")


def error_handler(update, context):
    LOGGER.error(msg="Exception while handling an update:", exc_info=context.error)

    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb = "".join(tb_list)

    message = (
        "An exception was raised while handling an update\n"
        "<pre>update = {}</pre>\n\n"
        "<pre>{}</pre>"
    ).format(
        html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False)),
        html.escape(tb),
    )

    if len(message) >= 4096:
        message = message[:4096]

    context.bot.send_message(chat_id=LOG_CHANNEL, text=message, parse_mode=ParseMode.HTML)


def main():
    dispatcher.add_error_handler(error_handler)
    LOGGER.info("Using long polling.")
    updater.start_polling(timeout=15, read_latency=4)
    updater.idle()
    
if __name__ == "__main__":
    LOGGER.info("Successfully loaded modules: " + str(ALL_MODULES))
    main()