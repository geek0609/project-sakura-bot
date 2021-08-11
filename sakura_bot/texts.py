import random


def bold(text1, text2):
    message = "<b>" + text1 + "</b>" + text2
    return message


def link(url, text):
    return "<a href=\"" + str(url) + "\">" + text + "</a>"
    # links need to be in this format <a href="http://www.example.com/">XYZ</a>


def code(text):
    return "<code>" + str(text) + "</code>"


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

