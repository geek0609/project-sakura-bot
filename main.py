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

BOT_API = os.environ.get("BOT_API")

bot = Bot(BOT_API)
updater = Updater(BOT_API, use_context=True)
dispatcher = updater.dispatcher
timeout = 60


def auto_delete(message_sent, update):
    if update.effective_chat.type == "supergroup" or  update.effective_chat.type == "group":
        time.sleep(timeout)
        bot.deleteMessage(update.effective_chat.id, message_sent.message_id)
        bot.deleteMessage(update.effective_chat.id, update.message.message_id)


def get_device_info(device):
    request = requests.get("https://raw.githubusercontent.com/ProjectSakura/OTA/11/website/" + device + ".json")
    print("https://raw.githubusercontent.com/ProjectSakura/OTA/11/website/" + device + ".json")
    print(request.content)
    if not request.ok:
        return False
    converted = json.loads(request.content)
    required = converted['response'][0]
    request = requests.get("https://raw.githubusercontent.com/ProjectSakura/OTA/11/devices.json")
    json_processed = json.loads(request.content)
    for devices in json_processed:
        if devices['codename'] == device:
            maintainer = devices['maintainer_name']
            name = devices['name']
            brand = devices['brand']
            active = devices["active"]

    if "VANILLA" in required['filename']:
        variant = "Vanilla"
    elif "GAPPS-Core" in required['filename']:
        variant = "GApps Core"
    elif "GAPPS-Basic" in required['filename']:
        variant = "GApps Basic"
    elif "microg" in required['filename'].lower():
        variant = "MicroG"
    else:
        variant = "GApps"

    if required['updater']:
        notes = "✅ OTA has been pushed; Clean flash not mandatory"
    else:
        notes = "❎ OTA not pushed; Clean flash mandatory"

    print("Device is : " + device)
    print("Size is : " + str(required['size']))
    print("Maintained by : " + maintainer)
    print("File name : " + required['filename'])
    print("Version : " + required['version'])
    print("Variant : " + variant)
    print("Notes : " + notes)

    return {
        "device": device,
        "size": str(required['size']),
        "maintainer": maintainer,
        "variant": variant,
        "version": required['version'],
        'name': name,
        "brand": brand,
        "notes": notes,
        "time": required['datetime'],
        "filename": required['filename'],
        "id": required['id'],
        "romtype": required['romtype'],
        "url": required['url'],
        "updater": required['updater'],
        "active": active
    }


def bold(text1, text2):
    message = "<b>" + text1 + "</b>" + text2
    return message


def link(link, text):
    return "<a href=\"" + str(link) + "\">" + text + "</a>"
    # links need to be in this format <a href="http://www.example.com/">XYZ</a>


def cook_content(information):
    if not information:
        return "Device not found, make sure you are typing see /help for more"

    if information["active"]:
        active_status = "✅ This device is currently <b>officially supported</b>"
    else:
        active_status = "❎ This device is <b>not currently officially supported</b>\nIf you wish to maintain " \
                        "Project Sakura for this device, see " + link("https://projectsakura.xyz/wiki/#/apply",
                                                                      "our official wiki")

    message = "Latest" + bold(" Project Sakura ", "") + "for " + information['name'] + " (" + str(
        information['device']) + ")\n" + \
              "👤 " + bold("by ", str(information["maintainer"])) + "\n" + \
              "ℹ️ " + bold("Version : ", str(information['version'])) + "\n" + \
              "❕ " + bold("Variant: ", str(information["variant"])) + "\n" + \
              "⬇️ " + bold(link("https://projectsakura.xyz/download/#/" + information['device'], "Download"),
                           "") + "\n\n" + \
              active_status

    return message


def start_fun(update: Update, context: CallbackContext):
    message_sent = bot.send_message(chat_id=update.effective_chat.id,
                     text=random_message(),
                     reply_to_message_id=update.message.message_id)

    auto_delete(message_sent, update)


def latest_fun(update: Update, context: CallbackContext):
    device = update.message.text.replace("/latest", "").replace(" ", "")
    message_sent = bot.send_message(disable_web_page_preview=True, parse_mode="HTML", chat_id=update.effective_chat.id,
                                    text=cook_content(get_device_info(device)),
                                    reply_to_message_id=update.message.message_id, )

    auto_delete(message_sent, update)


def help_fun(update: Update, context: CallbackContext):
    message = "Hey there, I am a bot who is made to help people with stuff related to Project Sakura\nI can do " \
              "these things as of now\n\n/start - try it out yourself\n\n/help - shows this message\n\n/latest" \
              " <codename> - to grab the latest Project Sakura (A11) Build for your device\n\n" \
              "/list -  to get a list of all supported devices for Project Sakura"
    message_sent = bot.send_message(disable_web_page_preview=True, parse_mode="MARKDOWN", chat_id=update.effective_chat.id,
                     text=message, reply_to_message_id=update.message.message_id, )

    auto_delete(message_sent, update)


def list_fun(update: Update, context: CallbackContext):
    supported_devices = []

    request = requests.get("https://raw.githubusercontent.com/ProjectSakura/OTA/11/devices.json")
    json_processed = json.loads(request.content)
    for devices in json_processed:
        if devices['active']:
            supported_devices.append(str(devices["name"]) + " (<code>" + str(devices["codename"]) + "</code>)")

    message = "The following devices have Official Project Sakura builds:\n\n"
    number = 1
    for i in supported_devices:
        message = message + str(number) + ". " + str(i) + "\n"
        number += 1

    message_sent = bot.send_message(disable_web_page_preview=True, parse_mode="HTML", chat_id=update.effective_chat.id,
                     text=message, reply_to_message_id=update.message.message_id, )

    auto_delete(message_sent, update)


def random_message():
    messages = ["Ignorance is Bliss", "Is it time to flash another update already?", "Hyped about Android 12?",
                "Oh hey, what\'s up?", "Focus on your tasks", "How many screenshots do you take?",
                "She will not say yes xD",
                "Spread love not havoc :P", "Have fun!", 'Time for some good music', "You need Project Sakura Premium",
                "Remember the Lineage of the Unicorn", "Enjoy Xtended battery life", "Starting from the ground zero",
                "Using Project Sakura? Damn you are superior", "Stay Home, Stay Safe", "Do something nice today",
                "Hello there its a nice day, isn\'t it?", "How is everything going?",
                "No illusions, welcome to reality!",
                "Thank you for your support", "No festival for Derps - only perfection!",
                "One of the buildbot\'s best picks",
                "Sanity for your Paranoia", "Try Ice Cold desserts", "Evolution is a myth, right?", "You are what you f"
                                                                                                    "lash, don\'t be "
                                                                                                    "Potato", 
                "What\'s on your mind?", "Playing that stupid game again?", "rm -rf *",
                "Imagine not using Project Sakura", "Hmmmm.... What is it?", "Send me PUBG 90fps module", "OK"]
    return random.choice(messages)


start_command = CommandHandler("start", start_fun, run_async=True)
latest_command = CommandHandler("latest", latest_fun, run_async=True)
help_command = CommandHandler("help", help_fun, run_async=True)
list_command = CommandHandler("list", list_fun, run_async=True)

dispatcher.add_handler(start_command)
dispatcher.add_handler(latest_command)
dispatcher.add_handler(help_command)
dispatcher.add_handler(list_command)

updater.start_polling()