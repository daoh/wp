##
# main
##
import login
import myriad
import convertor
import category

x = category.Category("Категория:Коммуны Сардинии")
print(x.get_cat_articles_list())
print(x.get_cat_subcategorys_list())

'''
print("starting...")
l = login.WPLogin()
l.login()

m = myriad.Myriad()
m.check_parts()
m.parts_parser()
'''