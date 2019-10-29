#! /usr/bin/env python
# -*- coding: utf-8 -*-

from bot_classes import *
token = "895692386:AAHx5XyR6rk36N9ZWfIsvs02x0sV0CBwEB4"

none_stop_polling = True # Stop polling in case of error
create_log = True  # BOOL-> printing logs to console, also may print to file

users_file = "new_users.json"  # saves list of user settings
log_file = "log.txt"  # CASE NONE - dont log to file

# bot_commands="""start - press start
#                 help - for more info
#                 contacts - if you found a bug
#                 menu - main menu
#                 products - products
#                 atb - atb
#                 """
# -----------------------------------------------

# _---------------------------------------------
# USER JSON TEMPLATE 
# data[buf_username] = {
#                 "last_seen": log_dict["time"],
#                 "name": log_dict["name"],
#                 "surname": log_dict["surname"],
#                 "chat_id": log_dict["chat_id"],
#                 "activity": 1,
#                 "current_service_code": -1,
#                 "urrent_page": 0,
#                 "page_size" : 5
#             }


# URLS
service_codes_list = ["atb"]

# SHOP CLASS SAMPLES
service_list = []
service_list.append(service(0, service_codes_list[0], u"Торгівельна мережа АТБ", "https://www.atbmarket.com/hot/akcii/economy/",))
# favourites_code = -4






# Bot Text Messages



class msg_text:
    def __init__(self):
        self.arrows_delimiter =  "<<<<<<<<<<<>>>>>>>>>"
        self.next_product_page_button = u"Наступна сторінка >>"
        self.update_product_page_button = u"<< Оновити сторінку >>"
        self.previous_product_page_button = u"<< Попередня сторінка"
        self.main_menu_button = u"<- Головне меню"
        self.main_menu_message = u"Main menu:"
        self.exit_curr_service_button = u"<- Вибір магазину"
        self.product_menu_button = u"Продукти ..."
        self.help_message = u"*Help here*"
        self.contacts_message = u"Write me through the telegram - @Meow_meow_meov"
        self.services_menu_message = u"Виберіть магазин"
        self.favourites_menu_button = u"|Favourites|"
        self.reply_to_unknown_message = u"Im not a chat-bot, u know.\n P.S: Maybe ur using a wrong command?"


    def get_help_message(self, username):
        return "Hello there, {}.\nType /help for more info".format(username)
    # self.main_menu

bot_msg_text = msg_text()
print(bot_msg_text.arrows_delimiter)


# ______________________________________________________
# Keyboards
# ______________________________________________________
# MAIN MENU
main_menu_keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
main_menu_keyboard.row(bot_msg_text.product_menu_button)
main_menu_keyboard.row(bot_msg_text.favourites_menu_button)
main_menu_keyboard.row("/help", "/contacts")
# 
