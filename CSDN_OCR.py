# !/user/bin/env Python3
# -*- coding:utf-8 -*-

"""
file：baidu_api.py
create time:2019/4/10 15:14
author:Loong Xu
desc: 调用百度OCRapi实现文本识别
"""
import base64
from urllib import parse, request
import json


def GetAccessToken(ak, sk):
    '''
    获取access_token代码
    :param ak:控制台应用API Key
    :param sk:控制台应用Secret Key
    :return:返回接口调用的access_token参数以及token的有效期（单位为秒）
    '''
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s' % (
        ak, sk)
    headers = {'Content-Type': 'application/json; charset=UTF-8'}
    req = request.Request(method='GET', url=host, headers=headers)
    response = request.urlopen(req)
    if (response.status == 200):
        data = json.loads(response.read().decode())
        access_token = data['access_token']
        expires_in = data['expires_in']
        return access_token, expires_in


def RecogniseForm(access_token, image, templateSign=None, classifierId=None):
    """
    自定义模板文字识别
    :param access_token:
    :param image:图像数据（string），base64编码，注意大小不超过4M，最短边至少15px，最长边最大4096px，支持jpg/png/bmp格式
    :param templateSign:模板ID（string）
    :param classifierId:分类器ID（int），这个参数与templateSign至少存在一个，优先使用templateSign，存在templateSign时，使用指定模板；如果没有templateSign而有classifierld，表示使用分类器去判断使用模板
    :return:返回识别结果
    """
    host = 'https://aip.baidubce.com/rest/2.0/solution/v1/iocr/recognise?access_token=%s' % access_token
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    formdata = {'image': image}
    if templateSign is not None:
        formdata['templateSign'] = templateSign
    if classifierId is not None:
        formdata['classifierId'] = classifierId
    data = parse.urlencode(formdata).encode('utf8')
    req = request.Request(method='POST', url=host, headers=headers, data=data)
    response = request.urlopen(req)
    if (response.status == 200):
        jobj = json.loads(response.read().decode())
        datas = jobj['data']
        recognise = {}
        for obj in datas['ret']:
            recognise[obj['word_name']] = obj['word']
        return recognise


def RecogniseGeneral(access_token, image=None, url=None, recognize_granularity='big', language_type='CHN_ENG',
                     detect_direction=False, detect_language=False, vertexes_location=False, probability=False):
    '''
    通用文字识别（含位置信息）
    :param access_token:URL参数，需要拼接到接口URL上
    :param image:图像数据，base64编码，要求base64编码后大小不超过4M，最短边至少15px，最长边最大4096px,支持jpg/png/bmp格式，当image字段存在时url字段失效
    :param url:图片完整URL，URL长度不超过1024字节，URL对应的图片base64编码后大小不超过4M，最短边至少15px，最长边最大4096px,支持jpg/png/bmp格式，当image字段存在时url字段失效，不支持https的图片链接
    :param recognize_granularity:是否定位单字符位置，big：不定位单字符位置，默认值；small：定位单字符位置
    :param language_type:识别语言类型，默认为CHN_ENG。可选值包括：- CHN_ENG：中英文混合；- ENG：英文；- POR：葡萄牙语；- FRE：法语；- GER：德语；- ITA：意大利语；- SPA：西班牙语；- RUS：俄语；- JAP：日语；- KOR：韩语
    :param detect_direction:是否检测图像朝向，默认不检测，即：false。朝向是指输入图像是正常方向、逆时针旋转90/180/270度。可选值包括:- true：检测朝向；- false：不检测朝向。
    :param detect_language:是否检测语言，默认不检测。当前支持（中文、英语、日语、韩语）
    :param vertexes_location:是否返回文字外接多边形顶点位置，不支持单字位置。默认为false
    :param probability:是否返回识别结果中每一行的置信度
    :return:
    '''
    host = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=%s' % access_token
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    formdata = {'recognize_granularity': recognize_granularity,
                'detect_direction': detect_direction, 'detect_language': detect_language,
                'vertexes_location': vertexes_location, 'probability': probability}
    if image is not None:
        formdata['image'] = image
    elif url is not None:
        formdata['url'] = url
    data = parse.urlencode(formdata).encode('utf8')
    req = request.Request(method='POST', url=host, headers=headers, data=data)
    response = request.urlopen(req)
    # print(response.read())
    if response.status == 200:
        jobj = json.loads(response.read().decode())
        if jobj.get("words_result_num") != 0:
            return jobj.get("words_result")[0].get("words")
        else:
            print("验证码识别错误")
            return 1
    else:
        print("网络请求错误")
        return "网络请求错误"


def Recognise(img_path):
    ak = 'ak'
    sk = 'sk'
    access_token, expires_in = GetAccessToken(ak, sk)  # 将此ak与sk替换成自己应用的值
    with open(file=img_path, mode='rb') as file:
        base64_data = base64.b64encode(file.read())
    # 调用iOCR自定义模板文字识别接口 recognise = RecogniseForm(access_token=access_token, image=base64_data,
    # templateSign=templateSign)    # 将此templateSign替换成自己设置的模板值
    recognise = RecogniseGeneral(access_token=access_token, image=base64_data)
    # print(recognise)
    # for k, v in recognise.items():
    #     print(k, v)
    return recognise

'''
这是我在网上找到的调用百度api的例子，并使用了。作者是Loong Xu。CSDN但是原文懒得找，想要学习的童鞋，应该可以在CSDN上面根据名字找到他的。
'''
# print(Recognise("transfered_image.jpg"))