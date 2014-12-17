##
# Модуль редактирования страниц
##
import saver


class Editor():
    def __init__(self, page_name=None, prefix="ru"):
        if page_name is None:
            print("No page name!")
        self.saver = saver.Saver()
        self.session = self.saver.get_session()
        self.page_name = page_name
        self.prefix = prefix
        if self.prefix == "meta":
            self.domen = "wikimedia"
        else:
            self.domen = "wikipedia"

    def get_text(self):
        get_params = "action=query&prop=revisions&rvprop=content"
        url = "http://"+self.prefix+"."+self.domen+".org/w/api.php?"+get_params+"&format=json&titles="+self.page_name
        try:
            res = self.session.get(url).json()
            res = res["query"]["pages"]
            for id in res:
                break
            res = res[id]["revisions"][0]["*"]
        except:
            res = None
        return res

    def get_usercontribs(self, username, days):
        #https://ru.wikipedia.org/w/api.php?action=userdailycontribs&format=json&user=DZ&daysago=2
        #{"userdailycontribs":{"id":906754,"registration":"20120904180145","timeFrameEdits":42,"totalEdits":12446}}
        url = "https://ru.wikipedia.org/w/api.php?action=userdailycontribs&format=json&user="+username+"&daysago="+str(days)
        try:
            res = self.session.get(url).json()["userdailycontribs"]
        except:
            res = None
        return res

    def get_token(self):
        url = "https://ru.wikipedia.org/w/api.php?action=query&prop=info&format=json&intoken=edit&titles=" + self.page_name
        res = self.session.get(url)
        key = list(res.json()["query"]["pages"])[0]
        token = res.json()["query"]["pages"][key]["edittoken"]
        return token

    def put_art(self, data, comment):
        url = "https://ru.wikipedia.org/w/api.php?action=edit&format=json"
        token = self.get_token()
        post_data = {"title": self.page_name, "text": data, "token": token, "summary": comment, "bot": ""}
        res = self.session.post(url, post_data)
        print(res.json())