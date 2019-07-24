from bot_classes import *
token = "895692386:AAHx5XyR6rk36N9ZWfIsvs02x0sV0CBwEB4"


create_log = True  # BOOL-> printing logs to console, also may print to file

users_file = "users.json"  # saves list of unique users, stop logging
log_file = "log.txt"  # CASE NONE - dont log to file
users_login_file = "logins.json"  # file with users and their logins

# bot_commands="""start - press start
#                 help - for more info
#                 contacts - if you found a bug
#                 menu - main menu
#                 products - products
#                 atb - atb
#                 """
# -----------------------------------------------
# BOT KEYBOARD TEMPLATES
# MAIN MENU
mm_keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
mm_keyboard.row("/products")
mm_keyboard.row("/help", "/contacts", "/genpass")
# PRODUCT MENU
prod_menu = telebot.types.ReplyKeyboardMarkup(True, False)
prod_menu.add("Торгівельна мережа АТБ")
prod_menu.add("/menu - go to main menu")
# _---------------------------------------------


current_service_code = -1

# URLS
service_codes_list = ["atb"]

# SHOP CLASS SAMPLES
service_list = []
service_list.append(service(0, service_codes_list[0], "Торгівельна мережа АТБ", "https://www.atbmarket.com/hot/akcii/economy/",))
