from functools import wraps
from bot import SUPPORT_CHANNEL,SUDO_USERS
from bot.modules.helper_funcs.text import ERROR
from telegram import ParseMode
from telegram.error import Unauthorized
from bot.modules.sql.admin_sql import get_admins
from bot.modules.sql.settings_sql import get_contest


def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        def command_func(update, context, *args, **kwargs):
            try:
                context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
                return func(update, context,  *args, **kwargs)
            except Unauthorized:
                return -1
        return command_func
    
    return decorator

def check_user(func):
    @wraps(func)
    def command_func(update,context,*args, **kwargs):
        a=context.bot.get_chat_member(chat_id=f'@{SUPPORT_CHANNEL}',user_id=update.effective_message.chat_id)
        if a.status in ['member','creator','administartor']:
           return func(update, context,  *args, **kwargs)
        context.bot.send_message(update.effective_message.chat_id,ERROR,parse_mode=ParseMode.HTML)
    return command_func


def admin_only(func):
    @wraps(func)
    def command_func(update,context,*args, **kwargs):
        if update.effective_message.chat_id in get_admins() or update.effective_message.chat_id in SUDO_USERS:
            return func(update, context,  *args, **kwargs)
        context.bot.send_message(update.effective_message.chat_id,"This acess only for admin")
    return command_func

def contest(func):
    @wraps(func)
    def command_func(update,context,*args, **kwargs):
        if get_contest() == True:
            return func(update, context,  *args, **kwargs)
        else:
            context.bot.send_message(update.effective_message.chat_id,"<b>Contest Closed</b>")
            return -1
    return command_func