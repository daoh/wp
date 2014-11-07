##
# Модуль редактирования страниц
##
import saver


class Editor():
    def __init__(self, page_name=None):
        if page_name is None:
            print("No page name!")
            return
        self.saver = saver.Saver()
        self.session = self.saver.get_session()
        self.page_name = page_name

    def get_text(self):

