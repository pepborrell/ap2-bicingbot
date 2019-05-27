# importing the API
import telegram
from telegram.ext import Updater, CommandHandler

import os as os

# importing the functions that deal with the data
import data as dt

# declares an access token constant read from the token.txt file
TOKEN = open('token.txt').read().strip()

# creates objects needed to work with the API
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher


############# FUNCTIONS #############

def start(bot, update, user_data):
    name = update.message.chat.first_name
    bot.send_message(chat_id=update.message.chat_id, text='Hello %s!\n' % (name))
    missatge = '''
    I'm BicingBot, a bot to guide you in your daily cycling routes through across Barcelona.

    You can ask for /help, I'm always ready to help you.
    '''
    bot.send_message(chat_id=update.message.chat_id, text=missatge, parse_mode=telegram.ParseMode.MARKDOWN)

    d = 1000
    user_data['d'] = d
    user_data['G'], bicing, user_data['info'] = dt.build_graph(d)


def help(bot, update):
    info = '''
	These are the things that you can ask me to do:

    - /authors:
    - /graph <distance>
    - /nodes
    - /edges
    - /components
    - /plotgraph
    - /route <origin, destination>
    '''
    bot.send_message(chat_id=update.message.chat_id, text=info, parse_mode=telegram.ParseMode.MARKDOWN)

def authors(bot, update):
	info = '''
    The authors of this project are:

    - Josep Borrell Tatché: _josep.borrell@est.fib.upc.edu_
    - Mireia Cavallé Salvadó: _mireia.cavalle@est.fib.upc.edu_
    '''
	bot.send_message(chat_id=update.message.chat_id, text=info, parse_mode=telegram.ParseMode.MARKDOWN)

def graph(bot, update, user_data, args):
    try:
        d = float(args[0])
        user_data['d'] = d
        user_data['G'], bicing, user_data['info'] = dt.build_graph(d)
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text='💣Your command made me fail. Be kind to me. Please try again')

def nodes(bot, update, user_data):
    G = user_data['G']
    nnodes = dt.number_of_nodes(G)
    bot.send_message(chat_id=update.message.chat_id, text='There are currently %d working Bicing stations' % (nnodes))

def edges(bot, update, user_data):
    G = user_data['G']
    nedges = dt.number_of_edges(G)
    bot.send_message(chat_id=update.message.chat_id, text='There are currently %d edges in your graph' % (nedges))

def components(bot, update, user_data):
    G = user_data['G']
    nccomp = dt.number_of_connected_components(G)
    bot.send_message(chat_id=update.message.chat_id, text='There are currently %d connected components in your graph' % (nccomp))

def plotgraph(bot, update, user_data):
    filename = str(update.message.chat.username) + '.png'
    G = user_data['G']
    image = dt.plot_graph(G)
    image.save(filename)
    bot.send_photo(chat_id=update.message.chat_id, photo=open(filename, 'rb'))
    os.remove(filename)

def route(bot, update, user_data):
    miss_orig = update.message.text[7:]
    filename = str(update.message.chat.username) + '.png'
    image = dt.plot_route(miss_orig, user_data['G'], user_data['d'], user_data['info'])
    image.save(filename)
    bot.send_photo(chat_id=update.message.chat_id, photo=open(filename, 'rb'))
    os.remove(filename)


# assigns functions to their commands
dispatcher.add_handler(CommandHandler('start', start, pass_user_data=True))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler('authors', authors))
dispatcher.add_handler(CommandHandler('graph', graph, pass_user_data=True, pass_args=True))
dispatcher.add_handler(CommandHandler('nodes', nodes, pass_user_data=True))
dispatcher.add_handler(CommandHandler('edges', edges, pass_user_data=True))
dispatcher.add_handler(CommandHandler('components', components, pass_user_data=True))
dispatcher.add_handler(CommandHandler('plotgraph', plotgraph, pass_user_data=True))
dispatcher.add_handler(CommandHandler('route', route, pass_user_data=True))


# turns on bot
updater.start_polling()
updater.idle()
