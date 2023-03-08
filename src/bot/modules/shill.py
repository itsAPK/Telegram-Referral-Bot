from telegram import Update, ParseMode, ChatAction
from telegram.ext import CallbackContext, MessageHandler, CommandHandler, ConversationHandler, Filters, run_async

from bot import dispatcher, LOGGER
from bot.modules.sql.shill_sql import add_shill1, add_shill2, add_shill3, get_shill, add_welcome_image, add_welcome_text
from bot.modules.helper_funcs.decorators import admin_only, send_action, contest
from bot.modules.helper_funcs.markup import admin_markup, cancel_markup, edit_shill_post_markup

POST, SHILL1, SHILL2, SHILL3, WELCOME, IMAGE = range(6)


@send_action(ChatAction.TYPING)
@admin_only
def edit_shill(update: Update, context: CallbackContext):
    context.bot.send_message(update.effective_message.chat_id,
                             "select the shill post to edit 👇", reply_markup=edit_shill_post_markup())
    return POST


@send_action(ChatAction.TYPING)
@admin_only
def add_post(update: Update, context: CallbackContext):

    if update.effective_message.text == 'SHILL - 1':
        context.bot.send_message(
            update.effective_message.chat_id,
            "Send a post [ Use HTML tags for blod,italic]",
            reply_markup=cancel_markup()
        )
        return SHILL1

    elif update.effective_message.text == 'SHILL - 2':
        context.bot.send_message(
            update.effective_message.chat_id,
            "Send a post [ Use HTML tags for blod,italic]",
            reply_markup=cancel_markup()
        )
        return SHILL2

    elif update.effective_message.text == 'SHILL - 3':
        context.bot.send_message(
            update.effective_message.chat_id,
            "Send a post [ Use HTML tags for blod,italic]",
            reply_markup=cancel_markup()
        )
        return SHILL3

    else:
        context.bot.send_message(update.effective_message.chat_id, "Invalid ")
        return -1


@send_action(ChatAction.TYPING)
@admin_only
def add_post_1(update: Update, context: CallbackContext):
    add_shill1(update.message.text)
    context.bot.send_message(update.message.chat.id,
                             update.message.text, parse_mode=ParseMode.HTML)
    context.bot.send_message(update.message.chat.id,
                             "Done", reply_markup=admin_markup())

    return -1


@send_action(ChatAction.TYPING)
@admin_only
def add_post_2(update: Update, context: CallbackContext):

    add_shill2(update.message.text)
    context.bot.send_message(update.message.chat.id,
                             update.message.text, parse_mode=ParseMode.HTML)
    context.bot.send_message(update.message.chat.id,
                             "Done", reply_markup=admin_markup())

    return -1


@send_action(ChatAction.TYPING)
@admin_only
def add_post_3(update: Update, context: CallbackContext):

    add_shill3(update.message.text)
    context.bot.send_message(update.message.chat.id,
                             update.message.text, parse_mode=ParseMode.HTML)
    context.bot.send_message(update.message.chat.id,
                             "Done", reply_markup=admin_markup())

    return -1


@send_action(ChatAction.TYPING)
@admin_only
def cancel_shill(update: Update, context: CallbackContext):
    context.bot.send_message(
        update.effective_message.chat_id, "Cancelled", reply_markup=admin_markup())

    return -1


@send_action(ChatAction.TYPING)
@contest
def shill1(update: Update, context: CallbackContext):
    shill = get_shill()
    me = context.bot.get_me()
    data = f"{shill.shill1}\n\n<b>TG</b> : https://t.me/{me.username}?start={update.effective_message.chat_id} "
    context.bot.send_message(update.effective_message.chat_id, data,
                             disable_web_page_preview=True, parse_mode=ParseMode.HTML)


@send_action(ChatAction.TYPING)
@contest
def shill2(update: Update, context: CallbackContext):
    shill = get_shill()
    me = context.bot.get_me()
    data = f"{shill.shill2}\n\n<b>TG</b> : https://t.me/{me.username}?start={update.effective_message.chat_id} "
    context.bot.send_message(update.effective_message.chat_id, data,
                             disable_web_page_preview=True, parse_mode=ParseMode.HTML)


@send_action(ChatAction.TYPING)
@contest
def shill3(update: Update, context: CallbackContext):
    shill = get_shill()
    me = context.bot.get_me()
    data = f"{shill.shill3}\n\n<b>TG</b> : https://t.me/{me.username}?start={update.effective_message.chat_id} "
    context.bot.send_message(update.effective_message.chat_id, data,
                             disable_web_page_preview=True, parse_mode=ParseMode.HTML)


@send_action(ChatAction.TYPING)
@admin_only
def set_welcome_message(update: Update, context: CallbackContext):
    context.bot.send_message(update.effective_message.chat_id,
                             "Send a welcome text [ Use HTML tags for blod,italic]", reply_markup=cancel_markup())
    return WELCOME


@send_action(ChatAction.TYPING)
@admin_only
def process_welcome_text(update: Update, context: CallbackContext):
    add_welcome_text(update.message.text)
    context.bot.send_message(update.message.chat.id,
                             update.message.text, parse_mode=ParseMode.HTML)
    context.bot.send_message(update.message.chat.id,
                             "Done", reply_markup=admin_markup())

    return -1


@send_action(ChatAction.TYPING)
@admin_only
def set_welcome_image(update: Update, context: CallbackContext):
    context.bot.send_message(update.effective_message.chat_id,
                             "Send the image link\n\nUpload Image https://ibb.co and send the link below.",
                             reply_markup=cancel_markup())
    return IMAGE


@send_action(ChatAction.TYPING)
@admin_only
def process_welcome_image(update: Update, context: CallbackContext):
    add_welcome_image(update.message.text)
    context.bot.send_photo(update.message.chat.id, update.message.text)
    context.bot.send_message(update.message.chat.id,
                             "Done", reply_markup=admin_markup())

    return -1


EDIT_SHILL_POST_HANDLER = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex(
        '^📝 Edit Shill Post$'), edit_shill)],
    states={
        POST: [
            MessageHandler(Filters.regex('^SHILL - 1$'), add_post),
            MessageHandler(Filters.regex('^SHILL - 2$'), add_post),
            MessageHandler(Filters.regex('^SHILL - 3$'), add_post),


        ],
        SHILL1: [MessageHandler(Filters.text & ~Filters.regex('^🚫 Cancel$'), add_post_1)],
        SHILL2: [MessageHandler(Filters.text & ~Filters.regex('^🚫 Cancel$'), add_post_2)],
        SHILL3: [MessageHandler(
            Filters.text & ~Filters.regex('^🚫 Cancel$'), add_post_3)]

    },
    fallbacks=[
        MessageHandler(Filters.regex('^🚫 Cancel$'), cancel_shill),
        MessageHandler(Filters.regex('^🔙 Back$'), cancel_shill),
    ]

)

SHILL1_HANDLER = MessageHandler(Filters.regex('^SHILL - 1$'), shill1)
SHILL2_HANDLER = MessageHandler(Filters.regex('^SHILL - 2$'), shill2)
SHILL3_HANDLER = MessageHandler(Filters.regex('^SHILL - 3$'), shill3)

SET_WELCOME_TEXT_HANDLER = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex(
        '^✉️ Set Message$'), set_welcome_message)],
    states={
        WELCOME: [MessageHandler(Filters.text & ~Filters.regex(
            '^🚫 Cancel$'), process_welcome_text)]
    },
    fallbacks=[
        MessageHandler(Filters.regex('^🚫 Cancel$'), cancel_shill)]
)

SET_WELCOME_IMAGE_HANDLER = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex(
        '^🖼 Set Image$'), set_welcome_image)],
    states={
        IMAGE: [MessageHandler(Filters.text, process_welcome_image)]
    },
    fallbacks=[
        MessageHandler(Filters.regex('^🚫 Cancel$'), cancel_shill)]
)


dispatcher.add_handler(EDIT_SHILL_POST_HANDLER)
dispatcher.add_handler(SHILL1_HANDLER)
dispatcher.add_handler(SHILL2_HANDLER)
dispatcher.add_handler(SHILL3_HANDLER)
dispatcher.add_handler(SET_WELCOME_TEXT_HANDLER)
dispatcher.add_handler(SET_WELCOME_IMAGE_HANDLER)
