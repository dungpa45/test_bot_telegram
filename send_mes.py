import logging
from telegram import InlineQueryResultArticle, ParseMode, \
    InputTextMessageContent, ReplyKeyboardMarkup
from telegram.ext import Updater, InlineQueryHandler, CommandHandler,\
    MessageHandler, Filters, RegexHandler,ConversationHandler

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSE,TYPE_REPLY,TYPE_CHOICE = range(3)

reply_keyboard = [
    ['Name', 'Age', 'Country'],
    ['Number of child','Something else...'],
    ['Done ']
]
markup = ReplyKeyboardMarkup(reply_keyboard,one_time_keyboard=True)

def fact_to_str(user_data):
    fact = list()
    for key, value in user_data.items():
        fact.append('{} - {}'.format(key,value))
    return '\n'.join(fact).join(['\n','\n'])

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi! \nTell me somthing about yourself :)'
        ,reply_markup=markup)
    return CHOOSE

def regular_choice(update,context):
    text = update.message.text
    context.user_data['choice']=text
    update.message.reply_text('Your {}? Yes, I want to hear about that'.format(text.lower()))
    return TYPE_REPLY

def custom_choice(update,context):
    update.message.reply_text('Send me something \nexample "Damn Sonnn"')
    return TYPE_CHOICE

def recieve_info(update, context):
    user_data = context.user_data
    text = update.message.text
    category = user_data['choice']
    user_data[category]=text
    del user_data['choice']

    update.message.reply_text("this is what you already told me:"
    "{}"
    "U can change your opinion".format(fact_to_str(user_data)),reply_markup=markup)

    return CHOOSE

def done(update,context):
    user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']
    
    update.message.reply_text("There are facts about you"
    "{}"
    "Bye ahihi :))".format(fact_to_str(user_data)))
    user_data.clear()
    return ConversationHandler.END

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    updater = Updater(
        "876374897:AAGL2K9-sUb_7mnVso8WddzlYn69_9bIsHg", use_context=True)
    '''Lan3taobot'''
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start',start)],
        states={
            CHOOSE: [RegexHandler('^(Name|Age|Country|Number of child)$',
                                  regular_choice,
                                  pass_user_data=True),
                     RegexHandler('^Something else...$',
                                  custom_choice),
                     ],

            TYPE_CHOICE:[MessageHandler(Filters.text,
                                        regular_choice,
                                        pass_chat_data=True),
            ],

            TYPE_REPLY: [MessageHandler(Filters.text,
                                        recieve_info,
                                        pass_chat_data=True),
            ],

        },
        fallbacks=[RegexHandler('^Done$',done,pass_chat_data=True)]
    )

    dp.add_handler(CommandHandler("help", help))

    dp.add_handler(conv_handler)
    # log all errors
    dp.add_error_handler(error)
    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

# ############################################################
# ############################################################
# ############################################################
##########################################
##########################################

# import logging

# from telegram.ext import Updater, CommandHandler

# # Enable logging
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     level=logging.INFO)

# logger = logging.getLogger(__name__)


# # Define a few command handlers. These usually take the two arguments bot and
# # update. Error handlers also receive the raised TelegramError object in error.
# def start(update, context):
#     update.message.reply_text('Hi! Use /set <seconds> to set a timer')

# def alarm(context):
#     """Send the alarm message."""
#     job = context.job
#     context.bot.send_message(job.context, text='Beep!')

# def set_timer(update, context):
#     """Add a job to the queue."""
#     chat_id = update.message.chat_id
#     try:
#         # args[0] should contain the time for the timer in seconds
#         due = int(context.args[0])
#         if due < 0:
#             update.message.reply_text('Sorry we can not go back to future!')
#             return
#         # Add job to queue
#         job = context.job_queue.run_once(alarm, due, context=chat_id)
#         context.chat_data['job'] = job

#         update.message.reply_text('Timer successfully set!')

#     except (IndexError, ValueError):
#         update.message.reply_text('Usage: /set <seconds>')

# def unset(update, context):
#     """Remove the job if the user changed their mind."""
#     if 'job' not in context.chat_data:
#         update.message.reply_text('You have no active timer')
#         return

#     job = context.chat_data['job']
#     job.schedule_removal()
#     del context.chat_data['job']

#     update.message.reply_text('Timer successfully unset!')

# def error(update, context):
#     """Log Errors caused by Updates."""
#     logger.warning('Update "%s" caused error "%s"', update, context.error)

# def main():
#     """Run bot."""
#     # Create the Updater and pass it your bot's token.
#     # Make sure to set use_context=True to use the new context based callbacks
#     # Post version 12 this will no longer be necessary
#     updater = Updater(
#         "861699291:AAGio3CTexwKDtJw-EBR_AoeSUE4_ms5lEU", use_context=True)

#     # Get the dispatcher to register handlers
#     dp = updater.dispatcher

#     # on different commands - answer in Telegram
#     dp.add_handler(CommandHandler("start", start))
#     dp.add_handler(CommandHandler("help", start))
#     dp.add_handler(CommandHandler("set", set_timer,
#                                   pass_args=True,
#                                   pass_job_queue=True,
#                                   pass_chat_data=True))
#     dp.add_handler(CommandHandler("unset", unset, pass_chat_data=True))

#     # log all errors
#     dp.add_error_handler(error)

#     # Start the Bot
#     updater.start_polling()

#     updater.idle()


# if __name__ == '__main__':
#     main()
