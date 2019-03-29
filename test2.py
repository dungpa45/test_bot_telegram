# import logging
# from telegram import ReplyKeyboardMarkup
# from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
#                           ConversationHandler)

# # Enable logging
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     level=logging.INFO)

# logger = logging.getLogger(__name__)

# CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

# reply_keyboard = [['Age', 'Favourite colour'],
#                   ['Number of siblings', 'Something else...'],
#                   ['Done']]
# markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


# def facts_to_str(user_data):
#     facts = list()

#     for key, value in user_data.items():
#         facts.append('{} - {}'.format(key, value))

#     return "\n".join(facts).join(['\n', '\n'])


# def start(update, context):
#     update.message.reply_text(
#         "Hi! My name is Doctor Botter. I will hold a more complex conversation with you. "
#         "Why don't you tell me something about yourself?",
#         reply_markup=markup)

#     return CHOOSING


# def regular_choice(update, context):
#     text = update.message.text
#     context.user_data['choice'] = text
#     update.message.reply_text(
#         'Your {}? Yes, I would love to hear about that!'.format(text.lower()))

#     return TYPING_REPLY


# def custom_choice(update, context):
#     update.message.reply_text('Alright, please send me the category first, '
#                               'for example "Most impressive skill"')

#     return TYPING_CHOICE


# def received_information(update, context):
#     user_data = context.user_data
#     text = update.message.text
#     category = user_data['choice']
#     user_data[category] = text
#     del user_data['choice']

#     update.message.reply_text("Neat! Just so you know, this is what you already told me:"
#                               "{}"
#                               "You can tell me more, or change your opinion on something.".format(
#                                   facts_to_str(user_data)), reply_markup=markup)

#     return CHOOSING

# def done(update, context):
#     user_data = context.user_data
#     if 'choice' in user_data:
#         del user_data['choice']

#     update.message.reply_text("I learned these facts about you:"
#                               "{}"
#                               "Until next time!".format(facts_to_str(user_data)))

#     user_data.clear()
#     return ConversationHandler.END


# def error(update, context):
#     """Log Errors caused by Updates."""
#     logger.warning('Update "%s" caused error "%s"', update, error)


# def main():
#     updater = Updater(
#         "861699291:AAGio3CTexwKDtJw-EBR_AoeSUE4_ms5lEU", use_context=True)
#     # Get the dispatcher to register handlers
#     dp = updater.dispatcher
#     # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
#     conv_handler = ConversationHandler(
#         entry_points=[CommandHandler('start', start)],

#         states={
#             CHOOSING: [RegexHandler('^(Age|Favourite colour|Number of siblings)$',
#                                     regular_choice,
#                                     pass_user_data=True),
#                        RegexHandler('^Something else...$',
#                                     custom_choice),
#                        ],

#             TYPING_CHOICE: [MessageHandler(Filters.text,
#                                            regular_choice,
#                                            pass_user_data=True),
#                             ],

#             TYPING_REPLY: [MessageHandler(Filters.text,
#                                           received_information,
#                                           pass_user_data=True),
#                            ],
#         },
#         fallbacks=[RegexHandler('^Done$', done, pass_user_data=True)]
#     )
#     dp.add_handler(conv_handler)
#     # log all errors
#     dp.add_error_handler(error)
#     # Start the Bot
#     updater.start_polling()
#     updater.idle()


# if __name__ == '__main__':
#     main()

###############################
###############################
###############################

import logging

from telegram.ext import Updater, CommandHandler

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    update.message.reply_text('Hi! Use /set <seconds> to set a timer')

def alarm(context):
    """Send the alarm message."""
    job = context.job
    context.bot.send_message(job.context, text='Beep!')

def set_timer(update, context):
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        due = int(context.args[0])
        if due < 0:
            update.message.reply_text('Sorry we can not go back to future!')
            return
        # Add job to queue
        job = context.job_queue.run_once(alarm, due, context=chat_id)
        context.chat_data['job'] = job

        update.message.reply_text('Timer successfully set!')

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set <seconds>')

def unset(update, context):
    """Remove the job if the user changed their mind."""
    if 'job' not in context.chat_data:
        update.message.reply_text('You have no active timer')
        return
        
    job = context.chat_data['job']
    job.schedule_removal()
    del context.chat_data['job']

    update.message.reply_text('Timer successfully unset!')

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Run bot."""
    updater = Updater(
        "861699291:AAGio3CTexwKDtJw-EBR_AoeSUE4_ms5lEU", use_context=True)
        # '''Lan2taoBot'''
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", start))
    dp.add_handler(CommandHandler("set", set_timer,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))
    dp.add_handler(CommandHandler("unset", unset, pass_chat_data=True))
    # log all errors
    dp.add_error_handler(error)
    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
