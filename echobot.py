from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from flask import Flask
import logging
import datetime
import os
from wit import Wit
import db
from flask.ext.heroku import Heroku

# Wit.ai object initialization
client = Wit(access_token=os.environ["WIT_AI_API_KEY"])

app = Flask(__name__)
app.config['SECRET_KEY'] = "random string"
heroku = Heroku(app)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text('This bot are made by Luthfi Kurnia Putra')


def help(bot, update):
    update.message.reply_text('Yang bisa menolong skripsi anda hanyalah diri anda sendiri -LKP')

def echo(bot, update):
    resp = client.message(update.message.text)
    try:
        intent = str(resp['entities']['intent'][0]['value'])
        confidence = str(resp['entities']['intent'][0]['confidence'])
    except:
        intent = "no"
        confidence = 0.0

    now = datetime.datetime.now()
    deadline = datetime.datetime.now().replace(day=5, month=6, hour=23, minute=59)

    diff = deadline - now

    if intent == 'praise':
        update.message.reply_text("Makasih :)")
    elif intent == 'deadline':
        update.message.reply_text("Deadlinenya 5 Juni 2017. Jangan lupa ya ;)")
    elif intent == 'countdown':
        if diff.days >= 0:
            update.message.reply_text("Tinggal " + str(diff.days) + " hari lagi. Semangat ya! :)")
        else:
            update.message.reply_text("Udah lewat deadline :(")
    elif intent == 'quotes':
        update.message.reply_text("Masih ada semester depan :) \n \n-LKP")
    elif intent == 'insult':
        if confidence > 0.8:
            update.message.reply_text("Napa tot")
        else:
            update.message.reply_text("Kok kamu jahat ... :(")
    elif intent == 'dissapointment':
        update.message.reply_text("Semangat! hidup masih panjang :)")
    elif intent == 'greetings':
        update.message.reply_text("Haloo! \n \nHari yang cerah untuk revisi baru hari ini. Tetep semangat ya!")
    else:
        update.message.reply_text("Kamu ngomong apa sih :(")

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # For port binding and token
    TOKEN = os.environ['TELEGRAM_API_KEY']

    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN)

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

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

@app.route('/')  # the requests handled successfully!
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    main()
    PORT = int(os.environ.get('PORT', '5000'))

    app.run(host='0.0.0.0', port=PORT)
    while 1:
        time.sleep(10)
