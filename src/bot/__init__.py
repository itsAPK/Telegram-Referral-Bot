import betterlogging as logging
import os
import sys
import telegram.ext as tg
from telegram import ParseMode
from bot.config import Config

LOGGER = logging.get_colorized_logger(name=__name__)



handler = logging.StreamHandler()
handler.setFormatter(logging.ColorizedFormatter())

#LOGGER.addHandler(handler)
LOGGER.setLevel(logging.TRACE)



logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
#LOGGER = logging.getLogger(__name__)


LOGGER.info("Startings")

# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error(
        "You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting."
    )
try:
    SUDO_USERS = set(int(x) for x in Config.SUDO_USERS or [])
except ValueError:
    raise Exception("Your sudo users list does not contain valid integers.")


DATABASE_URI = Config.DATABASE_URI
LOG_CHANNEL=Config.LOG_CHANNEL
BOT_TOKEN=Config.BOT_TOKEN
WORKERS=Config.WORKERS
SUPPORT_CHANNEL=Config.SUPPORT_CHANNEL
LOAD=[]
NOLOAD=[]

defaults=tg.Defaults(run_async=True,parse_mode=ParseMode.HTML,disable_web_page_preview=True)

updater = tg.Updater(BOT_TOKEN, workers=WORKERS, use_context=True,defaults=defaults)

dispatcher = updater.dispatcher

SUDO_USERS = list(SUDO_USERS)


