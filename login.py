##
# Вход в Википедию и сохранение параметров
##
import settings
import gui
import requests
import pickle
import saver


class WPLogin():
    def __init__(self):
        self.user_name = settings.user_name
        self.user_password = settings.user_password
        self.saver = saver.Saver()
        self.session = self.saver.get_session()
        if self.session is None:
            self.session = requests.Session()

    def check_login(self):
        ##
        # Проверка авторизации.
        # Запрашивается страница с информацией об участнике.
        ##
        # good {"query":{"userinfo":{"id":1151236,"name":"Sebiumeker","editcount":115}}}
        # bad {"query":{"userinfo":{"id":0,"name":"93.175.12.119","anon":"","editcount":0}}}
        req_url = "https://ru.wikipedia.org/w/api.php?action=query&meta=userinfo&format=json"
        try:
            res = self.session.get(req_url)
            user_id = res.json()["query"]["userinfo"]["id"]
            name = res.json()["query"]["userinfo"]["name"]
        except:
            return False
        if user_id == 0 or name != self.user_name:
            return False
        return True

    def login_try(self):
        ##
        # Авторизация происходит в 2 этапа.
        # 1) имя и пароль посылаются пост-запросом, возвращается токен
        # 2) токен отсылается обратно для проверки
        ##
        # correct first: {"login":{"result":"NeedToken","token":"xxx","cookieprefix":"ruwiki","sessionid":"xxx"}}
        # correct 2nd: {"login":{"result":"Success","lguserid":1151236,"lgusername":"xxx","lgtoken":"xxx","cookieprefix":"ruwiki","sessionid":"xxx"}}
        # bad 2nd: {"login":{"result":"WrongPass"}}
        # bad 2nd: {"login":{"result":"NotExists"}}
        try:
            login_url = "https://ru.wikipedia.org/w/api.php?action=login&format=json"
            post_data1 = {'lgname': self.user_name, 'lgpassword': self.user_password}
            res1 = self.session.post(login_url, post_data1)
            result1 = res1.json()["login"]["result"]
            if result1 != "NeedToken":
                print("ACHTUNG! Bad login try. Wrong 1st result.")
                return False
            token1 = res1.json()["login"]["token"]
            cookieprefix1 = res1.json()["login"]["cookieprefix"]
            sessionid1 = res1.json()["login"]["sessionid"]
        except:
            print("EXCEPTION! Bad login try. 1st part.")
            return False

        try:
            post_data2 = post_data1
            post_data2["lgtoken"] = token1
            res2 = self.session.post(login_url, post_data2)
            result2 = res2.json()["login"]["result"]
            if result2 != "Success":
                print("ACHTUNG! Bad login try. Wrong 2nd result.")
                return False
            userid2 = res2.json()["login"]["lguserid"]
            username2 = res2.json()["login"]["lgusername"]
            if username2 != self.user_name:
                print("ACHTUNG! Bad login try. Get wrong username.")
                return False
            token2 = res2.json()["login"]["lgtoken"]
            cookieprefix2 = res2.json()["login"]["cookieprefix"]
            if cookieprefix2 != cookieprefix1:
                print("ACHTUNG! Bad login try. Wrong cookie prefix.")
                return False
            sessionid2 =  res2.json()["login"]["sessionid"]
            if sessionid2 != sessionid1:
                print("ACHTUNG! Bad login try. Wrong session id.")
                return False
        except:
            print("EXCEPTION! Bad login try. 2nd part.")
            return False
        print("Success login. User: " + self.user_name)
        return True

    def login(self):
        ##
        # Вход в Википедию с проверкой.
        # Если уже вошел - используются текущие данные.
        # Если нет - имя берется из настроек, а пароль оттуда же, либо вводится.
        ##
        print("Hello "+self.user_name)
        if self.check_login():
            print(self.user_name + " already logged in!")
            return
        if self.user_password != "":
            print("it's not safe to keep password in file")
        else:
            g = gui.Gui()
            self.user_password = g.get_string()
            print("Thank you!")
        if self.login_try():
            self.saver.set_session(self.session)