#! /usr/bin/env python
# -*- coding: utf-8 -*-
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

def get_user_field(username, field_name):
    with open(config.users_file, "r") as read_it:
        data = json.load(read_it)
    read_it.close()
    if not(username in data.keys()):
        line = "--------------->"
        print(line + "\n!!! No user in file " + config.users_file + '\n' + line)

    if not(field_name in data.values()):
        line = "--------------->"
        print(line + "\n!!! No value {} in file".format(field_name) + config.users_file + '\n' + line)
    return data[username][field_name]


def get_user_dict(username):
    try:
        f = open(config.users_file, "r")
        data = json.load(f)
        f.close()
    except:
        line = "--------------->"

        print(line + "\n!!!Can't open file " + config.users_file + '\n' + line)
    # with open(config.users_file, "r") as read_it:
    #     data = json.load(read_it)
    # read_it.close()
    
    return data[username]

def update_user_field(field, value, user):
    
    with open(config.users_file, "r") as read_it:
        data = json.load(read_it)
    read_it.close()
    # ---------------------------------
    try:
        list_json = open(config.users_file, "w")
    except:
        line = "--------------->"
        print(line + "\n!!!Can't open file " + config.users_file + '\n' + line)
    # ---------------------------

    if not(user in data.keys()):
        line = "--------------->"
        print(line + "\n!!! No user in file" + config.users_file + '\n' + line)
    else:
        data[user][field] = value
        json.dump(data, list_json)
        list_json.close()


def update_user(log_dict):
    if(config.users_file != None):
        with open(config.users_file, "r") as read_it:
            data = json.load(read_it)
        read_it.close()
        # ---------------------------------
        try:
            list_json = open(config.users_file, "w")
        except:
            line = "--------------->"
            print(line + "\n!!!Can't open file" + config.users_file + '\n' + line)
        # ---------------------------
        buf_username = log_dict["username"]

        # IF USER US FIRSTLY ADDED TO FILE, CREATE JSON TEMPLATE
        if not(buf_username in data.keys()):
            data[buf_username] = {
                "last_seen": log_dict["time"],
                "name": log_dict["name"],
                "surname": log_dict["surname"],
                "chat_id": log_dict["chat_id"],
                "activity": 1,
                "current_service_code": -1,
                "current_page": 0,
                "page_size": 5,
                "favourites" : []
            }
            json.dump(data, list_json)
            list_json.close()
        else:
            # ELSE WE UPDATE
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
    # CHECK FOR NON-ENGLISH NAME
    name_list = mess.chat.first_name.split(" ")
    if(len(name_list) > 1):
        info["name"] = name_list[1]
        info["surname"] = name_list[0]
    else:
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
    update_user(info, )
    print(info)
