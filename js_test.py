import re

import execjs
import requests
from bs4 import BeautifulSoup
'''
yiban.cn使用了js反爬虫，这里是一个demo可以看一下。帮助了解源码
'''
session = requests.session()
res = requests.get("https://www.yiban.cn/login")
soup_script = BeautifulSoup(res.text, "html.parser")
script = soup_script.find("script")
scriptStr = script.text
fun_str = re.search(r'function (..)', scriptStr).group(1)
param = scriptStr[re.search(fun_str + "\(", scriptStr).end():re.search("....200", scriptStr).start()]
print(fun_str, param)
scriptStr = re.sub(r'window.onload=setTimeout.................', "", scriptStr)
scriptStr = re.sub(r'eval."qo=eval;qo.po.;".;', "return po;", scriptStr)
ctx = execjs.compile(scriptStr)
fun_res = ctx.call(fun_str, param)
cookies = fun_res.replace("document.cookie='", "")
cookies = cookies.replace("'; window.document.location=document.URL", "")
header = {"cookie": cookies}
r = session.get("https://www.yiban.cn/login", headers=header)
print(r)
