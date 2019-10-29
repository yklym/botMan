#! /usr/bin/env python
# -*- coding: utf-8 -*-

import telebot

class product:
    """docstring for product"""

    def __init__(self, name="-", current_price="-", old_price="-", details_url="-", description="-", discount="-", picture_url="-", service_code = -1):
        super(product, self).__init__()
        self.name = name
        self.current_price = current_price
        self.old_price = old_price
        self.description = description
        self.discount = discount
        self.details_url = details_url
        self.picture_url = picture_url
        self.service_code = service_code

    def print_product(self):
        print("Name:[" + self.name + "] Price:[" + self.current_price + "] DISCOUNT[" +
              self.discount + "] Old price[" + self.old_price + "] Description[" + self.description + "]")

    def create_dict(self):
        dict = {
            "name": self.name,
            "current_price": self.current_price,
            "old_price": self.old_price,
            "details_url": self.details_url,
            "description": self.description,
            "discount": self.discount,
            "picture_url": self.picture_url,
            "service_code" : self.service_code
        }
        return dict
    def from_dict(self, dict):
        self.name = dict["name"]
        self.current_price = dict["current_price"]
        self.old_price = dict["old_price"]
        self.description = dict["description"]
        self.discount = dict["discount"]
        self.details_url = dict["details_url"]
        self.picture_url = dict["picture_url"]
        self.service_code = dict["service_code"]
        return self
        
    def create_preview_text(self):
        return """'{0}'\n//'{1}грн Стара ціна:{2}\nЗнижка: {3}""".format(self.name, self.current_price, self.old_price, self.discount)
# -------------------------------------------------------
class service:
    def __init__(self, code=-1, name="-", fullname="-", url="-", products=None):
        self.code = code
        self.name = name
        self.fullname = fullname
        self.products = products
        self.url = url


# new_obj = favourite(3, "dsad", "adsd", "dsaddas")
# print(new_obj.create_dict()["details_url"])