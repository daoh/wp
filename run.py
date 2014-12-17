import login
import yeararticle
import time

l = login.WPLogin()
l.login()

while True:
    yeararticle.stat()
    time.sleep(1000)