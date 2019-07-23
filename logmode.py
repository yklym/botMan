import telebot
import config
from datetime import datetime
import json


def log_to_file(log_dict, log_file=None):
    if(log_file != None):
        try:
            log_f = open(log_file, "a")
        except:
            line = "--------------->"
            print(line + "\n!!!Can't open file" + log_file + '\n' + line)
        log_f.write(str(log_dict) + "\n")
        log_f.close()
    else:
        return


def update_users(log_dict, users_file=None):
    if(users_file != None):
        with open(users_file, "r") as read_it:
            data = json.load(read_it)
        read_it.close()
        # ---------------------------------
        try:
            list_json = open(users_file, "w")
        except:
            line = "--------------->"
            print(line + "\n!!!Can't open file" + users_file + '\n' + line)
        # ---------------------------
        buf_username = log_dict["username"]

        if not(buf_username in data.keys()):
            data[buf_username] = {
                "last_seen": log_dict["time"],
                "name": log_dict["name"],
                "surname": log_dict["surname"],
                "chat_id": log_dict["chat_id"],
                "activity": 1
            }
            json.dump(data, list_json)
            list_json.close()
        else:
            data[buf_username]["activity"] += 1
            data[buf_username]["last_seen"] = log_dict["time"]
            json.dump(data, list_json)
            list_json.close()

    else:
        return


def create_log(bot, mess, mess_type=None):
    info = dict()
    info["time"] = ("M:{},D:{}|| {}:{}").format(datetime.now(
    ).month, datetime.now().day, datetime.now().hour, datetime.now().minute)
    info["username"] = mess.chat.username
    info["name"] = mess.chat.first_name
    info["surname"] = mess.chat.last_name
    info["chat_id"] = mess.chat.id
    info["mess_id"] = mess.message_id
    if mess_type == None:
        return
    elif mess_type == "text":
        info["text"] = mess.text
    elif mess_type == "audio":
        info["text"] = "AUDIO"
    elif mess_type == "command":
        info["text"] = mess.text
    elif mess_type == "sticker":
        info["text"] = "sticker"
        info["sticker_id"] = mess.sticker.file_id
    log_to_file(info, config.log_file)
    update_users(info, config.users_file)
    print(info)

    