from telegram import Update,ParseMode,ChatAction
from telegram.ext import CallbackContext,MessageHandler,CommandHandler,ConversationHandler,Filters,run_async
from telegram.error import Unauthorized

from bot import (LOGGER,SUPPORT_CHANNEL,dispatcher,updater)
from bot.modules.sql.user_sql import add_invalid_ref,get_users_id,get_user_data

def leave_users(update : Update , context : CallbackContext):
    if update.message.from_user.id in get_users_id():
        data=get_user_data(update.message.from_user.id)
        if not data.refferal_id==None:
            add_invalid_ref(data.refferal_id)
            
            
LEAVE_USER_HANDLER=MessageHandler(Filters.status_update.left_chat_member,leave_users)

dispatcher.add_handler(LEAVE_USER_HANDLER)