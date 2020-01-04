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
不需要特别的环境搭建就先run  EGPA_script_random_num.py这个文件吧。然后就知道需要哪些包文件了
提示需要哪些包之后就

`pip install xxx`

就可以。不过还是需要注意的是，有些包文件是别名的。
例：`execjs`这个包文件不能pip install execjs的..好像。读者可以试一下。如果不
行可以baidu：安装execjs。这里就不再给出requirement.txt文件。


#### 运行
> ##### 单例测试运行
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

xuehao|username|name|password
---|:--:|:--:|---:
学号|用户名字|易班账号|密码
2017xxxxx|X某某|177******|123456


第一次写GitHub项目如有不详细的还请原谅。/xk 

如果你喜欢欢迎`start`也欢迎`issue`
##### Time :Version 1.0 2020/1/4 提交了requests版本 