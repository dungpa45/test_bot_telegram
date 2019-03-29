from telegram.ext import Updater, CommandHandler, MessageHandler,Filters, InlineQueryHandler
mybots = {}



def sayhi(bot,job):
    job.context.message.reply_text("hi")
    # job = context.job
    # context.bot.send_message(job.context, text='HI')
def time(bot, update, job_queue):
    job_queue.run_repeating(sayhi, interval=5, context=update)

def main():
    updater = Updater("876374897:AAGL2K9-sUb_7mnVso8WddzlYn69_9bIsHg")
    #Lan3taobot
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text, time, pass_job_queue=True))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
