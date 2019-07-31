# Standart libs
import requests  # HTTP request pip lib
import time  # execution time
import re
# -----------------------------------------------------
# custom files
from bot_classes import *
import config


# -----------------------------------------------------
# INTERFACE FUNCTIONS
def get_products_list(service_code):
    
    start_time = time.time()

    target_url = config.service_list[service_code].url
    res = requests.get(target_url)
    htmlDocument = res.text
    # FOR ATB CODE == 0
    print("--- %s seconds for request: ---" % (time.time() - start_time))
    if(service_code == 0):
        result = create_product_atb(htmlDocument, config.service_list[service_code].url)
    elif service_code == 1:
        pass
    print("\n["+str(len(result))+"]")

    print("--- %s seconds for request + parse---" % (time.time() - start_time))
    return result


def remove_indent(string):
    #     #«Monaco» Чорничний чізкейк / Еклер-Брауні, ріжок ТМ «Три Ведмеді» - 110/100 г

    string = string.replace("\n", "").replace("\t", "").replace("\r", "")
    while(string.startswith(" ")):
        string = string[1:]
    while(string.endswith(" ")):
        string = string[0:len(string) - 1:]
    return string

# -----------------------------------------------------
# PARSE FUNCTIONS

def create_product_atb(string , url):
    resulting_array = []

    #@todo FIND FIRST ELEMENT 
    # IMAGE
    pattern = r"""attachments/product/[\w/]+.jpg"""
    image_url_list = re.findall(pattern, string)
    image_url_list = image_url_list[1::]

    # DISCOUNT
    pattern = r"""<p>Економія</p>[\s]*<span>-([\d]+.)</span>"""
    discount_list = re.findall(pattern, string)
    # discount_list = discount_list[1::]

    # NEW PRICE
    pattern = r"""<div class="promo_price">[\s]*(\d+)<span>"""
    # res = re.search(pattern, string)
    decimals_list = re.findall(pattern, string)
    pattern = r"""<div class="promo_price">[\s]*\d+<span>([\d]+)</span>"""
    floats_list = re.findall(pattern, string)
    # print(res.group())
    new_price_list = []
    for i in range(0, len(decimals_list)):
        new_price_list.append(decimals_list[i] + "," + floats_list[i])
    new_price_list = new_price_list[1::]

    # NAME / DESCRIPTION
    pattern = r"""<span class="promo_info_text">[\s]+(.+)[\s]+<span>"""
    # res = re.search(pattern, string)
    name_list = re.findall(pattern, string)
    name_list = name_list[1::]
    # print(remove_indent(res[0]))
    pattern = r"""<span class="promo_info_text">[\s].+[\s]+<span>[\s]+(.+)[\s]+</span>"""
    description_list = re.findall(pattern, string)
    description_list = description_list[1::]

    # OLD PRICE
    pattern = r"""<span class="promo_old_price big_price">([\d\.]+)"""
    # res = re.search(pattern, string)
    old_price_list = re.findall(pattern, string)

    for i in range(len(old_price_list)):
            # def __init__(self, name="-", current_price="-", old_price="-", details_url="-", description="-", discount="-", picture_url = "-"):
        tmp_object = product( name_list[i], new_price_list[i], old_price_list[i], url, description_list[i], discount_list[i], image_url_list[i])
        tmp_object.print_product()
        resulting_array.append(tmp_object)
    return resulting_array    

# def create_product_atb(string, url):

#     index_1 = 0
#     index_2 = 0
#     resulting_array = []

#     while index_1 != -1:
#         tmp_product = product("-")

#         # DISCOUNT
#         #@<div class="economy_price">
#         # 					<p>Економія</p>
#         # 					<span>-50%</span>
#         target_substring = """<div class="economy_price">"""
#         index_1 = string.find(target_substring, index_1, len(string))
#         if(index_2 - index_1 > 500):
#             index_1 = index_2
#         target_substring = """<span>"""
#         index_2 = string.find(target_substring, index_1, len(string))
#         index_2 += len(target_substring)
#         target_substring = "</span>"
#         # list[a:b:c] a - first ind, b - second ind, c - step
#         index_1 = string.find(target_substring, index_2, len(string))
#         discount = string[index_2:index_1]
#         tmp_product.discount = remove_indent(discount)

#         # IMAGE
#         # <span class="promo_image_link">
#         # 	<img class="lazyModal" data-src="attachments/product/5/e/1/f/5/5e1f5ae35e8649f48fe1061e8ad5b42d.jpg" alt="Морозиво"/>
#         # </span>
#         target_substring = """<img class="lazyModal" data-src=\""""
#         index_1 = string.find(target_substring, index_1 - 1000, len(string))
#         if(index_1 == -1):
#             # while ends here
#             return resulting_array
#         index_1 += len(target_substring)
#         target_substring = '.jpg\"'
#         index_2 = string.find(target_substring, index_1+2, len(string))
#         index_2 += len(target_substring) - 1

#         picture_url = string[index_1:index_2]
        
#         tmp_product.picture_url = "https://www.atbmarket.com/" + remove_indent(picture_url)

#         # CURRENT PRICE
#         # <div class="promo_price">
#         # 					9<span>90</span>
#         # 					<span class="currency">грн</span>
#         target_substring = """<div class="promo_price">"""
#         index_1 = string.find(target_substring, index_1, len(string))
#         index_1 += len(target_substring)
#         target_substring = """<span>"""
#         index_2 = string.find(target_substring, index_1, len(string))
#         # decimal part of price
#         current_price = string[index_1:index_2] + ","
#         #
#         index_2 += len(target_substring)
#         # index_1 = index_2
#         target_substring = "</span>"
#         index_1 = string.find(target_substring, index_2, len(string))
#         current_price += string[index_2:index_1]
        
#         tmp_product.current_price = remove_indent(current_price)

#         # OLD PRICE
#         # <span class="promo_old_price big_price">19.90</span>
#         target_substring = """<span class="promo_old_price big_price">"""
#         index_1 = string.find(target_substring, index_1, len(string))
#         # if(index_1 == -1):
#         #     # while ends here
#         #     return resulting_array
#         index_1 += len(target_substring)
#         target_substring = "</span>"
#         index_2 = string.find(target_substring, index_1, len(string))
#         old_price = string[index_1:index_2]
        
#         tmp_product.old_price = remove_indent(old_price)
#         # NAME/DESCRIPTION
#         # <span class="promo_info_text">
#     # 				Морозиво
#     # 				<span>
#     # 					Monaco Карамель-кунжут / Cookies ескімо, глазуроване ТМ «Три Ведмеді» - 80 г
#     # 				</span>
#         target_substring = """<span class="promo_info_text">"""
#         index_1 = string.find(target_substring, index_1, len(string))
#         index_1 += len(target_substring)
#         target_substring = "<span>"
#         index_2 = string.find(target_substring, index_1, len(string))
#         name = string[index_1:index_2]
#         tmp_product.name = remove_indent(name)
#         # DESCRIPTION
#         index_2 += len(target_substring)
#         target_substring = "</span>"
#         index_1 = string.find(target_substring, index_2, len(string))
#         description = string[index_2:index_1]
        
#         tmp_product.description = remove_indent(description)

#         tmp_product.details_url = url
#         # tmp_product.print_product()
#         resulting_array.append(tmp_product)
#         # print(len(resulting_array))

#     return resulting_array


# get_products_list(0)
# createProduct(htmlDOcument, url)

# print(requests.get("https://silpo.ua/offers").text)