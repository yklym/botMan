import telebot
import string
import os
import random
import logmode
import config
import json
import parse_shop
import bot_classes
import urllib.request


def print_products(message, bot):
    user_config = logmode.get_user_dict(message.chat.username)
    curr_service_code = user_config["current_service_code"]
    products_list = parse_shop.get_products_list(curr_service_code)
    index = user_config["current_page"] * user_config["page_size"]
    for i in range(0, 3):
        bot.send_message(message.chat.id, "<<<<<<<<<<<>>>>>>>>>")
    for i in range(0, user_config["page_size"]):
        if index + i >= len(products_list):
            break
        details_button_markup = telebot.types.InlineKeyboardMarkup()
        # name="-", current_price="-", old_price="-", details_url="-", description="-", discount="-", picture_url = "-"):
        detail_button = telebot.types.InlineKeyboardButton(
            text="details...", callback_data="details_" + str(curr_service_code) + "_" + str(index+i))
        details_button_markup.add(detail_button)

        filename = "prodPictures/tmpPicture.jpg"
        urllib.request.urlretrieve(
            products_list[index+i].picture_url, filename)
        picture = " "
        picture_file = open(filename, "rb")

        picture = picture_file.read()
        bot.send_photo(message.chat.id, picture, reply_markup=details_button_markup,
                       caption=products_list[index+i].create_preview_text())
        # bot.send_photo(message.chat.id, picture)
        # bot.send_message(message.chat.id, products_list[index+i].create_preview_text(
        # ), reply_markup=details_button_markup)

    menu_buttons_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    if(user_config["current_page"] == 0):
        menu_buttons_markup.row("Наступна сторінка >>")
    elif (user_config["current_page"] >= len(products_list) // user_config["page_size"]):
        menu_buttons_markup.row("<< Попередня сторінка")
    else:
        menu_buttons_markup.row("<< Попередня сторінка",
                                "Наступна сторінка >>")
    menu_buttons_markup.row("<< Оновити сторінку >>")
    menu_buttons_markup.row("/menu", "/products")
    # menu_buttons_markup.row("/")
    bot.send_message(message.chat.id, "<b>[[СТОРІНКА {}/{}]]</b>".format(user_config["current_page"] + 1, len(
        products_list) // user_config["page_size"] + 1), reply_markup=menu_buttons_markup, parse_mode="HTML")


def delete_few_messages(msg_id, msg_number, chat_id,  bot):
    msg_id += 1
    for i in range(msg_id - msg_number, msg_id):
        bot.delete_message(chat_id, i)


def delete_products_page(message, bot):
    # Receive users message, deletes product page
    user_settings = logmode.get_user_dict(message.chat.username)
    prod_array_len = len(parse_shop.get_products_list(user_settings["current_service_code"]))  
    if user_settings["current_page"] >= (prod_array_len// user_settings["page_size"]):
        delete_few_messages(message.message_id, (prod_array_len % user_settings["page_size"]) + 5, message.chat.id, bot)    
        return
    delete_few_messages(message.message_id, int(user_settings["page_size"]) + 5, message.chat.id, bot)

def print_details_callback(message, callback_data, bot):
    args = callback_data.split("_")
    current_service_code = args[1]
    product_index = int(args[2])

    prod = parse_shop.get_products_list(current_service_code)[product_index]

    details_button_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    details_button_markup.row("Додати в обране")
    details_button_markup.row("<< Повернутися до магазину >>")
    details_button_markup.row("/menu", "/products")
    # MSG TEXT
    msg_text = "<b>Назва</b>: " + prod.name + "\n<b>Ціна зі знижкою</b>: " + prod.current_price + "\n<b>Ціна без знижки</b>: " + \
        prod.old_price + "\n<b>Знижка</b>: " + prod.discount + "\n<b>Опис</b>: \n" + \
        prod.description + "\n<b>Деталі</b>: <a href=\"" + \
        prod.details_url + "\">Сайт магазину</a>"
    # PICTURE
    filename = "prodPictures/tmpPicture.jpg"
    urllib.request.urlretrieve(prod.picture_url, filename)
    picture = " "
    picture_file = open(filename, "rb")
    picture = picture_file.read()

    # SendMSG method
    new_msg = bot.send_photo(message.chat.id, picture, reply_markup=details_button_markup,
                             caption=msg_text, parse_mode="HTML")
    print("\n{" + str(new_msg.message_id) + "}")
    return new_msg


def products_menu(message, bot):
    prod_menu = telebot.types.ReplyKeyboardMarkup(True, False)
    for service in config.service_list:
        prod_menu.add(service.fullname)

    prod_menu.add("/menu - go to main menu")
    # keyboard = config.prod_menu
    message_text = "Choose shop"

    bot.send_message(message.chat.id, message_text, reply_markup=prod_menu)


def main_menu(message, bot):
    start_message = "Main menu:"
    keyboard = config.mm_keyboard
    bot.send_message(message.chat.id, start_message, reply_markup=keyboard)


def tell_about_help(message, bot):
    help_message = "*Help here*"
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


def check_if_service_name(message):
    if(message.text == "Торгівельна мережа АТБ"):
        logmode.update_user_field("current_service_code", config.service_codes_list.index(
            "atb"), message.chat.username)
        # config.current_service_code = config.service_codes_list.index("atb")
        # print("\n" + config.service_list[config.current_service_code].fullname +
        #       "\ncurr index:[{}]".format(config.current_service_code))
        return config.service_list[config.service_codes_list.index("atb")]
    else:
        return bot_classes.service(code=-1)


# def products_menu_atb(message, bot):
def responce_to_casual_text(message, bot):
    responce_to_text = "Im not a chat-bot, u know.\n P.S: Maybe ur using a wrong command?"
    bot.send_message(message.chat.id, responce_to_text)
