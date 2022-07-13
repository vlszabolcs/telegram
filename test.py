#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import keys
import logging

from matplotlib.cbook import file_requires_unicode
import csv_to_gpx
import os


from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)



# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )

def downloader(update, context):
    global file_in
    file_in=context.bot.get_file(update.message.document.file_id).download(update.message.document.file_name)

    
    if file_in != "" and file_in[-3:]=="csv":
       send_text_message(file_in+" fodadva! /original , /original_alti vagy /modify ?",update,context)
    else:
        send_text_message(file_in+" nem .CSV file!",update,context)
    
    return  file_in

def send_document(send_file,update:Update, context:CallbackContext,):
    chat_id = update.message.chat_id
    document = open(send_file, 'rb')
    send_text_message(send_file+" elkészült!",update,context)
    context.bot.send_document(chat_id, document)


def original_gpx(update,context):
        status=csv_to_gpx.csv_to_gpx_original(str(file_in))
        send_document(status,update, context )
        os.remove(file_in)
        os.remove(status)

def original_alti_gpx(update, context):
    status=csv_to_gpx.csv_to_gpx_alti(str(file_in))
    send_document(status,update, context )
    os.remove(file_in)
    os.remove(status)


def modify_gpx(update, context):
    update.message.reply_text("EZ még nincs kész")


    



def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def send_text_message(send_message,update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(send_message)



    
def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(keys.telegram_key)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.document, downloader))
    dispatcher.add_handler(CommandHandler("original",original_gpx))
    dispatcher.add_handler(CommandHandler("original_alti",original_alti_gpx))
    dispatcher.add_handler(CommandHandler("modify",modify_gpx ))
    

    # on non command i.e message - echo the message on Telegram
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    print(echo_handler)
    dispatcher.add_handler(echo_handler)
   
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()