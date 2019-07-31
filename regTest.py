import re

def remove_indent(string):
    #     #«Monaco» Чорничний чізкейк / Еклер-Брауні, ріжок ТМ «Три Ведмеді» - 110/100 г

    string = string.replace("\n", "").replace("\t", "").replace("\r", "")
    while(string.startswith(" ")):
        string = string[1:]
    while(string.endswith(" ")):
        string = string[0:len(string) - 1:]
    return string

string = """ <span class="promo_old_price big_price">19.90</span>"""

pattern1 = r"""<span class="promo_old_price big_price">([\d\.]+)"""
# res = re.search(pattern, string)
res = re.findall(pattern1, string)
print(remove_indent(res[0]))
# pattern2 = r"""<span class="promo_info_text">[\s].+[\s]+<span>[\s]+(.+)[\s]+</span>"""
# res2 = re.findall(pattern2, string)
# print(remove_indent(res2[0]))

# print(res.group())
# for i in range(0, len(res)):
#     print(i)
