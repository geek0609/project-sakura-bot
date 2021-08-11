#!/usr/bin/env python
#
# Copyright (C) 2021 Ashwin DS <astroashwin@outlook.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation;
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

import os
import random
import time
from telegram import *
from telegram.ext import *
import requests
import json
import texts, info

BOT_API = os.environ.get("BOT_API")

bot = Bot(BOT_API)
updater = Updater(BOT_API, use_context=True, workers=128)
dispatcher = updater.dispatcher
timeout = 60


def auto_delete(message_sent, update):
    if update.effective_chat.type == "supergroup" or update.effective_chat.type == "group":
        time.sleep(timeout)
        bot.deleteMessage(update.effective_chat.id, message_sent.message_id)
        bot.deleteMessage(update.effective_chat.id, update.message.message_id)


def start_fun(update: Update, context: CallbackContext):
    message_sent = bot.send_message(chat_id=update.effective_chat.id,
                                    text=texts.random_message(),
                                    reply_to_message_id=update.message.message_id)

    auto_delete(message_sent, update)


def latest_fun(update: Update, context: CallbackContext):
    device = update.message.text.replace("/latest", "").replace(" ", "")
    message_sent = bot.send_message(disable_web_page_preview=True, parse_mode="HTML", chat_id=update.effective_chat.id,
                                    text=info.cook_content(info.get_device_info(device)),
                                    reply_to_message_id=update.message.message_id, )

    auto_delete(message_sent, update)


def help_fun(update: Update, context: CallbackContext):
    message = "Hey there, I am a bot who is made to help people with stuff related to Project Sakura\nI can do " \
              "these things as of now\n\n/start - try it out yourself\n\n/help - shows this message\n\n/latest" \
              " <codename> - to grab the latest Project Sakura (A11) Build for your device\n\n" \
              "/list -  to get a list of all supported devices for Project Sakura"
    message_sent = bot.send_message(disable_web_page_preview=True, parse_mode="MARKDOWN",
                                    chat_id=update.effective_chat.id,
                                    text=message, reply_to_message_id=update.message.message_id, )

    auto_delete(message_sent, update)


def list_fun(update: Update, context: CallbackContext):
    supported_devices = []

    request = requests.get("https://raw.githubusercontent.com/ProjectSakura/OTA/11/devices.json")
    json_processed = json.loads(request.content)
    for devices in json_processed:
        if devices['active']:
            supported_devices.append(str(devices["name"]) + " (" + texts.code(str(devices["codename"])) + ")")

    message = "The following devices have Official Project Sakura builds:\n\n"
    number = 1
    for i in supported_devices:
        message = message + str(number) + ". " + str(i) + "\n"
        number += 1

    message_sent = bot.send_message(disable_web_page_preview=True, parse_mode="HTML", chat_id=update.effective_chat.id,
                                    text=message, reply_to_message_id=update.message.message_id, )

    auto_delete(message_sent, update)


start_command = CommandHandler("start", start_fun, run_async=True)
latest_command = CommandHandler("latest", latest_fun, run_async=True)
help_command = CommandHandler("help", help_fun, run_async=True)
list_command = CommandHandler("list", list_fun, run_async=True)

dispatcher.add_handler(start_command)
dispatcher.add_handler(latest_command)
dispatcher.add_handler(help_command)
dispatcher.add_handler(list_command)

updater.start_polling()
