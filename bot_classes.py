import telebot
# import config

# -----------------------------------------------

class product:
    """docstring for product"""

    def __init__(self, name="-", current_price="-", old_price="-", details_url="-", description="-", discount="-", picture_url = "-"):
        super(product, self).__init__()
        self.name = name
        self.current_price = current_price
        self.old_price = old_price
        self.description = description
        self.discount = discount
        self.details_url = details_url
        self.picture_url = picture_url

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
            "discount": self.discount
        }
        # dict["name"] = self.name
        # dict["current_price"] = self.current_price
        return dict
    def create_preview_text(self):
        return """'{0}'\n//'{1}грн Стара ціна:{2}\nЗнижка: {3}""".format(self.name, self.current_price, self.old_price, self.discount)     
# -------------------------------------------------------
class service:
    current_page = 0
    def __init__(self, code= -1, name = "-", fullname= "-", url = "-",products = None ):
        self.code = code
        self.name = name
        self.fullname = fullname
        self.products = products
        self.url = url
        # self.url = 

