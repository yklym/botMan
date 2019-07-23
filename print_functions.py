import telebot
import string
import os
import 
import random
import logmode
import config
import json

def test_atb(message, bot):
    
def tell_about_help(message, bot):
    help_message = ("Hello {}.\nTo start using this bot type \
/login option this way:\n\n*/login [your login] [password] [service]*\n\nwithout \
using <>brackets, where [service] is optional(if None, I'll output all of the services). \
\n*NOTE*: I'LL delete your login message in case you pass authorization \
\n*NOTE_2*: u should be already registred in desktop application to use this bot.\
\n/contacts for any questions or suggestions!\nAnd may the Force be with you!").format(message.from_user.first_name)
    bot.send_message(message.chat.id, help_message, parse_mode="Markdown")


def tell_about_start(message, bot):
    start_message = "Hello there, {}.\nYou are using password manager bot. \
Although it still being tested and developed, you could help the project by testing it. \
You can write me /contacts of you have any questions or suggestions\
\nType /help for more info".format(message.from_user.first_name)
    bot.send_message(message.chat.id, start_message)


def tell_about_cat(message, bot):
    directory = "./cats"
    all_filles_in_dir = os.listdir(directory)
    random_cat = random.choice(all_filles_in_dir)
    img = open(directory + "/" + random_cat, "rb")

    bot.send_photo(message.chat.id, img)
    bot.send_message(message.chat.id, "Meow, shouldn't I?")
    img.close()


def say_hello(message, bot):
    text = message.text
    if "HELLO" in text.upper():
        greetings_message = "Hello you too!"
    elif "HI" in text.upper():
        greetings_message = "Hi, cutie)"
    elif "WHATS UP" in text.upper() or \
        "WHAT'S UP" in text.upper() or \
        "WASSAP" in text.upper() or \
        "SUP" in text.upper() or \
            "WASSUP" in text.upper():
        greetings_message = "SUP, Bro ... master, I mean"
    else:
        return False

    bot.send_message(message.chat.id, greetings_message)
    return True


def tell_about_contacts(message, bot):
    bot.send_message(
        message.chat.id, "Write me through the telegram - @Meow_meow_meow")


def login(message, bot):
    input_string = message.text.split()
    print(input_string)
    if (len(input_string) > 4) or (len(input_string) < 3):
        bot.send_message(
            message.chat.id, "Incorrect input, too many or too litle arguments")
        return

    with open(config.users_login_file, "r") as read_it:
        database = json.load(read_it)
    read_it.close()
    # print(database)
    # ----------------------------------
    if not(input_string[1] in database.keys()):
        bot.send_message(message.chat.id, "Error, this login is not defined!")
        return
    if input_string[2] != database[input_string[1]]["password"]:
        bot.send_message(message.chat.id, "Error, wrong password!")
        return
    # ---------------------------------
    service_user_needs = None
    if len(input_string) == 4:
        service_user_needs = input_string[3]

    bot.delete_message(message.chat.id, message.message_id)
    # @todo send user his data
    bot.send_message(
        message.chat.id, "Authentification success!\nSending your request:")
    # --------------------


def pass_gen(message, bot):
    input_string = message.text.split()
    if (len(input_string) > 3):
        bot.send_message(
            message.chat.id, "Incorrect input, too many arguments")
        return

    pass_length = 8
    char_list = list(string.digits)
    if(len(input_string) >= 2):
        pass_length = int(input_string[1])
        if(len(input_string) == 3):
            pass_strength = input_string[2]
            if(pass_strength == "medium"):
                char_list += string.ascii_letters
            elif(pass_strength == "strong"):
                char_list.clear()
                char_list += string.printable
                char_list.remove(" ")
                char_list.remove("\n")
                char_list.remove("\t")


    new_pass = ""
    for i in range(pass_length):
        new_pass += random.choice(char_list)

    bot.send_message(message.chat.id, new_pass)



# @part CONSTANTS
responce_to_text = "Im not a chat-bot, u know.\n P.S: Maybe ur using a wrong command?"
