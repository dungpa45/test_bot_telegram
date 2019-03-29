import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    update.message.reply_text('Hi!\nType some text or icon, Bot will respond just like you type')

def help(update, context):
    update.message.reply_text('Help!')

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    '''Lan2taoBot'''
    updater = Updater(
        "861699291:AAGio3CTexwKDtJw-EBR_AoeSUE4_ms5lEU", use_context=True)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))
    # log all errors
    dp.add_error_handler(error)
    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

###########################################
###########################################
###########################################

# import logging
# import telegram
# from telegram.error import NetworkError, Unauthorized
# from time import sleep

# update_id = None


# def main():
#     """Run the bot."""
#     global update_id
#     # Telegram Bot Authorization Token
#     bot = telegram.Bot('861699291:AAGio3CTexwKDtJw-EBR_AoeSUE4_ms5lEU')
#     # get the first pending update_id, this is so we can skip over it in case
#     # we get an "Unauthorized" exception.
#     try:
#         update_id = bot.get_updates()[0].update_id
#     except IndexError:
#         update_id = None

#     logging.basicConfig(
#         format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

#     while True:
#         try:
#             echo(bot)
#         except NetworkError:
#             sleep(1)
#         except Unauthorized:
#             # The user has removed or blocked the bot.
#             update_id += 1


# def echo(bot):
#     """Echo the message the user sent."""
#     global update_id
#     # Request updates after the last update_id
#     for update in bot.get_updates(offset=update_id, timeout=10):
#         update_id = update.update_id + 1

#         if update.message:  # your bot can receive updates without messages
#             # Reply to the message
#             update.message.reply_text(update.message.text)


# if __name__ == '__main__':
#     main()
