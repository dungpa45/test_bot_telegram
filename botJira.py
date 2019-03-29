from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext import Filters, InlineQueryHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent, ReplyKeyboardMarkup
import requests,re,os
from jira import JIRA

#Ket noi den Jira
jira_server = 'https://osamers.atlassian.net'

jira_servers = {'server': jira_server}

jira = JIRA(options=jira_servers, basic_auth=(
    'dphamanh45@gmail.com', 'dung4597'))


def start(update,context):
    # user =update.message.from_user
    update.message.reply_text("Hello \nType /check to check DOD from Jira")

def check(update,context):
    #Truy van data bang JQL
    search = jira.search_issues(
        'DOD is EMPTY AND status != Done AND status != "To Do" AND Sprint in (89, 105) ORDER BY priority DESC', maxResults=50)
    so_task = len(search)
    dic ={}
    ls_status=[]
    stt=0

    if len(search) == 0:
        update.message.reply_text("Tasks already have DOD")
    else:
        update.message.reply_text("Number of task missing DOD: {}".format(so_task))
        for iss in search:
            tieude = iss.fields.summary
            ten = iss.fields.reporter.displayName
            trangthai = iss.fields.status.name
            dic[tieude]= ten
            ls_status.append(trangthai)
        # print(dic)
        #Chuyen tu dic sang list roi thanh string
        k = []
        index = 0
        for j in dic:
            stt += 1
            k.append(str(stt)+': '+j + ' - ' + dic[j] + ' - ' + ls_status[index])
            index += 1
        z = " \n".join(k)
        # print(z)
        # update.message.reply_text("{}: {} - {}".format(stt,tieude,ten))
        #Hien thi inline url
        keyboard = []
        keyboard.append([InlineKeyboardButton(
            'Check it out', url='https://osamers.atlassian.net/issues/?jql=DOD%20is%20EMPTY%20AND%20status%20!%3D%20Done%20AND%20status%20!%3D%20%22To%20Do%22%20AND%20Sprint%20in%20(89%2C%20105)%20ORDER%20BY%20priority%20DESC')])

        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text("{}".format(z), reply_markup=reply_markup)


def main():
    updater = Updater(
        "861699291:AAGio3CTexwKDtJw-EBR_AoeSUE4_ms5lEU", use_context=True)
        #Lan2taoBot
    dp =updater.dispatcher
    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(CommandHandler('check',check,pass_args=False))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
