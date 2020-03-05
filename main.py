import threading
import EGPA_script_random_num
import pandas as pd


def login(username, password, puid, group_id, is_trans):
    EGPA_script_random_num.login(username=username, password=password, puid=puid, group_id=group_id,is_trans=is_trans)


def func():
    data = pd.read_excel("users.xlsx")
    name = data.get("name")
    password = data.get("password")
    puid = data.get("puid")
    group_id = data.get("group_id")
    username = data.get("username")
    is_trans = data.get("trans")

    for i in range(data.__len__()):
        try:
            print(username[i] + " Start")
            t = threading.Thread(target=EGPA_script_random_num.login,
                                 args=(name[i], password[i], puid[i], group_id[i], is_trans[i]))
            # t.setDaemon(True)
            t.start()
            t.join(150)
        except Exception as e:
            print("出错了：", username[i], e)


func()
'''
# 放到服务器上可持久化运行。内存占用极小。
while True:
    time_now = time.strftime("%H:%M", time.localtime())  # 刷新
    print("检测了一次时间",time_now )
    if time_now == "05:30": #此处设置每天定时的时间
        func()
    time.sleep(60)
'''
