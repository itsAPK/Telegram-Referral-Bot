from telegram import Update,ParseMode,ChatAction
from telegram.ext import CallbackContext,MessageHandler,CommandHandler,ConversationHandler,Filters,run_async

from bot import dispatcher,LOGGER
from bot.modules.helper_funcs.decorators import admin_only,send_action
from bot.modules.sql.settings_sql import update_contest

@send_action(ChatAction.TYPING)
@admin_only
def open_contest(update : Update,context : CallbackContext):
    update_contest(True)
    context.bot.send_message(update.effective_message.chat_id,"Contest Opened")

@send_action(ChatAction.TYPING)
@admin_only
def close_contest(update : Update,context : CallbackContext):
    update_contest(False)
    context.bot.send_message(update.effective_message.chat_id,"Contest Closed")
    
    
OPEN_CONTEST_HANDLER=MessageHandler(Filters.regex('^🔓 Open Contest$'),open_contest)
CLOSE_CONTEST_HANDLER=MessageHandler(Filters.regex('^🔒 Close Contest$'),close_contest)

dispatcher.add_handler(OPEN_CONTEST_HANDLER)
dispatcher.add_handler(CLOSE_CONTEST_HANDLER)