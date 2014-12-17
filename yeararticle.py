import editor
import re
import datetime

def stat():
    res = "По состоянию на " + str(datetime.datetime.now().time()) + " " + str(datetime.datetime.now().date()) + "\n\n"
    ed = editor.Editor("Википедия:Статьи года/2014/Голосование")
    data = ed.get_text()
    tmp_list = re.findall("[^=]==[^=]+==[^=]", data)
    nom_list = []
    for unit in tmp_list:
        nom_list.append(re.search("=[^=]+", unit).group()[1:].strip())
    for nom in nom_list:
        #print(nom)
        res += "=== Номинация «"+nom+"» ===\n"
        tmp_data = data[data.find(nom)+len(nom):]
        try:
            tmp_data = tmp_data[:tmp_data.find(re.search("[^=]==[^=]+==[^=]", tmp_data).group())]
        except:
            # last part
            pass
        tmp_list = re.findall("[^=]===[^=]+===[^=]", tmp_data)
        art_list = []
        for unit in tmp_list:
            art_list.append(re.search("\[\[[^\[]+\]\]", unit).group()[2:-2])
        i = 0
        art_dic = {}
        while i < len(art_list):
            art = art_list[i]
            art_data = tmp_data[tmp_data.find(art_list[i]):]
            try:
                art_data = art_data[:art_data.find(art_list[i+1])]
            except:
                pass
            count = len(re.findall("\{\{[Зз]а\}\}", art_data))
            art_dic[art] = count
            #print(str(count) + "  -  " + art)
            i += 1
        counts = sorted(list(set(art_dic.values())), reverse=True)
        top = counts[0]
        pos = 1
        #print(counts)
        res += '{|class="sortable wikitable"\n'
        res += '|-\n'
        res += '! Место !! Статья !! Голосов\n'
        for count in counts:
            if count >= 0:
                for art in art_dic:
                    if art_dic[art] == count:
                        if count == top:
                            res += '|-bgcolor="gold"\n'
                        else:
                            res += '|-\n'
                        #print(str(count) + " - " + art)
                        res += '|align="center"| '+str(pos)+' || [['+art+']] ||align="center"| '+str(count)+'\n'
                        pos += 1
        res += "|}\n\n"
    #print(res)
    ed = editor.Editor("Участник:DZ/СГ2014")
    ed.put_art(res, "update")