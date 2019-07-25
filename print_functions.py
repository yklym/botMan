import telebot
import string
import os
import random
import logmode
import config
import json
import parse_shop
import bot_classes

# bot.stop_polling()
# bot.polling(none_stop=True, interval=0)

# def test_atb(message, bot):


def print_products(message, bot):
    # @todo add event trigger
    products_list = parse_shop.get_products_list(config.current_service_code)
    index = config.current_page * config.page_size
    for i in range(0, 5):
        if index + i>= len(products_list):
            break
        details_button_markup = telebot.types.InlineKeyboardMarkup()
        detail_button = telebot.types.InlineKeyboardButton(text="Деталі...", callback_data="1")
        details_button_markup.add(detail_button)
        bot.send_message(message.chat.id, products_list[index+i].create_preview_text(
        ), reply_markup=details_button_markup)

 
    menu_buttons_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    if(config.current_page == 0):
        menu_buttons_markup.row("Наступна сторінка >>")
    elif (config.current_page >= len(products_list) // config.page_size):
        menu_buttons_markup.row("<< Попередня сторінка")
    else:
        menu_buttons_markup.row("<< Попередня сторінка",
                                "Наступна сторінка >>")
    menu_buttons_markup.row("<< Оновити сторінку >>")
    menu_buttons_markup.row("/menu", "/products")
    # menu_buttons_markup.row("/")
    bot.send_message(message.chat.id, "<<Сторінка {}/{}>>".format(config.current_page+1, len(products_list) // config.page_size + 1), reply_markup=menu_buttons_markup)


def products_menu(message, bot):
    keyboard = config.prod_menu
    message_text = "Choose shop"

    bot.send_message(message.chat.id, message_text, reply_markup=keyboard)


def main_menu(message, bot):
    start_message = "Main menu:"
    keyboard = config.mm_keyboard
    bot.send_message(message.chat.id, start_message, reply_markup=keyboard)


def tell_about_help(message, bot):
    help_message = "Help here"
    bot.send_message(message.chat.id, help_message, parse_mode="Markdown")


def tell_about_start(message, bot):
    start_message = "Hello there, {}.\nType /help for more info".format(
        message.from_user.first_name)
    keyboard = config.mm_keyboard
    # test_keyboard.row("/atb", "/contacts")
    bot.send_message(message.chat.id, start_message, reply_markup=keyboard)


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
        message.chat.id, "Write me through the telegram - @Meow_meow_meov")


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


def check_if_service_name(message):
    if(message.text == "Торгівельна мережа АТБ"):
        config.current_service_code = config.service_codes_list.index("atb")
        print("\n" + config.service_list[config.current_service_code].fullname +
              "\ncurr index:[{}]".format(config.current_service_code))
        return config.service_list[config.current_service_code]
    else:
        return bot_classes.service(code=-1)


# def products_menu_atb(message, bot):


# @part CONSTANTS
responce_to_text = "Im not a chat-bot, u know.\n P.S: Maybe ur using a wrong command?"
