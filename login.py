##
# Вход в Википедию и сохранение параметров
##
import settings

class WPLogin():
    def __init__(self):
        self.user_name = settings.user_name

    def login(self):
        print("Hello "+self.user_name)