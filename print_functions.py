#! /usr/bin/env python
# -*- coding: utf-8 -*-
import telebot
import string
import os
import random
import logmode
from config import *
import json
import re
import parse_shop
import bot_classes
# import urllib.request

def print_favourites(message, bot):
    user_config = logmode.get_user_dict(message.chat.username)
    # curr_service_code = user_config["current_service_code"]
    products_dict_list = user_config["favourites"]
    products_list = []
    for i in products_dict_list:
        tmp_product = bot_classes.product("-")
        products_list.append(tmp_product.from_dict(i))

    print("{" + str(type(products_list))+ '}{' + str(len(products_list)) +"}")
    print(products_list[0].name)
    index = user_config["current_page"] * user_config["page_size"]
    for i in range(0, 3):
        bot.send_message(message.chat.id, bot_msg_text.arrows_delimiter)
    for i in range(0, user_config["page_size"]):
        if index + i >= len(products_list):
            break
        # details_button_markup = telebot.types.InlineKeyboardMarkup()
        # detail_button = telebot.types.InlineKeyboardButton(
        #     text="details...", callback_data="details_" + str(curr_service_code) + "_" + str(index+i))
        # details_button_markup.add(detail_button)
        # SAVE AND SEND PHOTO
        filename = "prodPictures/tmpPicture.jpg"
        urllib.request.urlretrieve(products_list[index+i].picture_url, filename)
        picture_file = open(filename, "rb")
        picture = picture_file.read()

        bot.send_photo(message.chat.id, picture,  caption=products_list[index+i].create_preview_text())

    menu_buttons_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    if(user_config["current_page"] == 0 and len(products_list) // user_config["page_size"] <= 1):
        pass
    elif(user_config["current_page"] == 0):
        menu_buttons_markup.row(bot_msg_text.next_product_page_button)
    elif (user_config["current_page"] >= len(products_list) // user_config["page_size"]):
        menu_buttons_markup.row(bot_msg_text.previous_product_page_button)
    else:
        menu_buttons_markup.row(bot_msg_text.previous_product_page_button,
                                bot_msg_text.next_product_page_button)
    menu_buttons_markup.row()
    menu_buttons_markup.row(bot_msg_text.exit_curr_service_button)
    bot.send_message(message.chat.id, "<b>[[СТОРІНКА {}/{}]]</b>".format(user_config["current_page"] + 1, len(
        products_list) // user_config["page_size"] + 1), reply_markup=menu_buttons_markup, parse_mode="HTML")


def print_products(message, bot):
    user_config = logmode.get_user_dict(message.chat.username)
    curr_service_code = user_config["current_service_code"]
    products_list = parse_shop.get_products_list(curr_service_code)
    index = user_config["current_page"] * user_config["page_size"]
    for i in range(0, 3):
        bot.send_message(message.chat.id, bot_msg_text.arrows_delimiter)
    for i in range(0, user_config["page_size"]):
        if index + i >= len(products_list):
            break
        details_button_markup = telebot.types.InlineKeyboardMarkup()
        # name="-", current_price="-", old_price="-", details_url="-", description="-", discount="-", picture_url = "-"):
        detail_button = telebot.types.InlineKeyboardButton(
            text="details...", callback_data="details_" + str(curr_service_code) + "_" + str(index+i))
        details_button_markup.add(detail_button)
        # SAVE AND SEND PHOTO
        filename = "prodPictures/tmpPicture.jpg"
        urllib.request.urlretrieve(
            products_list[index+i].picture_url, filename)
        picture_file = open(filename, "rb")
        picture = picture_file.read()

        bot.send_photo(message.chat.id, picture, reply_markup=details_button_markup, caption=products_list[index+i].create_preview_text())

    menu_buttons_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    if(user_config["current_page"] == 0):
        menu_buttons_markup.row(bot_msg_text.next_product_page_button)
    elif (user_config["current_page"] >= len(products_list) // user_config["page_size"]):
        menu_buttons_markup.row(bot_msg_text.previous_product_page_button)
    else:
        menu_buttons_markup.row(bot_msg_text.previous_product_page_button,
                                bot_msg_text.next_product_page_button)
    menu_buttons_markup.row(bot_msg_text.update_product_page_button)
    menu_buttons_markup.row(bot_msg_text.exit_curr_service_button)
    bot.send_message(message.chat.id, "<b>[[СТОРІНКА {}/{}]]</b>".format(user_config["current_page"] + 1, len(
        products_list) // user_config["page_size"] + 1), reply_markup=menu_buttons_markup, parse_mode="HTML")
    
def delete_few_messages(msg_id, msg_number, chat_id,  bot):
    msg_id += 1
    try:
        for i in range(msg_id - msg_number, msg_id):
            bot.delete_message(chat_id, i)
    except:
        bot.send_message(chat_id, "----------------------------------")
        print("\n\n!!!ERROR DELETING MSG!!!\n\n")
        return

def delete_products_page(message, bot):
    # Receive users message, deletes product page
    user_settings = logmode.get_user_dict(message.chat.username)
    prod_array_len = len(parse_shop.get_products_list(
        user_settings["current_service_code"]))
    if user_settings["current_page"] >= (prod_array_len // user_settings["page_size"]):
        delete_few_messages(message.message_id, (prod_array_len % user_settings["page_size"]) + 5, message.chat.id, bot)
        return
    delete_few_messages(message.message_id, int(
        user_settings["page_size"]) + 5, message.chat.id, bot)

# def add_favourite(message, bot):

def print_details_callback(message, callback_data, bot):
    args = callback_data.split("_")
    current_service_code = args[1]
    product_index = int(args[2])

    prod = parse_shop.get_products_list(current_service_code)[product_index]
    details_button_markup = telebot.types.InlineKeyboardMarkup()
        # name="-", current_price="-", old_price="-", details_url="-", description="-", discount="-", picture_url = "-"):
    detail_button = telebot.types.InlineKeyboardButton(
        text="Додати в обране", callback_data="addfavourite_{}_{}".format(current_service_code, product_index))
    print("!!!!!!!!!!!!!!!!!!!!!!!\n"+'addfavourite_{}_{}'.format(current_service_code, product_index))
    detail_button_2 = telebot.types.InlineKeyboardButton(
        text="<< Повернутися до магазину >>", callback_data="exit_details")
    details_button_markup.add(detail_button)
    details_button_markup.add(detail_button_2)

    # MSG TEXT
    msg_text = "<b>Назва</b>: " + prod.name + "\n<b>Ціна зі знижкою</b>: " + prod.current_price + "\n<b>Ціна без знижки</b>: " + \
        prod.old_price + "\n<b>Знижка</b>: " + prod.discount + "\n<b>Опис</b>: \n" + \
        prod.description + "\n<b>Деталі</b>: <a href=\"" + \
        str(prod.details_url) + "\">Сайт магазину</a>"
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

def new_favourite(callback_data, bot):
    args = callback_data.data.split("_")
    current_service_code = args[1]
    product_index = int(args[2])

    prod = parse_shop.get_products_list(current_service_code)[product_index]
    
    current_fav_list = logmode.get_user_field( callback_data.message.chat.username, "favourites")
    current_fav_list.append(prod.create_dict())
    
    logmode.update_user_field("favourites", current_fav_list, callback_data.message.chat.username)



def products_menu(message, bot):
    prod_menu = telebot.types.ReplyKeyboardMarkup(True, False)
    for service in service_list:
        prod_menu.add(service.fullname)

    prod_menu.add(bot_msg_text.main_menu_button)
    message_text = bot_msg_text.services_menu_message

    bot.send_message(message.chat.id, message_text, reply_markup=prod_menu)


def main_menu(message, bot):
    start_message = bot_msg_text.main_menu_message
    bot.send_message(message.chat.id, start_message,
                     reply_markup=main_menu_keyboard)


def tell_about_help(message, bot):
    help_message = bot_msg_text.help_message
    bot.send_message(message.chat.id, help_message,
                     parse_mode="Markdown", reply_markup=main_menu_keyboard)

# def tell_about_start(message, bot):
#     keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
#     keyboard.row("Продукти ...")
#     keyboard.row("/help", "/contacts") 
#     bot.send_message(message.chat.id, bot_msg_text.get_help_message(message.from_user.first_name), reply_markup=keyboard)


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
    bot.send_message(message.chat.id, bot_msg_text.contacts_message, reply_markup=main_menu_keyboard)


def check_if_service_name(message):
    # Services list in config.py
    for service in service_list:
        if(message.text == service.fullname):
            logmode.update_user_field("current_service_code", service.code, message.chat.username)
            return service
    
    # if(message.text == "Торгівельна мережа АТБ"): PREV VERSION
    #     logmode.update_user_field("current_service_code", service_codes_list.index(
    #         "atb"), message.chat.username)
    #     # current_service_code = service_codes_list.index("atb")
    #     # print("\n" + service_list[current_service_code].fullname +
    #     #       "\ncurr index:[{}]".format(current_service_code))
    #     return service_list[service_codes_list.index("atb")]
    
    
    # else:
    return bot_classes.service(code=-1)

def responce_to_casual_text(message, bot):
    responce_to_text = bot_msg_text.reply_to_unknown_message
    bot.send_message(message.chat.id, responce_to_text)
