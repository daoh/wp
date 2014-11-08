import datetime


def get_date():
    now_datetime = datetime.datetime.now()
    now_date = now_datetime.strftime("%d.%m.%y")
    return now_date