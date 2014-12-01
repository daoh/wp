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


x = convertor.Convertor()
x.convert()


'''
m = myriad.Myriad()
m.check_parts()
m.parts_parser()
'''