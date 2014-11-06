##
# Модуль сохранения сессии
##
import pickle


class Saver():
    def __init__(self):
        # Основной словарь для сохранения состояния проекта
        try:
            saver_file = open("saver_data", 'rb')
            self.dic = pickle.load(saver_file)
            saver_file.close()
        except:
            self.dic = {"session": None}

    def save(self):
        saver_file = open("saver_data", "wb")
        pickle.dump(self.dic, saver_file)
        saver_file.close()

    def get_session(self):
        return self.dic["session"]

    def set_session(self, session):
        self.dic["session"] = session
        self.save()