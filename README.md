># yiban_自动化工具

这是一个易班的自动化工具，使用python实现。实现方法有两种，一种是大部分采用requests包实现网络请求->该包内可以实现登陆，和登陆后一切不需要验证码的东西。另一种是使用Selenium实现模拟浏览器点击实现自动化运行->可以实现登陆及登陆以后的所有事情（可破解验证码）。

---
>## requests版本
#### 目录结构
```
--requests_root
 |-captcha_test.py // 实现了验证码的处理
 |-CSDN_OCR.py // OCR调用百度api实现识别处理后的验证码
 |-EGPA_scripy_random_num.py //主要运行文件，可尝试调试。方法见后面...
 |-js_test.py // 实现了易班有点反爬的。这里的test实现了破解。是一个小demo于项目整体运行无用
 |-main.py // 可实现批量化运行。
```

#### 环境
TimeStamp：20201023 8.33 给出了requirements.txt 文件
> 环境安装

1、python环境安装
```
cd yiban_Automation_tool
pip install requirements.txt
```
2、js环境安装

因为该程序使用了PyExecJS，所以需要安装一个js运行环境。比如node等，都可以。我安装的node。你想换一个也行，百度：PyExecJs安装js环境即可搜索出更多的适用的环境

如果使用requirements.txt下载出现问题：一些有关的包下载现在给出[链接](https://sadtomlzr.github.io/2020/04/21/python%E5%A5%87%E6%80%AA%E7%9A%84%E5%8C%85%E7%9A%84%E5%AE%89%E8%A3%85%E6%95%B4%E7%90%86/)。


#### 运行
> ##### 单例测试运行
> 注：需要安装js环境（如node.js）
> EGPA_script_random_num.py -p 431有详细注释：
>
>"""登陆时调用的函数。可以从这里使用login开始调试"""
>
> login('您自己的账号', '密码', "班级")
最后一个参数是年级和班级，如果没有需要确定的话就可以不需要管他。
如果有要求发动态到指定的微社区，则需要确定年级和班级，然后再根据年级和班级确定group_id和puid在start(方法中)
班级参数需要自己映射到微社区的班级号->group_id。如果不自己确定我源码中写好的是在我的群页面的第一个群为用户发微社区的群
>
>这里CSDN_OCR文件下面也有一个`print(Recognise("transfered_image.jpg"))`方法..可以实现模块调试
因为要调用baidu的api所以还需要使用者在[百度通用字识别](https://ai.baidu.com/tech/ocr/general)注册自己的账号
并且将CSDN_OCR.py 文件中的 p-103 p-104 ak和sk填写自己的

> ##### 长时间服务器定时任务运行
> 使用的是main.py 文件可放置在服务器上实现自动每天登陆签到如果EGPA_script_random_num.py
文件可以直接使用了，那么就可以将数据写到user.xlsx表中运行`main.py`即可运行
>
>这里需要一个user.xslx 表头是，如下含义

username|name|password|puid|group_id|trans
---|:--:|:--:|:--:|:--:|---:
可以写账号人的姓名仅作显示用，未参加核心运行任务|账号|密码|院系编号|群组号|是否转网薪（1为可以，但要在代码里面开启，并填写自己的信息一般不做使用）
X某某|177******|xxxxx|123456|123456|2

[puid和group_id获取的地方](puid_groupid.png)
如图即可在自己的微社区里面就可以看到这个链接

如果你喜欢欢迎`start`也欢迎`issue`
### 有疑问请issue。（很重要）
##### Time :Version 1.0 2020/1/4 提交了requests版本  
有问题请尽量issue。我会尽量解决你的问题的。这样别人看到了得话就会根据issue来个更正自己的错误。谢谢！

> release有exe版本，可直接按照说明使用下载请点击上部release。下载速度太慢可移步到[gitee]("https://gitee.com/lzr9/yiban_Automation_tool/releases/V0.1.1")
https://gitee.com/lzr9/yiban_Automation_tool/releases/V0.1.1

##### 特别感谢[Eunsolfs](https://github.com/Eunsolfs "Eunsolfs的GitHub")
##### 这里使用了一言的api接口。有兴趣的小伙伴希望能够赞助他们一下。感谢！因为一直白嫖会让人家破产的。我们就只能每天发固定的东西了！不能发不一样的东西了。[附上链接](https://hitokoto.cn/)
----
[python代码版更新版详解。](https://sadtomlzr.github.io/2020/04/09/%E6%80%8E%E6%A0%B7%E5%88%B7%E6%98%93%E7%8F%AD%EF%BC%9F/)

[发行版使用手册。](https://sadtomlzr.github.io/2020/04/01/About-how-to-use-yiban-automation-tool/)

[蓝奏云下载地址](https://sadtom.lanzous.com/b015d4v0f)密码:aq6n


