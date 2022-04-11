from telegram import Update,ParseMode,ChatAction
from telegram.ext import CallbackContext,MessageHandler,CommandHandler,ConversationHandler,Filters,run_async

from bot import dispatcher,LOGGER
from bot.modules.sql.admin_sql import add_admin
from bot.modules.helper_funcs.decorators import admin_only,send_action
from bot.modules.helper_funcs.markup import admin_markup,cancel_markup

@send_action(ChatAction.TYPING)
@admin_only
def admin(update : Update, context : CallbackContext):
    context.bot.send_message(update.effective_message.chat_id,"You Logged in as admin",reply_markup=admin_markup())
    

ADMIN_FORWARD=range(1)

@send_action(ChatAction.TYPING)
@admin_only    
def add_admin_message(update : Update,context : CallbackContext):
    context.bot.send_message(update.effective_message.chat_id,"Forward message from user you wan to make admin",reply_markup=cancel_markup())
    return ADMIN_FORWARD

@send_action(ChatAction.TYPING)
def validate_admin(update : Update,context : CallbackContext):
    add_admin(update.message.forward_from.id)
    context.bot.send_message(
        update.effective_message.chat_id,
        f'{update.message.forward_from.first_name} added as admin sucessfully',
        reply_markup=admin_markup()
    )
    LOGGER.info(f'{update.message.forward_from.first_name} added as admin sucessfully')
    return -1
    
@send_action(ChatAction.TYPING) 
def cancel_add_admin(update : Update,context : CallbackContext):
    context.bot.send_message(update.effective_message.chat_id,"Cancelled",reply_markup=admin_markup())

ADMIN_HANDLER=CommandHandler('admin_start',admin)

ADD_ADMIN_HANDLER=ConversationHandler(
    entry_points=[MessageHandler(Filters.regex('^➕ Add Admin$'),add_admin_message)],
    states={
        ADMIN_FORWARD:[MessageHandler(Filters.forwarded,validate_admin)]
    },
    fallbacks=[MessageHandler(Filters.regex('^🚫 Cancel$'),cancel_add_admin)]

)

dispatcher.add_handler(ADMIN_HANDLER)
dispatcher.add_handler(ADD_ADMIN_HANDLER)