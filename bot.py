#! /usr/bin/env python
# -*- coding: utf-8 -*-

import telebot
import config
import requests
import parse_shop
import print_functions
import logmode

# CONSTANT
bot = telebot.TeleBot(config.token)

# @part COMMANDS
@bot.message_handler(commands=['help'])
def print_help(message):
    print_functions.delete_few_messages(
        message.message_id, 2, message.chat.id, bot)
    print_functions.tell_about_help(message, bot)

    logmode.create_log(bot, message, "command")

# @bot.message_handler(commands=['products'])
# def print_products(message):
#     # bot.send_message(message.chat.id, "hello to your power!")
#     # print_functions.login(message, bot)
#     print_functions.products_menu(message, bot)
#     logmode.create_log(bot, message, "command")


@bot.message_handler(commands=['start'])
def print_start(message):
    print_functions.delete_few_messages(
        message.message_id, 1, message.chat.id, bot)
    print_functions.main_menu(message, bot)

    logmode.create_log(bot, message, "command")


@bot.message_handler(commands=['menu'])
def main_menu(message):
    print_functions.delete_few_messages(
        message.message_id, 1, message.chat.id, bot)
    print_functions.main_menu(message, bot)

    logmode.create_log(bot, message, "command")


@bot.message_handler(commands=['contacts'])
def send_contacts(message):
    print_functions.delete_few_messages(
        message.message_id, 2, message.chat.id, bot)
    print_functions.tell_about_contacts(message, bot)

    logmode.create_log(bot, message, "command")


@bot.message_handler(func=lambda mess: mess.text == config.bot_msg_text.previous_product_page_button)
def reduce_page(message):
    curr_page = logmode.get_user_field(message.chat.username, "current_page")
    tmp_mess = message
    print_functions.delete_products_page(tmp_mess, bot)
    logmode.update_user_field(
        "current_page", curr_page - 1, message.chat.username)
    print_functions.print_products(message, bot)

    logmode.create_log(bot, message, "command")

@bot.message_handler(func=lambda mess: mess.text == config.bot_msg_text.next_product_page_button)
def increase_page(message):
    curr_page = logmode.get_user_field(message.chat.username, "current_page")

    print_functions.delete_products_page(message, bot)
    logmode.update_user_field(
        "current_page", curr_page + 1, message.chat.username)
    print_functions.print_products(message, bot)

    logmode.create_log(bot, message, "command")


@bot.message_handler(func=lambda mess: mess.text == config.bot_msg_text.update_product_page_button)
def update_page(message):
    print_functions.delete_products_page(message, bot)
    print_functions.print_products(message, bot)

    logmode.create_log(bot, message, "command")


@bot.message_handler(func=lambda mess: mess.text == config.bot_msg_text.main_menu_button)
def exit_product_menu(message):
    print_functions.delete_few_messages(
        message.message_id, 2, message.chat.id, bot)
    print_functions.main_menu(message, bot)

    logmode.create_log(bot, message, "command")


@bot.message_handler(func=lambda mess: mess.text == config.bot_msg_text.product_menu_button)
def exit_main_menu(message):
    print_functions.delete_few_messages(
        message.message_id, 2, message.chat.id, bot)
    print_functions.products_menu(message, bot)

    logmode.create_log(bot, message, "command")


@bot.message_handler(func=lambda mess: mess.text == config.bot_msg_text.exit_curr_service_button)
def exit_shop(message):
    print_functions.delete_products_page(message, bot)
    print_functions.products_menu(message, bot)
    logmode.create_log(bot, message, "command")

@bot.message_handler(func=lambda mess: mess.text == config.bot_msg_text.favourites_menu_button)
def favourites_menu(message):
    print_functions.delete_few_messages(message.message_id, 2, message.chat.id, bot)
    logmode.update_user_field("current_page", 0, message.chat.username)
    print_functions.print_favourites(message, bot)
    logmode.create_log(bot, message, "command")


@bot.message_handler(content_types=['text'])
def answer_text(message):
    code = print_functions.check_if_service_name(message).code
    if print_functions.say_hello(message, bot):  # CHAT-BOT FUNCTIONS
        if config.create_log:
            logmode.create_log(bot, message, "text")
        return
    elif(code >= 0):  # IF STRING IS SHOP NAME
        logmode.create_log(bot, message, "command")
        logmode.update_user_field("current_page", 0, message.chat.username)
        logmode.update_user_field(
            "current_service_code", code, message.chat.username)
        print_functions.delete_few_messages(
            message.message_id, 2, message.chat.id, bot)
        print_functions.print_products(message, bot)
        return
    else:
        print_functions.responce_to_casual_text(
            message, bot)  # DEFAULT ANSWER TO STRING
        if config.create_log:
            logmode.create_log(bot, message, "text")

# @part CALLBACK TO INLINE KEYS
@bot.callback_query_handler(func=lambda call: call.data.split("_")[0] == "details")
def show_details(call):
    print("CAlbback:[" + call.data + "]")
    tmp_mess = bot.send_message(call.message.chat.id, ".")
    print_functions.delete_products_page(tmp_mess, bot)
    # bot.delete_message(tmp_mess.chat.id, tmp_mess.message_id )
    print_functions.print_details_callback(call.message, call.data, bot)

    logmode.create_log(bot, call.message, "button")


@bot.callback_query_handler(func=lambda call: call.data == "exit_details")
def exit_details(call):
    print("CAlbback:[" + call.data + "]")
    print_functions.delete_few_messages(
        call.message.message_id, 1, call.message.chat.id, bot)
    print_functions.print_products(call.message, bot)

    logmode.create_log(bot, call.message, "command")


@bot.callback_query_handler(func=lambda call: call.data.split("_")[0] == "addfavourite")
def add_favourite(call):
    print("CAlbback:[" + call.data + "]")

    # bot.send_photo(call.message.chat.id, "AgADAgAD6KsxG53BuUqdkrXazwk3dX3Rtw8ABAEAAwIAA3gAA5hjAgABFgQ"	)
    print_functions.new_favourite(call, bot)
    print_functions.delete_few_messages(
        call.message.message_id, 1, call.message.chat.id, bot)
    print_functions.print_products(call.message, bot)

    logmode.create_log(bot, call.message, "command")

#  FOR LOG ONLY logs media
@bot.message_handler(content_types=['sticker'])
def answer_sticker(message):
    logmode.create_log(bot, message, "sticker")


@bot.message_handler(content_types=['photo'])
def answer_photo(message):
    logmode.create_log(bot, message, "sticker")


@bot.message_handler(content_types=['audio'])
def answer_audio(message):
    logmode.create_log(bot, message, "sticker")

    # bot.stop_polling()


bot.polling(none_stop=config.none_stop_polling, interval=0)
