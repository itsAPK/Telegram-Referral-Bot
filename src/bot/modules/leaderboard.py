import csv
from telegram import Update,ParseMode,ChatAction
from telegram.ext import CallbackContext,MessageHandler,CommandHandler,ConversationHandler,Filters,run_async

from bot import (LOGGER,SUPPORT_CHANNEL,dispatcher,updater)
from bot.modules.sql.user_sql import get_top_usrs,get_all
from bot.modules.helper_funcs.decorators import send_action,admin_only,contest

@send_action(ChatAction.TYPING)
@contest
def leaderboard(update : Update,context : CallbackContext):
    users=get_top_usrs()
    context.bot.send_message(update.message.chat.id,users,parse_mode=ParseMode.HTML,disable_web_page_preview=True)
    
@send_action(ChatAction.UPLOAD_DOCUMENT)
@admin_only
def export_data(update : Update,context : CallbackContext):
    users=get_all()
    with open("users.csv","w",encoding='UTF-8') as f:
        writer = csv.writer(f,delimiter=",",lineterminator="\n")
        writer.writerow(['User ID','Name','Username','Score','Total Referral','Invalid Refferal','Refered By',"Wallet Address",'Joined'])
        for user in users:
            if user.username:
                username= user.username
            else:
                continue
            if user.first_name:
                first_name= user.first_name
            else:
                first_name= ""
            if user.last_name:
                last_name= user.last_name
            else:
                last_name= ""
            name= (first_name + ' ' + last_name).strip()
            writer.writerow([user.chat_id,name,username,user.score,user.refferal,user.invalid_ref,user.refferal_id,user.wallet,user.joined]) 
    context.bot.send_document(update.effective_message.chat_id,open('users.csv', 'r',encoding='utf-8'),filename='users.csv')
    
__mod_name__='leaderboard'

LEADERBOARD_HANDLER=MessageHandler(Filters.regex('^🔝 Leaderboard$'),leaderboard)

EXPORT_DATA_HANDLER=MessageHandler(Filters.regex('^ℹ️ Export Data$'),export_data)

dispatcher.add_handler(LEADERBOARD_HANDLER)
dispatcher.add_handler(EXPORT_DATA_HANDLER)