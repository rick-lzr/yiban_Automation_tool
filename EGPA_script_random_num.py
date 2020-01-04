from __future__ import unicode_literals, print_function  # python2

import urllib

import datetime
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from bs4 import BeautifulSoup
import captcha_test
import CSDN_OCR
import base64
import requests
import json
import random
import time
import execjs
import re

# 当前的session会话对象

# 登录操作
cookies = "preview_hidden=0; FEED_NEW_VERSION_7130177=1; " \
          "UM_distinctid=16c0a179d9a202-00ff9970083d5f-c343162-189420-16c0a179d9ba7d; FEED_NEW_VERSION_11887100=1; " \
          "__SDID=32a7d854ba36e6af; analytics=b1f4e5c43a3d945d; " \
          "yd_cookie=0d57c30a-cc0a-43a6563366d9896176feb7a6645a9895cbbd; " \
          "_ydclearance=6a3c546f8e9ea03c46001647-43b8-4800-92c8-d27b191c6659-1570102092; " \
          "YB_SSID=d86cca437c8f1feacff03c4823ba6c1f; CNZZDATA1253488264=1474242759-1542784100-null%7C1570091073; " \
          "_cnzz_CV1253488264=%E5%AD%A6%E6%A0%A1%E9%A1%B5%E9%9D%A2%7C%3A%2FIndex%2FLogin%2Findex%7C1570095214636%26" \
          "%E5%AD%A6%E6%A0%A1%E5%90%8D%E7%A7%B0%7C%E5%85%B6%E4%BB%96%7C1570095214636 "
user_website = ""
user_id = ""
group_id = ""
puid = ""
channel_id = ""
actor_id = ""
nick = ""


def login(username, password, banji):
    global session
    session = requests.session()
    header = get_html_header("https://www.yiban.cn/login")
    # print(header)
    r = session.get("https://www.yiban.cn/login", headers=header, timeout=12)
    soup = BeautifulSoup(r.text, "html.parser")
    ul = soup.find("ul", id="login-pr")
    # 从html当中获取私钥
    try:
        data_keys = ul['data-keys']
        # 从html当中获取时间
        data_keys_time = ul['data-keys-time']
        code = ""
        # 获取到验证码
        encrypt_password = get_crypt_password(data_keys, password)
        # print("login_json")
        login_json = json.loads(login_request(
            username, encrypt_password, code, data_keys_time))
        # 获取到返回的json数据
        if login_json['code'] == 200:
            start(login_json, banji)
        else:
            if login_json['code'] == '711':
                code = wirte_code("yanzhengma.jpg")
                print("使用了验证码，验证码是:", code)
                if code == 1:
                    login(username=username, password=password, banji=banji)
                    return
                else:
                    login_json = json.loads(login_request(
                        username, encrypt_password, code, data_keys_time))
                if login_json['code'] == '201':
                    login(username=username, password=password, banji=banji)
                    return
                elif login_json['code'] == 200:
                    start(login_json, banji)
                    return
                else:
                    print("错误码:", login_json['code'], " 原因:", login_json['message'])
                    session.close()
            else:
                print("错误码:", login_json['code'], " 原因:", login_json['message'])
                session.close()
                # print(r.text)
    except TypeError:
        f = open('1.html', 'wb')
        text = r.content
        f.write(text)
        f.close()
        print(username, "出错了")
        login(username, password, banji)
        session.close()
        pass


def get_html_header(url):
    res = requests.get(url, timeout=12)
    # print(res) 861500
    if res.status_code == 200:
        header = {"cookie": str(res.cookies.get_dict())}
        # print(res.cookies.get_dict(), "this is cookie dict")
        return header
    soup_script = BeautifulSoup(res.text, "html.parser")
    script = soup_script.find("script")
    scriptStr = script.text
    fun_str = re.search(r'function (..)', scriptStr).group(1)
    param = scriptStr[re.search(fun_str + "\(", scriptStr).end():re.search("....200", scriptStr).start()]
    # print(fun_str, param)
    scriptStr = re.sub(r'window.onload=setTimeout................', "", scriptStr)
    scriptStr = re.sub(r'eval."qo=eval;qo.po.;".;', "return po;", scriptStr)
    # print(url)
    # print(scriptStr)
    ctx = execjs.compile(scriptStr)
    fun_res = ctx.call(fun_str, param)
    cookies = fun_res.replace("document.cookie='", "")
    cookies = cookies.replace("'; window.document.location=document.URL", "")
    header = {"cookie": cookies}
    # print("get 到了cookies")
    return header


def cookie2session(cookies):
    if cookies == "":
        return session
    for i in cookies:
        cookie = {'name': i['name'].replace(" ", ""), 'value': i["value"]}
        session.cookies.set(cookie.get("name"), cookie.get("value"))
    # print("session的cookie已装填好准备签到")
    return session


def ParseCookiestr(cookie_str):
    cookielist = []
    # print(cookie_str,"this is str")
    if cookie_str == "{}":
        return cookielist
    for item in cookie_str.split(';'):
        cookie = {}
        itemname = item.split('=')[0]
        iremvalue = item.split('=')[1]
        cookie['name'] = itemname
        cookie['value'] = urllib.parse.unquote(iremvalue)
        cookielist.append(cookie)
    return cookielist


def login_request(username, encrypt_password, code, data_keys_time):
    form_data = {
        'account': username,
        'password': encrypt_password,
        'captcha': code,
        'keysTime': data_keys_time
    }
    # print(form_data)
    cookie_str = get_html_header("https://www.yiban.cn/login/doLoginAjax")
    # print(cookie_str, "143")
    cookies = ParseCookiestr(cookie_str=cookie_str.get("cookie"))
    session = cookie2session(cookies)
    r = session.post("https://www.yiban.cn/login/doLoginAjax",
                     data=form_data, allow_redirects=False, timeout=12)
    # print(r.text)
    return r.text


# 验证码保存


def wirte_code(saveUrl):
    r = session.get("https://www.yiban.cn/captcha/index?" +
                    (str(int(time.time()))))
    with open(saveUrl, 'wb') as f:
        f.write(r.content)
    captcha_test.automation(r'yanzhengma.jpg')
    code = CSDN_OCR.Recognise(r'transfered_image.jpg')

    # code = quote(code, safe=string.printable)
    return code


def start(login_json, banji):
    print("模拟登陆成功")
    print(login_json)
    user_website = login_json['data']['url']
    user_id = get_user_id()
    print("获取到的用户id为:" + user_id)

    global group_id
    global puid
    global channel_id
    global actor_id
    global nick

    info = getInfo(group_id=group_id, puid=puid)

    channel_id = info['channel_id']
    actor_id = info['actor_id']
    nick = info['nick']
    group_id = info['group_id']  # 这里是确定用户是在哪一个微社区发动态的如果需要确定则请自己填写
    puid = info['puid']  # 所属组织（院系）

    print(info)

    qiandao()
    # 循环四次.
    for i in range(1):
        # addFeed()
        addTopic()
        addPersonWebsite()
        # addblog()
        # addYiMiaoMiao()
        add_vote()
        print("执行一轮完成.等待下一轮执行")
        time.sleep(2)
    session.close()


def get_user_id():
    r = session.get("http://www.yiban.cn/my/feed", timeout=12)
    soup = BeautifulSoup(r.text, "html.parser")
    span = soup.find_all("span", class_="user-account")[0]
    return str(span)[str(span).index("user_id/") + 8:str(span).index("user_id/") + 16]


# 获取通过加密的密码
def get_crypt_password(private_key, password):
    rsa = RSA.importKey(private_key)
    cipher = PKCS1_v1_5.new(rsa)
    ciphertext = encrypt(password, cipher)
    return ciphertext


def encrypt(msg, cipher):
    ciphertext = cipher.encrypt(msg.encode('utf8'))
    return base64.b64encode(ciphertext).decode('ascii')


def qiandao():
    form_data = {
        "optionid[]": 12182,
        "input": ""
    }
    r = session.post("http://www.yiban.cn/ajax/checkin/answer", data=form_data)
    result_json = json.loads(r.text)
    print(result_json["message"])


# 发布动态(完成)
def addFeed():
    # randomstr = str(random.randint(100, 99999))
    randomstr = "今天是{today}又在易班上签到了，好开心啊....哈哈哈".format(today=datetime.date.today())
    form_data = {
        "content": randomstr,
        "privacy": "0",
        "dom": ".js-submit"
    }
    # 自动发表动态
    r = session.post("http://www.yiban.cn/feed/add", data=form_data)
    print(r.text)
    post_json = json.loads(r.text)
    if post_json['code'] == 200:
        try:
            feedId = str(post_json['data']['feedId'])
            print("获取到的动态id为:" + feedId)
            # 自动点赞
            session.post("http://www.yiban.cn/feed/up", data={"id": feedId})
            # 自动同情
            session.post("http://www.yiban.cn/feed/down", data={"id": feedId})
            # 自动发表评论
            comment_random = str(random.randint(100, 99999))
            session.post("http://www.yiban.cn/feed/createComment",
                         data={"id": feedId, "content": comment_random})
            print("动态相关的网薪完成.")
        except:
            addFeed()
    else:
        print("动态发表错误....")


# 博文添加


def addblog():
    r = session.get("http://www.yiban.cn" + user_website)
    randomstr = str(random.randint(100, 99999))
    r = session.post("http://www.yiban.cn/blog/blog/addblog", data={"title": randomstr, "content": randomstr,
                                                                    "ranges": "1", "type": "1",
                                                                    "token": "64d41ba3222a4c4614fc33f594a6df4d",
                                                                    "ymm": "1", "dom": ".js-submit"})
    post_result = json.loads(r.text)
    if post_result['code'] == 200:
        global user_id
        r = session.get(
            "http://www.yiban.cn/blog/blog/getBlogList?page=1&size=10&uid=" + user_id)
        m_json = json.loads(r.text)
        print(m_json)
        if m_json['code'] == 200:
            try:
                if m_json["data"]["count"] == 0:
                    # 判断数量是否为空
                    return
                m_json = m_json["data"]["list"][0]
                blog_id = m_json['id']
                Mount_id = m_json['Mount_id']
                # 博文点赞
                session.get("http://www.yiban.cn/blog/blog/addlike/uid/" +
                            user_id + "/blogid/" + blog_id)
                # 评论博文
                # blogid: 12300216 oid: 18884862 mid: 48893712 reply_user_id: 0 reply_comment_id: 0 content: 123123123
                session.post("http://www.yiban.cn/blog/blog/addcomment/", data={
                    "blogid": blog_id, "oid": user_id, "mid": Mount_id, "reply_user_id": "0", "reply_comment_id": "0",
                    "content": randomstr})
                print("博文发表成功")
            except Exception:
                print("博文发表异常")
        else:
            print("获取请求的博文错误...")

            # print("获得blogid:"+blogid)
    else:
        # 需要注意如果请求评论的速度过快会导致弹出验证码.
        print("发表博文失败")


# 添加易喵喵


def addYiMiaoMiao():
    randomstr = str(random.randint(100, 99999))
    data_form = {"title": randomstr,
                 "content": randomstr, "kind": '8', "agree": 'true'}
    r = session.post("http://ymm.yiban.cn/article/index/add", json=data_form)
    print(r.text)


# 网站\客户端查看(个人/公共/机构账号)主页
def addPersonWebsite():
    # 查看个人
    session.get("http://www.yiban.cn/user/index/index/user_id/" + user_id, timeout=12)
    # 查看机构
    session.get("http://www.yiban.cn/school/index/id/5000090", timeout=12)
    # 查看公共
    session.get("http://www.yiban.cn/user/index/index/user_id/15977811", timeout=12)
    print("网站\客户端查看(个人/公共/机构账号)主页完成")


# 添加话题


def addTopic():
    # randomstr = str(random.randint(100, 99999))
    randomstr = "坚持每天话题签到"
    payload = {
        'puid': puid,
        'pubArea': group_id,
        'title': randomstr,
        'content': randomstr,
        'isNotice': 'false',
        'dom': '.js-submit'
    }

    Add_Topic = session.post(
        'https://www.yiban.cn/forum/article/addAjax', data=payload, timeout=10)
    return Add_Topic.json()['message']


'''
获取群组信息
返回 JSON 字典
'''


def getInfo(group_id, puid):
    payload = {
        'puid': puid,
        'group_id': group_id
    }

    Get_Channel_Info = session.post(
        'https://www.yiban.cn/forum/api/getListAjax', data=payload, timeout=10)
    channel_id = Get_Channel_Info.json()['data']['channel_id']

    Get_User_Info = session.post(
        'https://www.yiban.cn/ajax/my/getLogin', timeout=10)
    actor_id = Get_User_Info.json()['data']['user']['id']
    nick = Get_User_Info.json()['data']['user']['nick']

    info = {
        'group_id': group_id,
        'puid': puid,
        'channel_id': channel_id,
        'actor_id': actor_id,
        'nick': nick
    }

    return info


def add_vote():
    # randomstr = str(random.randint(100, 99999))
    randomstr = "是否应该坚持每天发投票？"
    payload = {
        'puid': puid,
        'group_id': group_id,
        'scope_ids': group_id,
        'title': randomstr,
        'subjectTxt': randomstr,
        'subjectPic': None,
        'options_num': 2,
        'scopeMin': 1,
        'scopeMax': 1,
        'minimum': 1,
        'voteValue': time.strftime("%Y-%m-%d %H:%M", time.localtime(1893427200)),
        'voteKey': 2,
        'public_type': 0,
        'isAnonymous': 0,
        "voteIsCaptcha": 0,
        'istop': 1,
        'sysnotice': 2,
        'isshare': 1,
        'subjectTxt_1': randomstr,
        'subjectTxt_2': randomstr,
        'rsa': 1,
        'dom': '.js-submit'
    }

    session.post('https://www.yiban.cn/vote/vote/add',
                 data=payload, timeout=10)
    print("添加投票已经完成")


"""登陆时调用的函数。可以从这里使用login开始调试"""
# login('您自己的账号', '密码', "班级") #  最后一个参数是年级和班级，如果没有需要确定的话就可以不需要管他。
# 如果有要求发动态到指定的微社区，则需要确定年级和班级，然后再根据年级和班级确定group_id和puid在start(方法中)
# 班级参数需要自己映射。如果不自己确定我源码中写好的是在我的群页面的第一个群为用户发微社区的群

# except Exception:
#     print("程序异常,登录失败.")
# addblog()
# str = """{"code":200,"message":"\u64cd\u4f5c\u6210\u529f","data":{"url":"\/user\/index\/index\/user_id\/18884862"}}"""
# m = json.loads(str)x
# print(m['code'])72c737918b586744d88347de2a58ee75
