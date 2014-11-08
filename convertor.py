import re


class Convertor():
    def __init__(self):
        pass

    def cite_book_to_book(self, template):
        dic = {"first": "", "last": "", "title": "", "url": "", "year": "", "isbn": "", "location": "", "publisher": "", "volume": ""}
        for key in dic:
            pattern = re.compile("\|[\s]*"+key+"[\s]*=")
            if pattern.search(template) is not None:
                tmp = template[pattern.search(template).end():]
                if tmp.find("|") != -1:
                    dic[key] = tmp[:tmp.find("|")]
                elif tmp.find("}") != -1:
                    dic[key] = tmp[:tmp.find("}")]
        res = "* {{книга\n"
        res += " | автор         = " + dic["first"] + " " + dic["last"] + "\n"
        res += " | заглавие      = " + dic["title"] + "\n"
        res += " | ссылка        = " + dic["url"] + "\n"
        res += " | место         = " + dic["location"] + "\n"
        res += " | издательство  = " + dic["publisher"] + "\n"
        res += " | год           = " + dic["year"] + "\n"
        res += " | том           = " + dic["volume"] + "\n"
        res += " | isbn          = " + dic["isbn"] + "\n"
        res += " | ref           = " + dic["last"] + "\n"
        res += "}}"
        return res

    def cite_journal_to_article(self, template):
        dic = {"first": "", "last": "", "journal": "", "title": "", "url": "", "year": "", "number": "",
               "doi": "", "location": "", "publisher": "", "volume": "", "pages": "", "date": "", "issn": "", "isbn": ""}
        year = dic["year"]
        if dic["year"] == "":
            year = dic["date"]
        res = "* {{статья\n"
        res += " |автор         = " + dic["first"] + " " + dic["last"] + "\n"
        res += " |заглавие      = " + dic["title"] + "\n"
        res += " |ссылка        = " + dic["url"] + "\n"
        res += " |язык          = " + "en" + "\n"
        res += " |издание       = " + dic["journal"] + "\n"
        res += " |год           = " + year + "\n"
        res += " |том           = " +  + "\n"
        res += " |номер         = " +  + "\n"
        res += " |страницы      = " +  + "\n"
        res += " |doi           = " +  + "\n"
        res += " |isbn          = " +  + "\n"
        res += " |issn          = " + dic["last"] + "\n"
        res += "}}"
        return res

    def convert(self):
        data = open("input", "r").read()
        data_list = data.split("*")[1:]
        for unit in data_list:
            unit = unit.strip()
            pattern = re.compile("\{\{[\s]*cite[\s]*book[\s]*\|")
            if pattern.search(unit) is not None:
                continue
                res = self.cite_book_to_book(unit)
                print(res)
            pattern = re.compile("\{\{[\s]*cite[\s]*journal[\s]*\|")
            if pattern.search(unit) is not None:
                print(unit)
                res = self.cite_journal_to_article(unit)
                #print(res)