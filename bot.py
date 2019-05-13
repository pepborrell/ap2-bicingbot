# importing the API
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler

# importing the functions that deal with the data
import data as dt

# declares an access token constant read from the token.txt file
TOKEN = open('token.txt').read().strip()

# creates objects needed to work with the API
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

############# FUNCTIONS #############

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='This is a test bot!')


# assigns functions to their commands
dispatcher.add_handler(CommandHandler('start', start))

# turns on bot
updater.start_polling()
