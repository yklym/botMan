import requests

#-----------------------------------------------------
class product:
	"""docstring for product"""
	def __init__(self, name = "-",current_price="-", old_price="-",details_url="-", description ="-", discount ="-"):
		super(product, self).__init__()
		self.name = name
		self.current_price = current_price
		self.old_price = old_price
		self.description = description
		self.discount = discount
		self.details_url = details_url
	def print_product(self):
	    print("Name:[" + self.name+ "] Price:[" + self.current_price + "] DISCOUNT[" + self.discount + "] Old price[" + self.old_price + "] Description[" + self.description + "]")
	def create_dict(self):
		dict = {"name": self.name,
				"current_price": self.current_price,
				"old_price": self.old_price,
				"details_url": self.details_url,
				"description": self.description,
				"discount": self.discount
				}
		dict["name"] = self.name
		dict["current_price"] = self.current_price   
#-----------------------------------------------------
url = "https://www.atbmarket.com/hot/akcii/economy/"
res = requests.get(url)

# # print(res.text)

htmlDOcument = res.text

# <div class="promo_list promo_item">
# 				PICTURE HERE
				# <a href="" class="modal_close" data-dismiss="modal" aria-hidden="true">X</a>
				# <div class="promo_image_wrap">
				# 	<span class="promo_image_link">
				# 		<img class="lazyModal" data-src="attachments/product/5/e/1/f/5/5e1f5ae35e8649f48fe1061e8ad5b42d.jpg" alt="Морозиво"/>
				# 	</span>
				# </div>
				# DISCOUNT
		# 	<div class="promo_info">
		# 		<div class="price_box big_box red_box floated_left">
		# 			<div class="economy_price_container">
		# 				<div class="economy_price">
		# 					<p>Економія</p>
		# 					<span>-50%</span>
		#				</div>
		# 				</div>
		# NEW PRIcE
		# 				<div class="promo_price">
		# 					9<span>90</span>
		# 					<span class="currency">грн</span>
		# 				</div>
		# OLD PRICE
 		#		<span class="promo_old_price big_price">19.90</span>
 		#	</div>
 		# NAME
# 			<span class="promo_info_text">
# 				Морозиво
# 				<span>
# 					Monaco Карамель-кунжут / Cookies ескімо, глазуроване ТМ «Три Ведмеді» - 80 г
# 				</span>
# 			</span>
# 		</div>
# 	</div>
def clear_result(string):
	string = string.replace("\n", "").replace("\t", "").replace("\r", "")
	while(string.startswith(" ")):
		string = string[1:]
	while(string.endswith(" ")):
		string = string[0:len(string) - 1:]
	return string	

def createProduct(string, url):
	# Parse HTML-string
	index = 0
	tmp_substring = 0
	tmp_index_1 = 0
	tmp_index_2 = 0

	resulting_array = []
	while tmp_index_1 != -1:
		tmp_product = product()

		# DISCOUNT
		# <div class="economy_price">
		# 					<p>Економія</p>
		# 					<span>-50%</span>
		tmp_substring = """<div class="economy_price">"""
		tmp_index_1 = string.find(tmp_substring, tmp_index_1, len(string))
		tmp_substring = """<span>"""
		tmp_index_2 = string.find(tmp_substring, tmp_index_1, len(string))
		tmp_index_2+=len(tmp_substring)
		tmp_substring = "</span>"
		tmp_index_1 = string.find(tmp_substring, tmp_index_2, len(string))
		tmp_discount = string[tmp_index_2:tmp_index_1]
		tmp_product.discount = clear_result(tmp_discount)
	 	

		# CURRENT PRICE
		# <div class="promo_price">
		# 					9<span>90</span>
		# 					<span class="currency">грн</span>
		tmp_substring = """<div class="promo_price">"""
		tmp_index_1 = string.find(tmp_substring, tmp_index_1, len(string))
		tmp_index_1+=len(tmp_substring)
		tmp_substring = """<span>"""
		tmp_index_2 = string.find(tmp_substring, tmp_index_1, len(string))
		# decimal part of price
		tmp_current_price = string[tmp_index_1:tmp_index_2] + ","
		# 
		tmp_index_2 += len(tmp_substring)
		tmp_index_1 = tmp_index_2
		tmp_substring = "</span>"
		tmp_index_1 = string.find(tmp_substring, tmp_index_2, len(string))
		tmp_current_price += string[tmp_index_2:tmp_index_1]
		tmp_product.current_price = clear_result(tmp_current_price)

		
		# OLD PRICE
		# <span class="promo_old_price big_price">19.90</span>
		tmp_substring = """<span class="promo_old_price big_price">""";
		tmp_index_1 = string.find(tmp_substring, tmp_index_1, len(string))
		if(tmp_index_1==-1):
			# while ends here
			index = 0
			return resulting_array
		tmp_index_1 +=len(tmp_substring)
		tmp_substring = "</span>"
		tmp_index_2 = string.find(tmp_substring, tmp_index_1, len(string))
		tmp_old_price = string[tmp_index_1:tmp_index_2]
		tmp_product.old_price = tmp_old_price.replace(" ", "")
		# print(tmp_product)

		# NAME/DESCRIPTION 
		# <span class="promo_info_text">
	# 				Морозиво
	# 				<span>
	# 					Monaco Карамель-кунжут / Cookies ескімо, глазуроване ТМ «Три Ведмеді» - 80 г
	# 				</span>
		tmp_substring = """<span class="promo_info_text">""";
		tmp_index_1 = string.find(tmp_substring, tmp_index_1, len(string))
		tmp_index_1 +=len(tmp_substring)
		tmp_substring = "<span>"
		tmp_index_2 = string.find(tmp_substring, tmp_index_1, len(string))
		tmp_name = string[tmp_index_1:tmp_index_2]
		tmp_product.name = clear_result(tmp_name)
		# DESCRIPTION
		tmp_index_2+=len(tmp_substring)
		tmp_substring = "</span>"
		tmp_index_1 = string.find(tmp_substring, tmp_index_2, len(string))
		tmp_description = string[tmp_index_2:tmp_index_1]
		tmp_product.description = clear_result(tmp_description)

		tmp_product.details_url = url
		tmp_product.print_product()
		index = tmp_index_1
		resulting_array.append(tmp_product)
		print(len(resulting_array))
	
	return resulting_array
# print("!!!"+createProduct(htmlDOcument)[0].+"!!!!")


createProduct(htmlDOcument, url)