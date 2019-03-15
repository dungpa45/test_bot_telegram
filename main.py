from telegram.ext import Updater, CommandHandler
import requests
import re

def get_url():
    # Access the API and get the image URL
    contents = requests.get('https://random.dog/woof.json').json()
    #Get the image URL since we need that parameter to be able to send the image.
    image_url = contents['url']
    return image_url

# iterate the URL until we get the file extension that we want
def get_image_url():
    allowed_extension = ['jpg', 'jpeg', 'png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url()
        file_extension = re.search("([^.]*)$", url).group(1).lower()
    return url

def dog(bot,update):
    url = get_image_url()
    #Get the recipient’s ID
    chat_id = update.message.chat_id
    #it’s time to send the message, which is an image.
    bot.send_photo(chat_id=chat_id, photo=url)

def main():
    updater = Updater('754452513:AAFOY_HfYO8dlX8i-R5wE2bjpr3N4i7_3a4')
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('dog',dog))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
