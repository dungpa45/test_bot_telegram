import Response as R
# from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import json
import sys
sys.path.append('Method')
import os
import News
from yaml import Loader
from yaml import load

absolutepath = os.path.abspath(__file__)
fileDirectory = os.path.dirname(absolutepath)
print(fileDirectory)
with open(fileDirectory+"/secret.yaml","r") as yml_file:
    data = load(yml_file, Loader=Loader)

print("Bot Starting....")

def start_command(bot, update):
    update.message.reply_text(f'Chào {update.effective_user.first_name}')

def help_command(bot, update):
    update.message.reply_text("Bạn muốn tôi giúp gì? \n 1. Đọc báo -> /news <số lượng>")

def news_command(bot,update):
    print("ok")
    try:
        user_text = update.message.text
        input_num = user_text.split(" ") 
        limit_news = int(input_num[1]) # Lấy tham số từ input truyền vào -> cào về bao nhiêu tin
        print(limit_news)
        news = News.GetNews(limit_news)
        print('news',news)
        for x in range(0, len(news)): # Deserialize dữ liệu json trả về từ file News.py lúc nãy
            message = json.loads(news[x])
            print(message)
            update.message.reply_text(message['title'] + "\n" 
                + message['link'] + "\n" + message['description'])
    except (IndexError, ValueError):
        update.message.reply_text('Vui lòng chọn số lượng tin hiển thị!!')

def handle_message(bot,update):
    text = str(update.message.text).lower()
    response = R.sample_response(text)
    update.message.reply_text(response)

 # Function dùng để xác định lỗi gì khi có thông báo lỗi
def error(bot,update):
    print(f"Update {update} cause error {context.error}")

def main():
    TOKEN = data["telegram"]["token_quote"]
    updater = Updater(token=TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("news", news_command))
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

main()
