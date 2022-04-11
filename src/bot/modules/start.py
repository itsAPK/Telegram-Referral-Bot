from telegram import Update,ParseMode,ChatAction
from telegram.ext import CallbackContext,MessageHandler,CommandHandler,ConversationHandler,Filters,run_async

from bot import SUPPORT_CHANNEL,LOGGER,updater,dispatcher
from bot.modules.helper_funcs.text import ERROR,START_MESSAGE
from bot.modules.helper_funcs.decorators import send_action,contest
from bot.modules.helper_funcs.markup import join_markup,start_markup
from bot.modules.sql.user_sql import get_users_id,add_referral,add_user
from bot.modules.sql.shill_sql import get_welcome

VALIDATE,START_OVER=range(2)

@send_action(ChatAction.TYPING)
def start(update : Update,context : CallbackContext) :
    context.user_data[START_OVER]=update.message
    is_in_grp=context.bot.get_chat_member(f"@{SUPPORT_CHANNEL}",update.effective_message.chat_id)
    if not is_in_grp.status in  ['member','creator','administartor']:
        context.bot.send_message(update.effective_message.chat_id,ERROR,parse_mode=ParseMode.HTML,reply_markup=join_markup())
        return VALIDATE
    valid_user(update,context)
    return -1


def validate_user(update : Update,context : CallbackContext):
    is_in_grp=context.bot.get_chat_member(f"@{SUPPORT_CHANNEL}",update.effective_message.chat_id)
    if not is_in_grp.status in  ['member','creator','administrator']:
        context.bot.send_message(update.effective_message.chat_id,ERROR,parse_mode=ParseMode.HTML)
        return VALIDATE
    valid_user(update,context)
    return -1
    

@send_action(ChatAction.TYPING)
@contest
def valid_user(update:Update,context : CallbackContext):
    data=context.user_data.get(START_OVER)
    welcome=get_welcome()
    ref_id=data.text[7:]
    if not ref_id == '':
        if not data.chat.id in get_users_id():    
            add_referral(int(ref_id))
    add_user(data)
    context.bot.send_photo(
        update.effective_message.chat_id,
        welcome.image,
        caption=welcome.text,
        parse_mode=ParseMode.HTML,
        reply_markup=start_markup())
    return -1
    
@send_action(ChatAction.TYPING)
def back(update : Update,context : CallbackContext):
    context.bot.send_message(update.message.chat.id,f"Hey {update.message.chat.first_name}",reply_markup=start_markup())
    
__mod_name__='start'


START_HANDLER = ConversationHandler(
        entry_points=[CommandHandler('start',start,pass_args=True)],
        states={
            VALIDATE:[MessageHandler(filters=Filters.regex('^✅ Joined$'),callback=validate_user,pass_user_data=True)]
            },
        fallbacks=[],
        
    )

BACK_HANDLER=MessageHandler(Filters.regex('^🔙 Back$'),back)
    
dispatcher.add_handler(START_HANDLER)
dispatcher.add_handler(BACK_HANDLER)