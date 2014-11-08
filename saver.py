##
# Модуль сохранения сессии
##
import pickle
import tools


class Saver():
    def __init__(self):
        # Основной словарь для сохранения состояния проекта
        try:
            saver_file = open("saver_data", 'rb')
            self.dic = pickle.load(saver_file)
            saver_file.close()
        except:
            self.dic = {}

    def save(self):
        saver_file = open("saver_data", "wb")
        pickle.dump(self.dic, saver_file)
        saver_file.close()

    def add_param(self, param_name):
        self.dic[param_name] = None
        self.save()

    def get_param_data(self, param_name):
        if param_name in self.dic:
            return self.dic[param_name][1]
        else:
            return None

    def get_param_date(self, param_name):
        if param_name in self.dic:
            return self.dic[param_name][0]
        else:
            return None

    def set_param_data(self, param_name, data):
        unit = [tools.get_date(), data]
        self.dic[param_name] = unit
        self.save()

    def get_session(self):
        return self.get_param_data("session")

    def set_session(self, session):
        self.set_param_data("session", session)