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
    I'm BicingBot, a bot to guide you in your daily cycling routes across Barcelona.

    You can ask for /help, I'm always ready to help you.
    '''
    bot.send_message(chat_id=update.message.chat_id, text=missatge, parse_mode=telegram.ParseMode.MARKDOWN)

    try:
        d = 1000
        user_data['d'] = d
        user_data['G'], user_data['bicing'], user_data['info'] = dt.build_graph(d)
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text='An error occured. Please try again.')


def help(bot, update):
    info = '''
	These are the things that you can ask me to do:

    - /authors: I'll give you the names of my fantastic creators.
    - /graph <distance>: I'll build your particular graph with the maximum distance (in meters) between stations that you prefer. By default, your graph is built with a distance of 1000 m.
    - /nodes: This commands gives you the number of working bicing stations in Barcelona.
    - /edges: The number of edges there are in your graph.
    - /components: The number of connected components in the graph that you've asked me to build.
    - /plotgraph: I will plot the graph in a map and show it to you.
    - /route <origin, destination>: If you ask me to give you a route between two places, I will find the fastest one for you! You will maybe need to walk and then take a bike. Attention: the directions must be given separated by a comma.
    - /distribute <required bikes, required docks>: I will attempt to reorganise the bicycles so there are at least the number of required bikes and docks that you give me in every station. The input must be separated by spaces.
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
    try:
        nnodes = dt.number_of_nodes(G)
        bot.send_message(chat_id=update.message.chat_id, text='There are currently %d working Bicing stations' % (nnodes))
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text='An error occured. Please try again.')

def edges(bot, update, user_data):
    G = user_data['G']
    try:
        nedges = dt.number_of_edges(G)
        bot.send_message(chat_id=update.message.chat_id, text='There are currently %d edges in your graph' % (nedges))
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text='An error occured. Please try again.')

def components(bot, update, user_data):
    G = user_data['G']
    try:
        nccomp = dt.number_of_connected_components(G)
        bot.send_message(chat_id=update.message.chat_id, text='There are currently %d connected components in your graph' % (nccomp))
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text='An error occured. Please try again.')

def plotgraph(bot, update, user_data):
    filename = str(update.message.chat.username) + '.png'
    G = user_data['G']
    try:
        image = dt.plot_graph(G)
        image.save(filename)
        bot.send_photo(chat_id=update.message.chat_id, photo=open(filename, 'rb'))
        os.remove(filename)
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text='An error occured. Please try again.')

def route(bot, update, user_data):
    miss_orig = update.message.text[7:]
    filename = str(update.message.chat.username) + '.png'
    try:
        image = dt.plot_route(miss_orig, user_data['G'], user_data['d'], user_data['info'])
        image.save(filename)
        bot.send_photo(chat_id=update.message.chat_id, photo=open(filename, 'rb'))
        os.remove(filename)
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text='An error occured. Please try again.')

def distribute(bot, update, user_data, args):
    try:
        dt.distribute(user_data['G'], user_data['d'], user_data['bicing'], args[0], args[1])
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text='An error occured. Please try again.')


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
dispatcher.add_handler(CommandHandler('distribute', distribute, pass_user_data=True, pass_args=True))


# turns on bot
updater.start_polling()
updater.idle()
