##
# Модуль редактирования страниц
##
import saver


class Editor():
    def __init__(self, page_name=None, prefix="ru"):
        if page_name is None:
            print("No page name!")
            return
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