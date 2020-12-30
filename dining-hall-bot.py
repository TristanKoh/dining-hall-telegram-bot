import logging
import os
from telegram.ext import Updater, CommandHandler

import requests
from bs4 import BeautifulSoup

import threading
import schedule
import time

# For managing the daily updates
STOP_THREADS = False
UPDATE_SET = False

# Variables for tele bot to run
PORT = int(os.environ.get('PORT', '8443'))
TOKEN = ""
APP_NAME = "https://dining-hall-bot.herokuapp.com/"

# Dining hall menu link
DH_LINK = "https://studentlife.yale-nus.edu.sg/dining-experience/daily-dining-menu/"


# Function to pull the menu and then format the menu for the day
# TODO: Ideally the bot should only pull once a week, but the parsing would be more difficult getting "today's" menu
# would require conversion from UTC to SGT, and a separate thread to query the time constantly


def formatMenu(day) :
    """ 
    Accepts a int day (day of week) (ie. 1 for mon, 2 for tues etc)
    Queries the dining hall page and returns a formatted string for bot to use to reply 
    """

    # Get the html from the webpage
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66'}
    r = requests.get(DH_LINK, headers = headers)
    soup = BeautifulSoup(r.text, "html.parser")

    day_to_tab_dict = {1 : "tab1", 2 : "tab2", 3 : "tab3", 4 : "tab4", 5 : "tab5", 6 : "tab6", 7 : "tab7"}

    menu = ""
    meals = soup.find("div", {"id" : day_to_tab_dict[day]}).findAll(class_ = "menu-list")


    # If day is not weekend
    if day != 6 or day != 7 :

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


def formatMenu_Today() :
    """ 
    No arguments. Functionally same as the formatMenu function above.
    Queries the webpage, finds the active DH tab (which indicates that it is today's menu), 
    Pulls the text from that tab and formats it for the bot to reply
    """

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66'}
    r = requests.get(DH_LINK, headers = headers)
    soup = BeautifulSoup(r.text, "html.parser")

    today_tab = soup.find(class_ = "tabs dining").find(class_ =  "active").get("rel")

    # Extract fourth char of tab string (ie. tab4 returns 4), since that is the day of week
    day = int(today_tab[3])

    day_to_tab_dict = {1 : "tab1", 2 : "tab2", 3 : "tab3", 4 : "tab4", 5 : "tab5", 6 : "tab6", 7 : "tab7"}

    menu = ""
    meals = soup.find("div", {"id" : day_to_tab_dict[day]}).findAll(class_ = "menu-list")

    if day != 6 or day != 7 :

        for index in range(3) :

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
    update.message.reply_text(""" 
    Hello! \n
    To display the dining menu, type /[day of week]. For example, /mon displays the Monday menu. \n
    To schedule the bot to send you the day's menu at 6am every day, use /dailyupdate. \n
    To unschedule the daily update, use /stopupdate. \n
    """)

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text("""
    Hello! \n
    To display the dining menu, type /[day of week]. For example, /mon displays the Monday menu. \n
    To schedule the bot to send you the day's menu at 6am every day, use /dailyupdate. \n
    To unschedule the daily update, use /stopupdate. \n
    """)


# Get the relevant day's menu, depending on the user input
def getMon(update, context) :
    """ Gets the menu for the day """    
    update.message.reply_text(formatMenu(1), parse_mode = "HTML")

def getTues(update, context) :
    """ Gets the menu for the day """
    update.message.reply_text(formatMenu(2), parse_mode = "HTML")

def getWed(update, context) :
    """ Gets the menu for the day """
    update.message.reply_text(formatMenu(3), parse_mode = "HTML")

def getThurs(update, context) :
    """ Gets the menu for the day """
    update.message.reply_text(formatMenu(4), parse_mode = "HTML")

def getFri(update, context) :
    """ Gets the menu for the day """
    update.message.reply_text(formatMenu(5), parse_mode = "HTML")

def getSat(update, context) :
    """ Gets the menu for the day """
    update.message.reply_text(formatMenu(6), parse_mode = "HTML")

def getSun(update, context) :
    """ Gets the menu for the day """
    update.message.reply_text(formatMenu(7), parse_mode = "HTML")

def getToday(update, context) :
    """ Gets the menu for the day """    
    update.message.reply_text(formatMenu_Today(), parse_mode = "HTML")


# Set scheduler for today's menu at 6am (UTC time is behind SGT by 8 hours)
def set_schedule(update, context) :
    schedule.every(1).minute.do(getToday, update, context)
    # schedule.every().day.at("20:00").do(getToday, update, context)


# Auxilliary functions to run scheduler in threaded mode
def run_jobs(update, context) :
    
    set_schedule(update, context)
    global STOP_THREADS

    while True :
        if STOP_THREADS == True :
            break 

        else :
            schedule.run_pending()
            
            # TODO: Figure out delay to loop the check. Factor in server sleep time?
            time.sleep(50)


# TODO: Threading does not stop when process is shut down: Thread as daemon process?
def run_threads(update, context) :
    
    global UPDATE_SET

    if UPDATE_SET == False :
        th = threading.Thread(target=run_jobs, args = (update, context, ))
        th.start()
        UPDATE_SET = True 
        update.message.reply_text("Menu update scheduled for 6am daily")
    
    elif UPDATE_SET == True :
        update.message.reply_text("Error: Menu update already scheduled for 6am daily!")


def stop_update(update, context):
    global STOP_THREADS
    STOP_THREADS = True

    update.message.reply_text("Menu update unscheduled")


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

    dp.add_handler(CommandHandler("Today", getToday))
    dp.add_handler(CommandHandler("Mon", getMon))
    dp.add_handler(CommandHandler("Tues", getTues))
    dp.add_handler(CommandHandler("Wed", getWed))
    dp.add_handler(CommandHandler("Thurs", getThurs))
    dp.add_handler(CommandHandler("Fri", getFri))
    dp.add_handler(CommandHandler("Sat", getSat))
    dp.add_handler(CommandHandler("Sun", getSun))

    # Set daily updates
    dp.add_handler(CommandHandler("dailyupdate", run_threads))
    dp.add_handler(CommandHandler("stopupdate", stop_update))
    
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot (polling method)
    updater.start_polling()

    # Webhook method
    # NOTE: Change to webhook method when deploying
    # updater.start_webhook(listen = "0.0.0.0", port = PORT, url_path = TOKEN)
    # updater.bot.set_webhook(APP_NAME + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()