import logging
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
from bs4 import BeautifulSoup

PORT = int(os.environ.get('PORT', '8443'))
TOKEN = ""
APP_NAME = "https://dining-hall-bot.herokuapp.com/"

# Get the html from the webpage
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66'}
r = requests.get("https://studentlife.yale-nus.edu.sg/dining-experience/daily-dining-menu/", headers = headers)
soup = BeautifulSoup(r.text, "html.parser")

# Function to format the menu for the day
def formatMenu(meals, weekend = False) :
    """ 
    Accepts a soup object (meals) for the menu of the day and optional bool argument for weekend (since there are only two meals for weekends), 
    returns a formatted string for bot to reply 
    """
    
    menu = ""

    if weekend == False :
        # Loop through breakfast, lunch & dinner
        for index in range(3) :

            # Bold the meal text
            menu = menu + "<b>" + meals[index].find("h4").get_text() + "</b>" + "\n"
            
            # Find the stations (ie. salad bar, yakimix etc.) and the dishes (ie. kung pao chicken etc)
            stations = meals[index].findAll("strong")
            dishes = meals[index].findAll("td")

            # Convert to text 
            stations = [station.get_text() for station in stations]
            dishes = [dish.get_text() for dish in dishes]

            # Format the dishes
            for dish in dishes :

                # If dish is station name, print dish text with underline
                if dish in stations :
                    menu = menu + "<u>" + dish + "</u>" + "\n"
                
                else :
                    menu = menu + dish + "\n"
            
            # Add new lines to separate the meals from another
            menu = menu + "\n" + "\n"
        
        return menu
    
    else :
        for index in range(2) :

            menu = menu + "<b>" + meals[index].find("h4").get_text() + "</b>" + "\n"
            
            stations = meals[index].findAll("strong")
            dishes = meals[index].findAll("td")

            stations = [station.get_text() for station in stations]
            dishes = [dish.get_text() for dish in dishes]

            for dish in dishes :

                if dish in stations :
                    menu = menu + "<u>" + dish + "</u>" + "\n"
                
                else :
                    menu = menu + dish + "\n"
            
            menu = menu + "\n" + "\n"
        
        return menu


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)



# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hello! To display the dining menu, type /[day of week]. For example, /mon displays the Monday menu.')

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Hello! To display the dining menu, type /[day of week]. For example, /mon displays the Monday menu.')


# Get the relevant day's menu, depending on the user input

# def getToday(update, context) :
#     """ Gets the menu for the day """
#     update.message.reply_text(formatMenu(soup.find("div", {"id" : "tab_na"}).findAll(class_ = "menu-list")), parse_mode = "HTML")

def getMon(update, context) :
    """ Gets the menu for the day """    
    update.message.reply_text(formatMenu(soup.find("div", {"id" : "tab1"}).findAll(class_ = "menu-list")), parse_mode = "HTML")

def getTues(update, context) :
    """ Gets the menu for the day """
    update.message.reply_text(formatMenu(soup.find("div", {"id" : "tab2"}).findAll(class_ = "menu-list")), parse_mode = "HTML")

def getWed(update, context) :
    """ Gets the menu for the day """
    update.message.reply_text(formatMenu(soup.find("div", {"id" : "tab3"}).findAll(class_ = "menu-list")), parse_mode = "HTML")

def getThurs(update, context) :
    """ Gets the menu for the day """
    update.message.reply_text(formatMenu(soup.find("div", {"id" : "tab4"}).findAll(class_ = "menu-list")), parse_mode = "HTML")

def getFri(update, context) :
    """ Gets the menu for the day """
    update.message.reply_text(formatMenu(soup.find("div", {"id" : "tab5"}).findAll(class_ = "menu-list")), parse_mode = "HTML")

def getSat(update, context) :
    """ Gets the menu for the day """
    update.message.reply_text(formatMenu(soup.find("div", {"id" : "tab6"}).findAll(class_ = "menu-list"), weekend = True), parse_mode = "HTML")

def getSun(update, context) :
    """ Gets the menu for the day """
    update.message.reply_text(formatMenu(soup.find("div", {"id" : "tab7"}).findAll(class_ = "menu-list"), weekend = True), parse_mode = "HTML")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # dp.add_handler(CommandHandler("Today", getToday))
    dp.add_handler(CommandHandler("Mon", getMon))
    dp.add_handler(CommandHandler("Tues", getTues))
    dp.add_handler(CommandHandler("Wed", getWed))
    dp.add_handler(CommandHandler("Thurs", getThurs))
    dp.add_handler(CommandHandler("Fri", getFri))
    dp.add_handler(CommandHandler("Sat", getSat))
    dp.add_handler(CommandHandler("Sun", getSun))

    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen = "0.0.0.0", port = PORT, url_path = TOKEN)
    updater.bot.set_webhook(APP_NAME + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()