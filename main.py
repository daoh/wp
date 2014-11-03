##
# main
##
import login
import gui

print("run")
l = login.WPLogin()
l.login()

g = gui.Gui()
print("password = "+g.get_string())