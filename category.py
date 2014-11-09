import saver


class Category():
    def __init__(self, category, prefix="ru"):
        self.saver = saver.Saver()
        self.session = self.saver.get_session()
        self.category = category
        self.prefix = prefix
        self.base_url = "https://"+self.prefix+".wikipedia.org"
        self.res_list = []

    def is_exists(self, cat):
        pass

    def get_articles_with_deep(self, deep, cat_name=None):
        cur_deep = 0
        if cat_name == None:
            category = self.category
        else:
            category = cat_name
        while cur_deep <= deep:
            cur_deep += 1
            articles = self.get_cat_articles_list_by_name(cat_name=category)
            if articles is not None:

            subcategorys = self.get_cat_subcategorys_list_by_name(cat_name=category)
            if subcategorys is None:
                break
            else:
                for unit in subcategorys:
                    self.get_articles_with_deep(deep-cur_deep, unit)

    def get_articles(self):
        return self.get_cat_articles_list()

    def get_cat_subcategorys_list_by_name(self, cat_name):
        api = "/w/api.php?action=query&list=categorymembers&format=json&cmprop=title&cmtype=subcat&cmtitle="
        url = self.base_url + api + cat_name
        try:
            res = self.session.get(url)
            dic_list = res.json()["query"]["categorymembers"]
            res_list = []
            for unit in dic_list:
                res_list.append(unit["title"])
            return res_list
        except:
            return None

    def get_cat_subcategorys_list(self):
        return self.get_cat_subcategorys_list_by_name(cat_name=self.category)

    def get_cat_articles_list_by_name(self, cat_name):
        api = "/w/api.php?action=query&list=categorymembers&format=json&cmprop=title&cmtype=page&cmtitle="
        url = self.base_url + api + cat_name
        try:
            res = self.session.get(url)
            dic_list = res.json()["query"]["categorymembers"]
            res_list = []
            for unit in dic_list:
                res_list.append(unit["title"])
            return res_list
        except:
            return None

    def get_cat_articles_list(self):
        return self.get_cat_articles_list_by_name(cat_name=self.category)