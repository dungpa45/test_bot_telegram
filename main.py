from telegram.ext import Updater ,CommandHandler, InlineQueryHandler, MessageHandler, Filters, ConversationHandler, RegexHandler
import requests, re, os
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, ReplyKeyboardMarkup



reply_keboard = [['/dog','/cat'],['Start count','Done']]
markup = ReplyKeyboardMarkup(reply_keboard,one_time_keyboard=True)

CHOOSE = 1

def get_url():
    # Access the API and get the image URL
    contents = requests.get('https://random.dog/woof.json').json()
    #Get the image URL since we need that parameter to be able to send the image.
    image_url = contents['url']
    return image_url

def get_url1():
    # Access the API and get the image URL
    contents1 = requests.get('http://aws.random.cat/meow').json()
    #Get the image URL since we need that parameter to be able to send the image.
    image_file = contents1['file']
    return image_file


# iterate the URL until we get the file extension that we want
def get_image_url():
    allowed_extension = ['jpg', 'JPG', 'jpeg', 'png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url()
        
        file_extension = re.search("([^.]*)$", url).group(1).lower()
    return url 

def get_image_url1():
    allowed_extension = ['jpg', 'JPG', 'jpeg', 'png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url1 = get_url1()
        
        file_extension = re.search("([^.]*)$", url1).group(1).lower()
    return url1 

def start(bot,update):
    user = update.message.from_user
    update.message.reply_text(
        "Hello master {} \nType /dog or /cat to see random picture\nType some text".format(user.full_name),reply_markup=markup)
    # update.message.reply_text("Type /dog or /cat to see random picture")
    
def convert_uppercase(bot ,update):
    update.message.reply_text(update.message.text.upper())

def convert_lowercase(bot ,update):
    update.message.reply_text(update.message.text.lower())

def dog(bot,update):
    url = get_image_url()
    #Get the recipient’s ID
    chat_id = update.message.chat_id
    #it’s time to send the message, which is an image.
    bot.send_photo(chat_id=chat_id, photo=url)

# print(dog(,get_image_url()))
def cat(bot1,update1):
    url1 = get_image_url1()
    chat_id = update1.message.chat_id
    bot1.send_photo(chat_id=chat_id, photo=url1)

def sayhi(bot, job):
    job.context.message.reply_text("Message auto send each 5 minutes")

def time(bot, update, job_queue):
    job_queue.run_repeating(sayhi, 300, context=update)

def done(update,context):
    
    update.message.reply_text('Stop counting')
    return ConversationHandler.END

def main():
    TOKEN = "754452513:AAFOY_HfYO8dlX8i-R5wE2bjpr3N4i7_3a4"
    # PORT = int(os.environ.get('PORT', '8443'))
    updater = Updater(TOKEN)

    conv_handler = ConversationHandler(
        entry_points = [CommandHandler('start',start)],
        states={
            CHOOSE:[RegexHandler('^Start count$',sayhi,pass_chat_data=True),
                    RegexHandler('^/dog$',dog,pass_chat_data=True),
                    RegexHandler('^/cat$',cat,pass_chat_data=True),
                    ],

        },
        fallbacks=[RegexHandler('^Done$', done, pass_chat_data=True)]
    )
    
    dp = updater.dispatcher
    # upper_case = MessageHandler(Filters.text, convert_uppercase)
    # lower_case = MessageHandler(Filters.text, convert_lowercase)
    dp.add_handler(MessageHandler(Filters.text, time, pass_job_queue=True))
    start_handler = CommandHandler('start',start)
    dp.add_handler(CommandHandler('dog',dog))
    dp.add_handler(CommandHandler('cat',cat))
    dp.add_handler(start_handler)
    # dp.add_handler(lower_case)
    # dp.add_handler(upper_case)
    dp.add_handler(conv_handler)
    #start the bot
    updater.start_polling()
    #Run the bot until press ctrl +C
    updater.idle()
    
if __name__ == '__main__':
    main()
   
