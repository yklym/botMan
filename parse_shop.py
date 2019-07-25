# Standart libs
import requests  # HTTP request pip lib
import time  # execution time
# -----------------------------------------------------
# custom files
from bot_classes import *
import config


# -----------------------------------------------------
# INTERFACE FUNCTIONS
def get_products_list(service_code):

	#DECORATOR
    target_url = config.service_list[service_code].url
    res = requests.get(target_url)
    htmlDocument = res.text
    start_time = time.time()
    # FOR ATB CODE == 0
    if(service_code == 0):
        result = create_product_atb(htmlDocument, config.service_list[service_code].url)
    print("\n["+str(len(result))+"]")

    print("--- %s seconds ---" % (time.time() - start_time))
    return result


def remove_indent(string):
    string = string.replace("\n", "").replace("\t", "").replace("\r", "")
    while(string.startswith(" ")):
        string = string[1:]
    while(string.endswith(" ")):
        string = string[0:len(string) - 1:]
    return string

# -----------------------------------------------------
# PARSE FUNCTIONS
def create_product_atb(string, url):
    
	#Parse HTML-string
    """
	PICTURE
		<div class="promo_list promo_item">
    	<a href="" class="modal_close" data-dismiss="modal" aria-hidden="true">X</a>
    	<div class="promo_image_wrap">
    	<span class="promo_image_link">
    		<img class="lazyModal" data-src="attachments/product/5/e/1/f/5/5e1f5ae35e8649f48fe1061e8ad5b42d.jpg" alt="Морозиво"/>
    	</span>
    	</div>
    DISCOUNT
    	<div class="promo_info">
    		<div class="price_box big_box red_box floated_left">
    			<div class="economy_price_container">
    				<div class="economy_price">
    					<p>Економія</p>
    					<span>-50%</span>
    				</div>
    				</div>
    NEW PRIcE
    				<div class="promo_price">
    					9<span>90</span>
    					<span class="currency">грн</span>
    				</div>
    OLD PRICE
    		<span class="promo_old_price big_price">19.90</span>
    	</div>
    NAME
    			<span class="promo_info_text">
    				Морозиво
    				<span>
    					Monaco Карамель-кунжут / Cookies ескімо, глазуроване ТМ «Три Ведмеді» - 80 г
    				</span>
    			</span>
    		</div>
    	</div>
	"""
    target_substring = 0
    index_1 = 0
    index_2 = 0
    resulting_array = []
 
    while index_1 != -1:
        tmp_product = product("-")

        # DISCOUNT
        # <div class="economy_price">
        # 					<p>Економія</p>
        # 					<span>-50%</span>
        target_substring = """<div class="economy_price">"""
        index_1 = string.find(target_substring, index_1, len(string))
        target_substring = """<span>"""
        index_2 = string.find(target_substring, index_1, len(string))
        index_2 += len(target_substring)
        target_substring = "</span>"
        index_1 = string.find(target_substring, index_2, len(string))
        discount = string[index_2:index_1]
        tmp_product.discount = remove_indent(discount)

        # CURRENT PRICE
        # <div class="promo_price">
        # 					9<span>90</span>
        # 					<span class="currency">грн</span>
        target_substring = """<div class="promo_price">"""
        index_1 = string.find(target_substring, index_1, len(string))
        index_1 += len(target_substring)
        target_substring = """<span>"""
        index_2 = string.find(target_substring, index_1, len(string))
        # decimal part of price
        current_price = string[index_1:index_2] + ","
        #
        index_2 += len(target_substring)
        index_1 = index_2
        target_substring = "</span>"
        index_1 = string.find(target_substring, index_2, len(string))
        current_price += string[index_2:index_1]
        tmp_product.current_price = remove_indent(current_price)

        # OLD PRICE
        # <span class="promo_old_price big_price">19.90</span>
        target_substring = """<span class="promo_old_price big_price">"""
        index_1 = string.find(target_substring, index_1, len(string))
        if(index_1 == -1):
            # while ends here
            return resulting_array
        index_1 += len(target_substring)
        target_substring = "</span>"
        index_2 = string.find(target_substring, index_1, len(string))
        old_price = string[index_1:index_2]
        tmp_product.old_price = old_price.replace(" ", "")

        # NAME/DESCRIPTION
        # <span class="promo_info_text">
    # 				Морозиво
    # 				<span>
    # 					Monaco Карамель-кунжут / Cookies ескімо, глазуроване ТМ «Три Ведмеді» - 80 г
    # 				</span>
        target_substring = """<span class="promo_info_text">"""
        index_1 = string.find(target_substring, index_1, len(string))
        index_1 += len(target_substring)
        target_substring = "<span>"
        index_2 = string.find(target_substring, index_1, len(string))
        name = string[index_1:index_2]
        tmp_product.name = remove_indent(name)
        # DESCRIPTION
        index_2 += len(target_substring)
        target_substring = "</span>"
        index_1 = string.find(target_substring, index_2, len(string))
        description = string[index_2:index_1]
        tmp_product.description = remove_indent(description)

        tmp_product.details_url = url
        # tmp_product.print_product()
        resulting_array.append(tmp_product)
        # print(len(resulting_array))

    return resulting_array


# get_products_list(config.url_atb, create_product_atb)
# createProduct(htmlDOcument, url)
