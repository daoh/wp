##
# Модуль для проекта Мириада
##
import saver
import editor
import re

class Myriad():
    def __init__(self):
        self.saver = saver.Saver()
        self.session = self.saver.get_session()
        self.base_parts_name = "List of articles every Wikipedia should have/Expanded/"
        # FIXME в тестовом режиме работаем с сокращенным списком
        self.parts = ["People"]
        #self.parts = ["People","History","Geography","Arts","Philosophy and religion",
        #              "Anthropology, psychology and everyday life","Society and social sciences",
        #              "Biology and health sciences","Physical sciences","Technology","Mathematics"]
        self.is_full_parts_work = True
        self.broken_parts = []

    def check_parts(self):
        good_count = 0
        all_count = len(self.parts)
        good_list = []
        for part_name in self.parts:
            full_part_name = self.base_parts_name + part_name
            ed = editor.Editor(full_part_name, prefix="meta")
            status = "[ ]"
            if ed.get_text() is not None:
                status = "[x]"
                good_list.append(part_name)
                good_count += 1
            else:
                self.is_full_parts_work = False
                self.broken_parts.append(part_name)
            print(status + " " + part_name)
        print("Всего разделов: "+str(all_count)+". Ошибок: "+str(all_count-good_count))
        if good_count < all_count:
            self.parts = good_list
            for part_name in self.broken_parts:
                print("[fail] "+part_name)

    def parts_parser(self):
        print("\n\n======================")
        ##
        # Обходим все разделы списка
        ##
        for part_name in self.parts:
            print(part_name)
            ##
            # Достаем текст раздела, будучи уверенными, что он существует,
            # так как после проверки в списке остались только существующие
            ##
            full_part_name = self.base_parts_name + part_name
            ed = editor.Editor(full_part_name, prefix="meta")
            data = ed.get_text()
            ##
            # Ищем заявленное количество статей в разделе
            ##
            try:
                pattern = re.compile("[^=]==[^=]+"+part_name+"[^=]+==[^=]")
                line = re.search(pattern, data).group()[1:-1]
                part_art_count_t = int(re.search(re.compile("[0-9]+"), line).group())
            except:
                part_art_count_t = -1
            print("  - теретически должно быть "+str(part_art_count_t)+" статей")
            ##
            # Смотрим подразделы
            ##
            subtitle_count = 0
            subtitle_pattern = re.compile("[^=]===[^=]+===[^=]")
            is_subtitle_exists = True
            subtitle_art_count_t = 0
            while is_subtitle_exists:
                try:
                    subtitle = re.search(subtitle_pattern, data).group()[1:-1]
                    subtitle_art_count_t += int(re.search(re.compile("[0-9]+"), subtitle).group())
                    print(subtitle)
                    data = data[data.find(subtitle)+len(subtitle):]
                    subtitle_count += 1
                    try:
                        next_subtitle = re.search(subtitle_pattern, data).group()
                        temp = data[:data.find(next_subtitle)]
                        data = data[data.find(next_subtitle):]
                    except:
                        temp = data
                        is_subtitle_exists = False
                except:
                    is_subtitle_exists = False
            print(subtitle_count)
            print(subtitle_art_count_t)