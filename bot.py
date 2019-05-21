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

x = 's'

############# FUNCTIONS #############

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='This is a test bot!')

def help(bot, update):
    info = '''
	Aquí es pot escriure en MarkDown:

    - En *negreta*
    - En _cursiva_

    '''
    bot.send_message(chat_id=update.message.chat_id, text=info, parse_mode=telegram.ParseMode.MARKDOWN)

def authors(bot, update):
	info = 'Josep Borrell Tatché: josep.borrell@est.fib.upc.edu Mireia Cavallé Salvadó: mireia.cavalle@est.fib.upc.edu'
	bot.send_message(chat_id=update.message.chat_id, text=info, parse_mode=telegram.ParseMode.MARKDOWN)

def prova(bot, update, args):
    print(args[0])
    print(args[1])
    x = args[1]

def prova2(bot,update):
    bot.send_message(chat_id=update.message.chat_id, text=x, parse_mode=telegram.ParseMode.MARKDOWN)


'''
def graph(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='This is a test bot!')

def nodes(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='This is a test bot!')

def edges(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='This is a test bot!')

def components(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='This is a test bot!')

def plotgraph(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='This is a test bot!')

def route(bot, update):
	miss_orig = update.message.text[7:]

	image = plot_route(miss_orig, G, d, info)
	image.save('route.png')

    bot.send_message(chat_id=update.message.chat_id, text=miss_orig)
'''

# assigns functions to their commands
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler('authors', authors))
dispatcher.add_handler(CommandHandler('prova', prova, pass_args=True))
dispatcher.add_handler(CommandHandler('prova2', prova2))


# turns on bot
updater.start_polling()
