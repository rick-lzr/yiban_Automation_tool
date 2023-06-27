from __future__ import unicode_literals, print_function  # python2
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
import urllib

# 全局参数
cookies = "preview_hidden=0; FEED_NEW_VERSION_7130177=1; " \
          "UM_distinctid=16c0a179d9a202-00ff9970083d5f-c343162-189420-16c0a179d9ba7d; FEED_NEW_VERSION_11887100=1; " \
          "__SDID=32a7d854ba36e6af; analytics=b1f4e5c43a3d945d; " \
          "yd_cookie=0d57c30a-cc0a-43a6563366d9896176feb7a6645a9895cbbd; " \
          "_ydclearance=6a3c546f8e9ea03c46001647-43b8-4800-92c8-d27b191c6659-1570102092; " \
          "YB_SSID=d86cca437c8f1feacff03c4823ba6c1f; CNZZDATA1253488264=1474242759-1542784100-null%7C1570091073; " \
          "_cnzz_CV1253488264=%E5%AD%A6%E6%A0%A1%E9%A1%B5%E9%9D%A2%7C%3A%2FIndex%2FLogin%2Findex%7C1570095214636%26" \
          "%E5%AD%A6%E6%A0%A1%E5%90%8D%E7%A7%B0%7C%E5%85%B6%E4%BB%96%7C1570095214636 "

session = ""
Name = ""
User_website = ""
Group_id = ""
Puid = ""
Channel_id = ""
User_id = ""  # 就是userid
Nick = ""
TransMoney = ""
TransAccount = ""  # 欲转入网薪的账户的用户ID
IsTrans = ""


def login(name, username, password, puid, group_id, istrans):
    # 全局变量声明
    global Name
    global Puid
    global Group_id
    global session
    global TransMoney
    global IsTrans
    IsTrans = istrans
    Name = name
    Puid = puid
    Group_id = group_id
    TransMoney = 100
    session = requests.session()

    header = get_html_header("https://www.yiban.cn/login")
    # print(header)
    r = session.get("https://www.yiban.cn/login", headers=header)
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
        login_json = json.loads(login_request(username, encrypt_password, code, data_keys_time))
        # print("login_json")
        # 获取到返回的json数据
        if login_json['code'] == 200:
            start(login_json)
        else:
            if login_json['code'] == '711':
                code = wirte_code("yanzhengma.jpg")
                print(Name + "--使用了验证码，验证码是:", str(code))
                if code == 1:
                    login(name, username, password, puid, group_id, IsTrans)
                    return
                else:
                    login_json = json.loads(login_request(
                        username, encrypt_password, code, data_keys_time))
                if login_json['code'] == '201':
                    login(name, username, password, puid, group_id, IsTrans)
                    return
                elif login_json['code'] == 200:
                    start(login_json)
                    return
                else:
                    print(Name + "--错误码:", login_json['code'], " 原因:", login_json['message'])
                    print("--------------分---割---线--------------")
                    session.close()
            elif login_json['message'] == '用户名或密码错误':
                print(Name + "--用户名或密码错误")
                return
            else:
                print(Name + "--错误码:", login_json['code'], " 原因:", login_json['message'])
                print("--------------分---割---线--------------")
                session.close()
                # print(r.text)
    except TypeError as e:
        f = open('1.html', 'wb')
        text = r.content
        f.write(text)
        f.close()
        print(Name + "--出错了")
        print("--------------分---割---线--------------")
        print(e)
        login(name, username, password, puid, group_id, IsTrans)
        session.close()
        pass


def get_html_header(url):
    res = requests.get(url)
    if res.status_code == 200:
        header = {"cookie": str(res.cookies.get_dict())}
        return header
    soup_script = BeautifulSoup(res.text, "html.parser")
    script = soup_script.find("script")
    scriptStr = script.text
    fun_str = re.search(r'function (..)', scriptStr).group(1)
    param = scriptStr[re.search(fun_str + "\(", scriptStr).end():re.search("....200", scriptStr).start()]
    scriptStr = re.sub(r'window.onload=setTimeout................', "", scriptStr)
    scriptStr = re.sub(r'eval."qo=eval;qo.po.;".;', "return po;", scriptStr)
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
                     data=form_data, allow_redirects=False)
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


def start(login_json):
    print(Name + "--模拟登陆成功")
    info = getInfo(Group_id, Puid)
    # User_id = info['user_id']
    # Nick = info['nick']
    # Group_id = info['group_id']  # 这里是确定用户是在哪一个微社区发动态
    # Puid = info['puid']  # 所属组织（院系）
    # print("获取到的Channel_id为:" + Channel_id)
    # print("获取到的用户id为:" + User_id)
    # print(info)
    # 签到
    qiandao()
    # 发布动态
    # 微社区添加投票*2
    for iii in range(2):
        # addFeed() # 接口调用没有效果并且得不到 feed id
        add_vote()
    # 批量评论 同情 赞动态
    Comments_sympathy_likes()
    # 微社区添加话题*3
    for kkk in range(3):
        addTopic()
    # 点赞并评论微社区所有的话题
    Comment_And_Like_All()
    # 网站\客户端查看(个人/公共/机构账号)主页
    addPersonWebsite()
    # 参与投票[ 投票 + 评论 + 赞]
    Join_Vote()
    # 修改签名
    Change_Sign()
    # 网薪转账 函数内部自带判断是否转移
    # givePresent(info)
    # 博文添加
    # addblog()
    # 添加易喵喵
    # addYiMiaoMiao()
    print(Name + "--执行完毕")
    print("--------------分---割---线--------------")
    session.close()


# 获取通过加密的密码
def get_crypt_password(private_key, password):
    rsa = RSA.importKey(private_key)
    cipher = PKCS1_v1_5.new(rsa)
    ciphertext = encrypt(password, cipher)
    return ciphertext


def encrypt(msg, cipher):
    ciphertext = cipher.encrypt(msg.encode('utf8'))
    return base64.b64encode(ciphertext).decode('ascii')


# 签到
def qiandao():
    info = YiYan()
    form_data = {
        "optionid[]": 12182,
        "input": info
    }
    r = session.post("http://www.yiban.cn/ajax/checkin/answer", data=form_data)
    result_json = json.loads(r.text)
    print(Name + "--签到状态：" + result_json["message"])


# 发布动态
def addFeed():
    info = YiYan()
    form_data = {
        "content": info,
        "privacy": "0",
        "dom": ".js-submit"
    }
    # 自动发表动态
    r = session.post("http://www.yiban.cn/feed/add", data=form_data)
    # print(r.text)
    post_json = json.loads(r.text)

    if post_json['code'] == 200:
        try:
            feedId = str(post_json['data']['feedId'])
            # print("获取到的动态id为:" + feedId)
            # 自动点赞
            session.post("http://www.yiban.cn/feed/up", data={"id": feedId})
            time.sleep(0.2)  # 休眠1秒
            # 自动同情
            session.post("http://www.yiban.cn/feed/down", data={"id": feedId})
            time.sleep(0.2)  # 休眠1秒
            # 自动发表评论
            yiyan = YiYan()
            session.post("http://www.yiban.cn/feed/createComment",
                         data={"id": feedId, "content": yiyan})
            time.sleep(0.2)  # 休眠1秒
            print(Name + "--发布动态完成")
        except:
            addFeed()
    else:
        print(Name + "--动态发表错误....返回信息：", post_json)


# 博文添加
def addblog():
    r = session.get("http://www.yiban.cn" + User_website, timeout=10)
    info = YiYan()
    r = session.post("http://www.yiban.cn/blog/blog/addblog", data={"title": info, "content": info,
                                                                    "ranges": "1", "type": "1",
                                                                    "token": "64d41ba3222a4c4614fc33f594a6df4d",
                                                                    "ymm": "1", "dom": ".js-submit"}, timeout=10)
    post_result = json.loads(r.text)
    if post_result['code'] == 200:
        r = session.get(
            "http://www.yiban.cn/blog/blog/getBlogList?page=1&size=10&uid=" + User_id, timeout=10)
        m_json = json.loads(r.text)
        # print(m_json)
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
                            User_id + "/blogid/" + blog_id, timeout=10)
                # 评论博文
                # blogid: 12300216 oid: 18884862 mid: 48893712 reply_user_id: 0 reply_comment_id: 0 content: 123123123
                session.post("http://www.yiban.cn/blog/blog/addcomment/", data={
                    "blogid": blog_id, "oid": User_id, "mid": Mount_id, "reply_user_id": "0", "reply_comment_id": "0",
                    "content": info}, timeout=10)
                print(Name + "--博文发表成功")
            except Exception:
                print(Name + "--博文发表异常")
        else:
            print(Name + "--获取请求的博文错误...")

            # print("获得blogid:"+blogid)
    else:
        # 需要注意如果请求评论的速度过快会导致弹出验证码.
        print(Name + "--发表博文失败")


# 添加易喵喵
def addYiMiaoMiao():
    randomstr = str(random.randint(100, 99999))
    data_form = {"title": randomstr,
                 "content": randomstr, "kind": '8', "agree": 'true'}
    session.post("http://ymm.yiban.cn/article/index/add", json=data_form, timeout=10)
    # r = session.post("http://ymm.yiban.cn/article/index/add", json=data_form)
    # print(r.text)


# 网站\客户端查看(个人/公共/机构账号)主页
def addPersonWebsite():
    for m in range(2):
        # 查看个人
        session.get("http://www.yiban.cn/user/index/index/user_id/" + str(User_id), timeout=10)
        time.sleep(0.2)  # 休眠1秒
        # 查看机构
        session.get("http://www.yiban.cn/school/index/id/5925583", timeout=10)
        time.sleep(0.2)  # 休眠1秒
        # 查看公共
        session.get("http://www.yiban.cn/user/index/index/user_id/15977811", timeout=10)
        time.sleep(0.2)  # 休眠1秒
        # 查看公共群主页
        # http://www.yiban.cn/newgroup/indexPub/group_id/468396/puid/7644136
        session.get("http://www.yiban.cn/newgroup/indexPub/group_id/" + str(Group_id) + "/puid/" + str(Puid),
                    timeout=10)
        time.sleep(0.2)  # 休眠1秒
    print(Name + "--网站/客户端查看(个人/公共/机构账号/公共群)主页完成")


# 添加话题
def addTopic():
    info = YiYan()
    payload = {
        'puid': Puid,
        'pubArea': Group_id,
        'title': info,
        'content': info,
        'isNotice': 'false',
        'dom': '.js-submit'
    }
    Add_Topic = session.post(
        'https://www.yiban.cn/forum/article/addAjax', data=payload, timeout=10)
    return Add_Topic.json()['message']


# 修改签名
def Change_Sign():
    yy = YiYan()
    session.post("http://www.yiban.cn/user/info/signature", data={"signature": yy}, timeout=10)
    print(Name + "--修改签名成功")


# 添加投票
def add_vote():
    info1 = YiYan()
    info2 = YiYan()
    info3 = YiYan()
    info4 = YiYan()
    payload = {
        'puid': Puid,
        'group_id': Group_id,
        'scope_ids': Group_id,
        'title': info1,
        'subjectTxt': info2,
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
        'subjectTxt_1': info3,
        'subjectTxt_2': info4,
        'rsa': 1,
        'dom': '.js-submit'
    }

    session.post('https://www.yiban.cn/vote/vote/add',
                 data=payload, timeout=10)
    print(Name + "--添加投票已经完成")


# 批量评论 同情 赞动态
def Comments_sympathy_likes():
    # 取动态ID
    data = {
        'user_id': User_id,
        'lastid': 0,
        'num': 10,
        'topic_content': '',
        'scroll': 1
    }
    res = session.post('http://www.yiban.cn/feed/list', data=data, timeout=10)
    # print(res.text)
    js_res = res.json()
    for i in range(len(js_res['data'])):
        feedid = js_res['data'][i]['_id']
        # 自动点赞
        up_res = session.post("http://www.yiban.cn/feed/up", data={"id": feedid})
        time.sleep(0.2)  # 休眠1秒
        # 自动同情
        down_res = session.post("http://www.yiban.cn/feed/down", data={"id": feedid})
        time.sleep(0.2)  # 休眠1秒
        # 自动发表评论
        yiyan = YiYan()
        creatComment_res = session.post("http://www.yiban.cn/feed/createComment", data={"id": feedid, "content": yiyan})
        time.sleep(0.2)  # 休眠1秒
        # print("up_res:", up_res.text, "\ndown_res:", down_res.text, "\ncreatComment_res", creatComment_res.text)
        print(Name + "--第[ " + str(i + 1) + " ]次 赞/同情/评论动态")
    print(Name + "--批量评论/同情/赞动态完成")


# 网薪转账
def givePresent(info):
    global TransMoney
    user_money = info["user_money"]
    print(Name + "--当前网薪：" + user_money)
    if int(TransMoney) == 1:
        if int(user_money) > 100:
            money = user_money[:len(user_money) - 2] + "00"
            # money = "100"
            from_data = {
                "to_user_id": TransAccount,
                "amount": money
            }
            session.post("http://www.yiban.cn/ajax/user/givePresent", data=from_data, timeout=10)
            # givePresent_res = session.post("http://www.yiban.cn/ajax/user/givePresent", data=from_data)
            # print(givePresent_res.content)
            print(Name + "--转帐 [" + money + "]")
    pass


# 评论并点赞微社区当前页所有的动态
def Comment_And_Like_All():
    Article_Idinfo = Get_AllArticle_Id()
    # 点赞动态
    for i in Article_Idinfo:
        # 点赞
        payload1 = {
            'article_id': i,
            'channel_id': Channel_id,
            'puid': Puid
        }
        session.post('https://www.yiban.cn/forum/article/upArticleAjax', data=payload1)
        time.sleep(0.2)  # 休眠1秒
        # 评论
        yy = YiYan()
        payload2 = {
            'channel_id': Channel_id,
            'puid': Puid,
            'article_id': i,
            'content': yy,
            'reply_id': "0",
            'syncFeed': "1",
            'isAnonymous': "0"
        }
        session.post('https://www.yiban.cn/forum/reply/addAjax', data=payload2)
        time.sleep(0.2)  # 休眠1秒
    print("评论并点赞微社区当前页所有的动态--完成")


# 取微社区所有最新第一页动态的Article_Id
def Get_AllArticle_Id():
    # print(Channel_id)
    # print(Puid)
    # print(Group_id)
    payload1 = {
        'puid': Puid,
        'group_id': Group_id,

    }
    res = session.post('http://www.yiban.cn/forum/article/listAjax', data=payload1)
    # print(res.content)
    js_res = res.json()
    # print(js_res)
    data_list = js_res['data']['list']
    # print(data_list)
    article_id = []
    for items in data_list:
        id = items['id']
        # print(id)
        article_id.append(id)
    return article_id


# 参与投票[ 投票 + 评论 + 赞]
def Join_Vote():
    vote_id = Get_All_V_Id()
    actor_id = Get_All_A_Id()  # 作者的ID
    for i in range(len(vote_id)):
        # 获取voption_id  mount_id
        data0 = {
            'vote_id': vote_id[i],
            'uid': User_id,
            'puid': Puid,
            'pagetype': 1,
            'group_id': Group_id,
            'actor_id': User_id,
            'top_power': 'f',
            'edit_power': 'f',
            'end_power': 'f',
            'del_power': 'f',
            'block_power': 'f',
            'isSchoolVerify': 1,
            'is_public': 'f',
            'is_anonymous': 'f',
            'token': '',
            'out_power': 'f',
            'isMember': '',
            'url[getVoteDetail]': 'vote/vote/getVoteDetail',
            'url[output]': '/vote/Expand/output',
            'url[getCommentDetail]': 'vote/vote/getCommentDetail',
            'url[addComment]': 'vote/vote/addComment',
            'url[editLove]': 'vote / vote / editLove',
            'url[vote]': 'vote/vote/act',
            'url[setIsTop]': 'vote/Expand/setIsTop',
            'url[setManualEndVote]': 'vote/Expand/setManualEndVote',
            'url[delVote]': 'vote/Expand/delVote',
            'url[delComment]': 'vote/vote/delComment',
            'url[shieldVote]': 'vote/Expand/shieldVote',
            'url[getAnonymous]': 'vote/Expand/getAnonymous',
            'url[userInfo]': 'user/index/index',
            'isLogin': 1,
            'isOrganization': 0,
            'ispublic': 0
        }
        res0 = session.post('https://www.yiban.cn/vote/vote/getVoteDetail', data=data0)
        js_res0 = res0.json()
        # print(js_res)
        V_option_id = js_res0['data']['option_list'][0]['id']
        # print(V_option_id)
        # mount_id
        mount_id = js_res0['data']['vote_list']['Mount_id']
        # print(mount_id)
        time.sleep(0.2)  # 休眠1秒
        # 对投票评论
        yy = YiYan()
        data = {
            'mountid': mount_id,
            'msg': yy,
            'group_id': Group_id,
            'actor_id': User_id,  # 自己的ID
            'vote_id': vote_id[i],
            'author_id': actor_id[i],  # 发起投票的人的actor_id
            'puid': Puid,
            'reply_comment_id': 0,
            'reply_user_id': 0
        }
        session.post('https://www.yiban.cn/vote/vote/addComment', data=data)
        # print(str(i) + "--对投票评论返回值：" + str(res000))
        time.sleep(0.2)  # 休眠1秒
        # 投票
        data3 = {
            'puid': Puid,
            'group_id': Group_id,
            'vote_id': vote_id[i],
            'actor_id': User_id,
            'voptions_id': V_option_id,
            'minimum': 1,
            'scopeMax': 1
        }
        session.post('https://www.yiban.cn/vote/vote/act', data=data3)
        # print(str(i) + "--投票返回值：" + str(res001))
        # 赞投票
        data4 = {
            'puid': Puid,
            'group_id': Group_id,
            'vote_id': vote_id[i],
            'actor_id': User_id,  # 自己的id
            'flag': 1
        }
        session.post('https://www.yiban.cn/vote/vote/editLove', data=data4)
        time.sleep(0.2)  # 休眠0.2秒
        print(Name + "--第[ " + str(i + 1) + " ]次参与微社区投票:投票+评论+赞")
    print(Name + "--批量参与微社区投票:投票+评论+赞 完毕")


# 获取投票的vote_id
def Get_All_V_Id():
    global Group_id
    global Puid
    url = 'http://www.yiban.cn/newgroup/showMorePub/puid/' + str(Puid) + '/group_id/' + str(Group_id) + '/type/3'
    html = session.get(url)
    # print(html.content)
    soup = BeautifulSoup(html.content, 'html.parser')
    A = []
    for span in soup.find_all('span', class_='tx'):
        # print(span)
        m_url = span.find('a').get('href')
        voteid = str(m_url)[str(m_url).find("vote_id/") + 8:str(m_url).find("/puid")]
        A.append(voteid)
    return A


# 获取投票的作者id
def Get_All_A_Id():
    global Group_id
    global Puid
    url = 'http://www.yiban.cn/newgroup/showMorePub/puid/' + str(Puid) + '/group_id/' + str(Group_id) + '/type/3'
    html = session.get(url)
    # print(html.content)
    soup = BeautifulSoup(html.content, 'html.parser')
    B = []
    for span in soup.find_all('span', class_='tx'):
        # print(span)
        m_url = span.find('a').get('href')
        actorid = str(m_url)[str(m_url).find("actor_id/") + 9:str(m_url).find("/status")]
        B.append(actorid)
    return B


#  一言
def YiYan():
    headers = {'User-Agent':'Mozilla/5.0 3578.98 Safari/537.36'}
    url = urllib.request.Request("https://v1.hitokoto.cn/", headers=headers)
    try:
        data = urllib.request.urlopen(url)
        jsdate = json.loads(data.read())
        yiyan = jsdate["hitokoto"]
        '''info = {id,hitokoto,cat,catname,author,source,date'''
        return yiyan
    except urllib.error.HTTPError as e:
        print("yiban_Automation_tool:如果我报错了，请在GitHub上联系原作者：", e)
        yiyan = "学院加油，每日签到"
        return yiyan


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
        'https://www.yiban.cn/forum/api/getListAjax', data=payload)
    channel_id = Get_Channel_Info.json()['data']['channel_id']
    Get_User_Info = session.post(
        'https://www.yiban.cn/ajax/my/getLogin')
    actor_id = Get_User_Info.json()['data']['user']['id']
    nick = Get_User_Info.json()['data']['user']['nick']
    # 取网薪值
    html_res = session.post("http://www.yiban.cn/user/index/index/user_id/" + actor_id)
    soup = BeautifulSoup(html_res.content, 'html.parser')
    user_money_span = soup.find("span", id="user-money")
    str_begin = str(user_money_span).find(">")
    str_end = str(user_money_span).find("</")
    user_money = str(user_money_span)[str_begin + 1:str_end]
    # print( user_money_span)
    info = {
        'group_id': group_id,
        'puid': puid,
        'channel_id': channel_id,
        'actor_id': actor_id,
        'nick': nick,
        'user_money': user_money
    }
    return info

"""登陆时调用的函数。可以从这里使用login开始调试"""
# login("账号", "密码", 'puid', 'groupid', 'istrans')
