##
# main
##
import login
import myriad
import convertor
import category


print("starting...")
l = login.WPLogin()
l.login()


x = category.Category(category="Категория:Статьи проекта Галерея славы русскоязычных жителей Земли по участникам")


'''
m = myriad.Myriad()
m.check_parts()
m.parts_parser()
'''