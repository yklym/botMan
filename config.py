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
main_menu_keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
main_menu_keyboard.row("Продукти ...")
main_menu_keyboard.row("/help", "/contacts")
# PRODUCT MENU
# prod_menu = telebot.types.ReplyKeyboardMarkup(True, False)
# prod_menu.add("Торгівельна мережа АТБ")
# prod_menu.add("/menu - go to main menu")
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

# current_service_code = -1

# URLS
service_codes_list = ["atb"]

# SHOP CLASS SAMPLES
service_list = []
service_list.append(service(0, service_codes_list[0], "Торгівельна мережа АТБ", "https://www.atbmarket.com/hot/akcii/economy/",))

