import threading
from threading import Timer

import EGPA_script_random_num
import pandas as pd
import numpy as np
import time

from timeout_decorator import timeout

'''
:param row[0]代表name ， row[1]代表password
'''


def login(username, password, banji):
    EGPA_script_random_num.login(username=username, password=password, banji=banji)


def func():
    data = pd.read_excel("users.xlsx")
    name = data.get("name")
    password = data.get("password")
    xuehao = data.get("xuehao")
    for i in range(data.__len__()):
        try:
            print(xuehao[i], "开始了")
            banji = str(xuehao[i])[0:4] + str(xuehao[i])[8:10]
            t = threading.Thread(target=EGPA_script_random_num.login, args=(name[i], password[i], banji))
            t.setDaemon(True)
            t.start()
            t.join(100)
        except Exception as e:
            print("出错了：", xuehao[i], e)


while True:
    time_now = time.strftime("%H:%M", time.localtime())  # 刷新
    print("检测了一次时间",time_now )
    if time_now == "05:30": #此处设置每天定时的时间
        func()
    time.sleep(60)
    
