import telebot
import config
import requests
import parse_shop
import print_functions
import logmode

# print(requests.get("https://api.telegram.org/bot/"+ config.token+"/getUpdates"))
# part INIT

bot = telebot.TeleBot(config.token)


# part FUNCTS
@bot.message_handler(commands=['help'])
def print_help(message):
    print_functions.tell_about_help(message, bot)
    logmode.create_log(bot, message, "command")


@bot.message_handler(commands=['products'])
def print_products(message):
    # bot.send_message(message.chat.id, "hello to your power!")
    # print_functions.login(message, bot)
    print_functions.products_menu(message, bot)
    logmode.create_log(bot, message, "command")


@bot.message_handler(commands=['start'])
def print_start(message):
    # bot.send_message(message.chat.id, "hello to your power!")
    print_functions.tell_about_start(message, bot)
    logmode.create_log(bot, message, "command")


@bot.message_handler(commands=['menu'])
def main_menu(message):
    # bot.send_message(message.chat.id, "hello to your power!")
    print_functions.main_menu(message, bot)
    logmode.create_log(bot, message, "command")


@bot.message_handler(commands=['contacts'])
def send_contacts(message):
    # bot.send_message(message.chat.id, "hello to your power!")
    print_functions.tell_about_contacts(message, bot)
    logmode.create_log(bot, message, "command")


@bot.message_handler(commands=['genpass'])
def gen_pass(message):
    # bot.send_message(message.chat.id, "hello to your power!")
    print_functions.pass_gen(message, bot)
    logmode.create_log(bot, message, "command")


# @bot.message_handler(commands=['atb'])
# def atb_menu(message):
#     # print_functions.products_menu_atb(message, bot)
#     logmode.create_log(bot, message, "command")
# -------------------------------------------
@bot.message_handler(func=lambda mess:mess.text=="<< Попередня сторінка")
def reduce_page(message):
    # if config.current_page == 0:
    #     return
    curr_page = logmode.get_user_field(message.chat.username, "current_page")
    logmode.update_user_field("current_page", curr_page - 1, message.chat.username)
    print_functions.print_products(message, bot)
    logmode.create_log(bot, message, "command")

@bot.message_handler(func=lambda mess:mess.text=="Наступна сторінка >>")
def increase_page(message):
    # if config.current_page == 0:
    #     return
    curr_page = logmode.get_user_field(message.chat.username, "current_page")
    logmode.update_user_field("current_page", curr_page + 1, message.chat.username)
    print_functions.print_products(message, bot)
    logmode.create_log(bot, message, "command")

@bot.message_handler(func=lambda mess:mess.text=="<< Оновити сторінку >>")
def update_page(message):
    # if config.current_page == 0:
    #     return
    print_functions.print_products(message, bot)
    logmode.create_log(bot, message, "command")

@bot.message_handler(content_types=['text'])
def answer_text(message):
    if print_functions.say_hello(message, bot):
        if config.create_log:
            logmode.create_log(bot, message, "text")
        return
    elif(print_functions.check_if_service_name(message).code>=0):
        logmode.create_log(bot, message, "command")
        logmode.update_user_field("current_page", 0, message.chat.username)
        print_functions.print_products(message, bot)
        return
    else:
        bot.send_message(message.chat.id, print_functions.responce_to_text)
        if config.create_log:
            logmode.create_log(bot, message, "text")

#  FOR LOG ONLY
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
 
@bot.callback_query_handler(func=lambda call: call.data.split("_")[0] == "details")
def  test_callback(call):
    print("CAlbback:[" + call.data+ "]")
    print_functions.print_details_callback(call.message,call.data, bot)
    logmode.create_log(bot, call.message, "button")

bot.polling(none_stop=True, interval=0)
