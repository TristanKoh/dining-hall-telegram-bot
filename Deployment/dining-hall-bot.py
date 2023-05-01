import logging
import os
from telegram.ext import Updater, CommandHandler

import tokens.token

import requests
from bs4 import BeautifulSoup
from packages.menu import formatMenu, formatMenu_Today

import threading
import schedule
import time

# For managing the daily updates
STOP_THREADS = False
UPDATE_SET = False

# Variables for tele bot to run
PORT = int(os.environ.get('PORT', '8443'))
TOKEN = tokens.token.TOKEN
APP_NAME = "https://dining-hall-bot.herokuapp.com/"

# Dining hall menu link
DH_LINK = "https://studentlife.yale-nus.edu.sg/dining-experience/daily-dining-menu/"


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
    Or you can use /today or /tmr to show today's or tomorrow's menu.
    """)

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text("""
    Hello! \n
    To display the dining menu, type /[day of week]. For example, /mon displays the Monday menu. \n
    Or you can use /today or /tmr to show today's or tomorrow's menu.
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

def getTmr(update, context) :
    """ Gets the menu for the day """    
    update.message.reply_text(formatMenu_Today(tmr = True), parse_mode = "HTML")


# Set scheduler for today's menu at 6am (UTC time is behind SGT by 8 hours)
def set_schedule(update, context) :
    schedule.every().day.at("20:00").do(getToday, update, context)


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
            time.sleep(55)


def run_threads(update, context) :
    
    global UPDATE_SET

    if UPDATE_SET == False :
        th = threading.Thread(target=run_jobs, args = (update, context, ), daemon = True)
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
    dp.add_handler(CommandHandler("Tmr", getTmr))
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
    # updater.start_polling()

    # Webhook method
    # NOTE: Change to webhook method when deploying
    updater.start_webhook(listen = "0.0.0.0", port = PORT, url_path = TOKEN)
    updater.bot.set_webhook(APP_NAME + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()