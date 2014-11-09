import saver


class Category():
    def __init__(self, category, prefix="ru"):
        self.saver = saver.Saver()
        self.session = self.saver.get_session()
        self.category = category
        self.prefix = prefix
        self.base_url = "https://"+self.prefix+".wikipedia.org"
        self.res_list = []
        self.deep = 0

    def print(self, data):
        #print(data)
        pass

    def is_exists(self, cat):
        pass

    def get_all_articles(self):
        return self.get_articles_with_deep(1000000)

    def make_articles_with_deep(self, deep, catname=None):
        if catname is None:
            category = self.category
            self.deep = deep
            deep = 0
        else:
            category = catname
        self.print(category)
        self.print("deep: "+str(deep))
        if deep < self.deep:
            articles = self.get_cat_articles_list_by_name(cat_name=category)
            self.print(articles)
            if articles is not None:
                self.print(len(articles))
                self.res_list += articles
            if deep == self.deep:
                self.print("end of deep")
                return
            subcategorys = self.get_cat_subcategorys_list_by_name(cat_name=category)
            if subcategorys is None:
                self.print("no subcategories")
                return
            else:
                for unit in subcategorys:
                    self.make_articles_with_deep(deep+1, unit)

    def get_articles_with_deep(self, deep):
        self.res_list = []
        self.make_articles_with_deep(deep)
        return self.res_list

    def get_articles(self):
        return self.get_cat_articles_list()

    def get_cat_subcategorys_list_by_name(self, cat_name):
        api = "/w/api.php?action=query&list=categorymembers&cmlimit=1000000&format=json&cmprop=title&cmtype=subcat&cmtitle="
        url = self.base_url + api + cat_name
        try:
            res = self.session.get(url)
            dic_list = res.json()["query"]["categorymembers"]
            res_list = []
            for unit in dic_list:
                res_list.append(unit["title"])
            if len(res_list) == 0:
                return None
            return res_list
        except:
            return None

    def get_cat_subcategorys_list(self):
        return self.get_cat_subcategorys_list_by_name(cat_name=self.category)

    def get_cat_articles_list_by_name(self, cat_name):
        api = "/w/api.php?action=query&list=categorymembers&cmlimit=1000000&format=json&cmprop=title&cmtype=page&cmtitle="
        url = self.base_url + api + cat_name
        try:
            res = self.session.get(url)
            dic_list = res.json()["query"]["categorymembers"]
            res_list = []
            for unit in dic_list:
                res_list.append(unit["title"])
            if len(res_list) == 0:
                return None
            return res_list
        except:
            return None

    def get_cat_articles_list(self):
        return self.get_cat_articles_list_by_name(cat_name=self.category)