from telegram import Update,ParseMode,ChatAction
from telegram.ext import CallbackContext,MessageHandler,CommandHandler,ConversationHandler,Filters,CallbackQueryHandler

from bot import (LOGGER,SUPPORT_CHANNEL,dispatcher,updater)
from bot.modules.sql.user_sql import (get_user_data,get_rank,
                                        get_new_referral_user,
                                        get_new_user_count,
                                        get_referral_users_count,
                                        get_total_user_count,
                                        set_user_wallet)
from bot.modules.helper_funcs.decorators import send_action,admin_only,contest
from bot.modules.helper_funcs.markup import cancel_markup,admin_markup,dashboard_markup,start_markup

USER_INFO,WALLET=range(2)

@contest
@send_action(ChatAction.TYPING)
def dashboard(update : Update, context : CallbackContext):
    user=get_user_data(update.effective_message.chat_id)
    rank=get_rank(update.effective_message.chat_id)
    me=context.bot.get_me()
    
    data=f"""
🆔 <b>ID</b> : {update.effective_message.chat_id}
📛 <b>Name</b> : {update.message.chat.first_name}
🏆 <b>Rank</b> : {rank}
🎯 <b>Score</b> : {user.score}
👥 <b>Total Referral</b> : {user.refferal}
❌ <b>Invalid Referral</b> : {user.invalid_ref}
🧰 <b>Wallet :</b> <code>{user.wallet}</code>
🌐 <b>Referral Link</b> : https://t.me/{me.username}?start={update.effective_message.chat_id}
"""
    context.bot.send_message(update.effective_message.chat_id,data,reply_markup=dashboard_markup())



@send_action(ChatAction.TYPING)
@admin_only    
def get_user_details(update : Update,context : CallbackContext):
    context.bot.send_message(update.effective_message.chat_id,"Forward message from user to get their details",reply_markup=cancel_markup())
    return USER_INFO

@send_action(ChatAction.TYPING)
def processed_deatils(update : Update,context : CallbackContext):
    user=get_user_data(update.message.forward_from.id)
    if not user:
        context.bot.send_message(
            update.effective_message.chat_id,
            "No data found :(",
            reply_markup=admin_markup()
        )
    else:
        rank=get_rank(update.message.forward_from.id)
        
        
        data=f"""
🆔 <b>ID</b> : {user.chat_id}
📛 <b>Name</b> : {user.first_name} (@{user.username})
🏆 <b>Rank</b> : {rank}
🎯 <b>Score</b> : {user.score}
👥 <b>Total Referral</b> : {user.refferal}
❌ <b>Invalid Referral</b> : {user.invalid_ref}
🧰 <b>Wallet :</b> <code>{user.wallet}</code>

    """
        context.bot.send_message(
            update.effective_message.chat_id,
            data,
            parse_mode=ParseMode.HTML,
            reply_markup=admin_markup()
        )
    
    return -1
    
@send_action(ChatAction.TYPING) 
def cancel_user_details(update : Update,context : CallbackContext):
    context.bot.send_message(update.effective_message.chat_id,"Cancelled",reply_markup=admin_markup())

@admin_only
@send_action(ChatAction.TYPING)
def bot_stats(update : Update,context : CallbackContext):
    data=f"""

<b>Total Users :</b> {get_total_user_count()}
<b>New Users [24h] :</b> {get_new_user_count()}
<b>Total Referd Users :</b> {get_referral_users_count()}
<b>New Referd Users [24h]: </b> {get_new_referral_user()}
<b>Average Referrals : </b> {get_new_referral_user()/get_total_user_count()}

"""
    context.bot.send_message(update.effective_message.chat_id,data,parse_mode=ParseMode.HTML)

@send_action(ChatAction.TYPING)
@contest
def set_wallet(update : Update,context : CallbackContext):
    context.bot.send_message(update.effective_message.chat_id,"Please send your <b>Solana Wallet</b> address ",reply_markup=cancel_markup())
    
    return WALLET

@send_action(ChatAction.TYPING) 
def cancel_set_wallet(update : Update,context : CallbackContext):
    context.bot.send_message(update.effective_message.chat_id,"Cancelled",reply_markup=start_markup())
    
    return -1

@send_action(ChatAction.TYPING)
def invalid_wallet(update : Update,context : CallbackContext):
    context.bot.send_message(update.effective_message.chat_id,"Invalid Address",reply_markup=start_markup())
    return -1
    
@send_action(ChatAction.TYPING)
def process_set_wallet(update : Update,context : CallbackContext):
    set_user_wallet(update.effective_message.chat_id,update.message.text)
    context.bot.send_message(update.effective_message.chat_id,"Wallet added sucessfully",reply_markup=start_markup())
    return -1

__mod_name__='dashboard'
 
DASHBOARD_HANDLER=MessageHandler(Filters.regex('^📋 Dashboard$'),dashboard)

USER_INFO_HANDLER=ConversationHandler(
    entry_points=[MessageHandler(Filters.regex('^👤 Get User Info$'),get_user_details)],
    states={
        USER_INFO:[MessageHandler(Filters.forwarded,processed_deatils)]
    },
    fallbacks=[MessageHandler(Filters.regex('^🚫 Cancel$'),cancel_user_details)]

)

STATS_HANDLER=MessageHandler(Filters.regex('^📊 Statistics$'),bot_stats)


SET_WALLET_HANDLER=ConversationHandler(
    entry_points=[(CallbackQueryHandler(set_wallet,pattern=r'^set_wallet$',))],
    states={
        WALLET:[MessageHandler(Filters.regex(r'^0x[a-fA-F0-9]{40}$'),process_set_wallet)]
    },
    fallbacks=[
        MessageHandler(Filters.text & ~Filters.regex('^🚫 Cancel$'),invalid_wallet),
        MessageHandler(Filters.regex('^🚫 Cancel$'),cancel_set_wallet)
    ]
    )




dispatcher.add_handler(DASHBOARD_HANDLER)
dispatcher.add_handler(USER_INFO_HANDLER)
dispatcher.add_handler(STATS_HANDLER)
dispatcher.add_handler(SET_WALLET_HANDLER)