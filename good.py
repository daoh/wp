import re
import editor
import pickle
import tools


month_dic = {"01": "января", "02": "февраля", "03": "марта", "04": "апреля", "05": "мая", "06": "июня",
             "07": "июля", "08": "августа", "09": "сентября", "10": "октября", "11": "ноября", "12": "декабря"}

month_dic2 = {"01": "Январь", "02": "Февраль", "03": "Март", "04": "Апрель", "05": "Май", "06": "Июнь",
              "07": "Июль", "08": "Август", "09": "Сентябрь", "10": "Октябрь", "11": "Ноябрь", "12": "Декабрь"}

user_prefix = ["u", "U", "user", "User", "у", "У", "участник", "участница", "Участник", "Участница"]


def good_stater():
    # достаем рабочий словарь из файла
    work_dic = {}
    try:
        work_dic = pickle.load(open("good_data", "rb"))
    except:
        print("no data. create new")
        pickle.dump(work_dic, open("good_data", "wb"))

    # из него извлекаем список незаконченных дат
    nonfinish_date_list = []
    try:
        nonfinish_date_list = work_dic["nonfinish_date_list"]
    except:
        print("no nonfinish_date_list")
        work_dic["nonfinish_date_list"] = nonfinish_date_list
        pickle.dump(work_dic, open("good_data", "wb"))

    print("found "+str(len(nonfinish_date_list))+" nonfinished dates")
    cur_date = tools.get_date_str()
    cur_pos = 0
    is_last = False

    while not is_last:
        work_dic = pickle.load(open("good_data", "rb"))
        nonfinish_date_list = work_dic["nonfinish_date_list"]
        #nonfinish_date_list = ["270414"]                                   #fixme
        #is_last = True

        if len(nonfinish_date_list) == 0:
            print("закончился список")
            return

        print(nonfinish_date_list)
        date_str = nonfinish_date_list[cur_pos]

        if date_str == cur_date:
            is_last = True

        if date_str == "2011":
            title_date = date_str
        else:
            d = date_str[:2]
            if d[0] == "0":
                d = d[1]
            title_date = d + " " + month_dic[date_str[2:4]] + " 20" + date_str[4:6]
        print(title_date + "\n")
        base_name = "Википедия:Кандидаты в добротные статьи/"
        page_name = base_name + title_date

        ed = editor.Editor(page_name)
        date_data = ed.get_text()

        if date_data is None:
            print("no date page!")
            nonfinish_date_list.remove(date_str)
            work_dic["nonfinish_date_list"] = nonfinish_date_list
            pickle.dump(work_dic, open("good_data", "wb"))
            continue

        if date_str in work_dic:
            artdics_dic = work_dic[date_str]
        else:
            artdics_dic = {}

        is_done = True
        date_art_list = re.findall("[^=]==[^=][^\[]*\[\[[^\]]+\]\][^=]*==[^=]", date_data)

        for i in range(0, len(date_art_list), 1):
            art = date_art_list[i]
            art_name = art[art.find("[[")+2:art.find("]]")]
            if art_name in artdics_dic:
                art_dic = artdics_dic[art_name]
                is_new = False
            else:
                art_dic = {}
                art_dic["name"] = art_name
                is_new = True
            print(art_name)

            tmp_data = date_data[date_data.find(art):]
            art_data = tmp_data
            try:
                art_data = tmp_data[:tmp_data.find(date_art_list[i+1])]
            except:
                pass

            if is_new:
                nominator = ""
                for prefix in user_prefix:
                    try:
                        nominator = str(re.search("\[\["+prefix+":[^\|]+\|", art_data).group())[:-1]
                        nominator = nominator[nominator.find(":")+1:]
                    except:
                        pass
                    if nominator != "":
                        break
                if nominator == "":
                    nominator = "Unknown"
                art_dic["nominator"] = nominator
                nomdate = date_str
                art_dic["nomdate"] = nomdate
                print("Номинация: " + nominator + " - " + nomdate)

            if art_data.find("=== Итог ===") != -1:
                summ_data = art_data[art_data.find("=== Итог ==="):]
                if summ_data.find("{{Сделано|Статья избрана}}") != -1:
                    summary = "good"
                elif summ_data.find("{{Не сделано|Статья не избрана}}") != -1:
                    summary = "notgood"
                else:
                    summary = "Unknown"

                summator = ""
                for prefix in user_prefix:
                    try:
                        summator = str(re.search("\[\["+prefix+":[^\|]+\|", summ_data).group())[:-1]
                        summator = summator[summator.find(":")+1:]
                    except:
                        pass
                    if summator != "":
                        break
                if summator == "":
                    summator = "Unknown"

                tmp = re.search("\d\d:\d\d.*\(UTC\)", summ_data).group()
                tmp = re.search("[\d]+[ \w]+\d\d\d\d", tmp).group()
                d = re.search("[\d]+", tmp).group()
                if len(d) == 1:
                    d = "0" + d
                m = re.search("[^\d^\s]+", tmp).group()
                for key in month_dic:
                    if month_dic[key] == m:
                        m = key
                        break
                summdate = d + m + "14"
                print("Избрание: " + summator + " - " + summdate + " - " + summary)
            else:
                summary = ""
                summator = ""
                summdate = ""

            if summary == "":
                is_done = False

            art_dic["summary"] = summary
            art_dic["summator"] = summator
            art_dic["summdate"] = summdate

            ed = editor.Editor(art_name)
            art_text = ed.get_text()
            if art_text is None:
                art_curstate = "n"
            else:
                if art_text.find("Избранная статья") != -1:
                    art_curstate = "f"
                elif art_text.find("Хорошая статья") != -1:
                    art_curstate = "g"
                elif art_text.find("Добротная статья") != -1:
                    art_curstate = "d"
                else:
                    art_curstate = ""
            art_dic["art_curstate"] = art_curstate
            print("Шаблон в статье: "+art_curstate)

            talk_name = "Обсуждение:" + art_name
            ed = editor.Editor(talk_name)
            talk_text = ed.get_text()
            if talk_text is None:
                talk_curstate = "n"
            else:
                if talk_text.find("Сообщение ИС") != -1:
                    talk_curstate = "f"
                elif talk_text.find("Сообщение ХС") != -1:
                    talk_curstate = "g"
                elif talk_text.find("Сообщение ДС") != -1:
                    talk_curstate = "d"
                else:
                    talk_curstate = ""
            art_dic["talk_curstate"] = talk_curstate
            print("Шаблон на СО: "+talk_curstate)

            print(art_dic)
            artdics_dic[art_name] = art_dic

        work_dic[date_str] = artdics_dic

        if is_done:
            nonfinish_date_list.remove(date_str)
        else:
            cur_pos += 1

        work_dic["nonfinish_date_list"] = nonfinish_date_list
        pickle.dump(work_dic, open("good_data", "wb"))


def make_log():
    res_dic = {}
    work_dic = work_dic = pickle.load(open("good_data", "rb"))
    #print(work_dic)
    for date_str in work_dic:
        if date_str == "nonfinish_date_list":
            continue
        #print(date_str)
        arts_dic = work_dic[date_str]
        for art_name in arts_dic:
            #print(art_name)
            art_dic = arts_dic[art_name]
            #print(art_dic)
            status = art_dic["summary"]
            summator = art_dic["summator"]
            art_state = {}
            art_state["name"] = art_name
            art_state["status"] = status
            art_state["summator"] = summator
            summdate = art_dic["summdate"]
            d = summdate[:2]
            m = summdate[2:4]
            y = summdate[4:]
            #print(summator + " - " + d+m+y + " - " + summdate)
            if y in res_dic:
                ydic = res_dic[y]
            else:
                ydic = {}
            if m in ydic:
                mdic = ydic[m]
            else:
                mdic = {}
            if d in mdic:
                ddic = mdic[d]
            else:
                ddic = {}
            ddic[art_name] = art_dic
            mdic[d] = ddic
            ydic[m] = mdic
            res_dic[y] = ydic
    #print(res_dic)

    good_count = 0
    cur_good_count = 0
    lines = ""
    for y in range(14, 20):
        if str(y) not in res_dic:
            continue
        else:
            ydic = res_dic[str(y)]
        for m in range(1, 13):
            sm = str(m)
            if len(sm) == 1:
                sm = "0" + sm
            if sm not in ydic:
                continue
            else:
                mdic = ydic[sm]
            for d in range(1, 32):
                sd = str(d)
                if len(sd) == 1:
                    sd = "0" + sd
                if sd not in mdic:
                    continue
                else:
                    ddic = mdic[sd]
                for art_name in ddic:
                    art_dic = ddic[art_name]
                    #print(art_dic)
                    if art_dic["summary"] == "good":
                        stt = "избрана"
                        good_count += 1
                    elif art_dic["summary"] == "notgood":
                        stt = "отправлена на доработку"
                    else:
                        if art_dic["art_curstate"] == "d" or art_dic["talk_curstate"] == "d":
                            stt = "избрана"
                            good_count += 1
                        else:
                            continue
                    if art_dic["art_curstate"] == "d":
                        cur_good_count += 1
                    lines += "# Статья [["+art_name+"]] "+stt+" участником [[u:"+art_dic["summator"]+"|"+art_dic["summator"]+"]] "+str(d)+" "+month_dic[sm]+" 20"+str(y)+"\n"
    print(lines)
    print("good: "+str(good_count))
    print("current good: "+str(cur_good_count))
    #ed = editor.Editor("Википедия:Кандидаты в добротные статьи/log")
    #ed.put_art(lines, "try again")


def first_run():
    work_dic = {}
    nonfinish_date_list = ["2011"]
    for y in range(13, 16):
        for m in range(1, 13):
            strm = str(m)
            if len(strm) == 1:
                strm = "0" + strm
            for d in range(1, 32, 1):
                strd = str(d)
                if len(strd) == 1:
                    strd = "0" + strd
                date_str = strd + strm + str(y)
                nonfinish_date_list.append(date_str)
                print(date_str)
    work_dic["nonfinish_date_list"] = nonfinish_date_list
    pickle.dump(work_dic, open("good_data", "wb"))