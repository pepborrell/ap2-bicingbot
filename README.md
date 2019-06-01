---
output:
  html_document: default
  pdf_document: default
---
# AP2-bicingbot
AP2 project. Telegram's bot for Bicing.

The present Telegram's bot _Inflitrats_BicingBot_ answers textually and graphically (using maps) questions about geometric graphs representing the bicing stations in Barcelona.

##Architecture
The bot has been constitued around a 
```
Graph
``` type object from 
```
NetworkX
``` library and it has two modules:

*
```
data.py
``` which contains all the commands to acquire the bicing data, to build the graph and to calculate some interesting features.

*
```
bot.py
``` which includes all the commands related to the Telegram's Bot implementation.

##Getting started
The following instructions try to guide you on how to install and make use of the bicingbot.

###Prerequisites
You will find the libraries needed at the requirements.txt file attached in the folder.

###Installing
To install the libraries metioned, you need to compute the following commands:

```{r}
pip install pandas
pip install networkx
pip install haversine
pip install geopy
pip install staticmap
pip install python-telegram-bot==10
```

To be able to make use of the bicingbot, you have to install the application Telegram on your mobile phone or computer and sign up or log in (in case you already have an account).

##Running the tests
To access to the bicingbot created you just need to follow the following link.

[Infiltrats_BicingBot](https://t.me/InfiltratsBicingBot)

To start talking with our bicingbot you just need to send him:
```{r}
/start
```

After that, you can follow the displayed link
```
/help
``` to see all the possible commands you can obtain from the bot.
Read carefully the specifications given so that bot doesn't get disturbed! 🔎

##Authors
* Josep Borrell Tatché: _<josep.borrell@est.fib.upc.edu>_
* Mireia Cavallé Salvadó: _<mireia.cavalle@est.fib.upc.edu>_

##Acknowledgments
Thanks to [Jordi Petit](https://github.com/jordi-petit) and [Jordi Cortadella](https://github.com/jordicf?tab=stars) for offering us part of the code.