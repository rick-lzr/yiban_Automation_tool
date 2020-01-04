import os
from PIL import Image


def read_captcha(path):
    image_array = []
    image_label = []
    file_list = os.listdir(path)  # 获取captcha文件
    for file in file_list:
        image = Image.open(path + '/' + file)  # 打开图片
        file_name = file.split(".")[0]  # 获取文件名，此为图片标签
        image_array.append(image)
        image_label.append(file_name)

    return image_array, image_label


def image_transfer(image):
    """
    :param: image_arry:图像list，每个元素为一副图像
    :return: image_clean:清理过后的图像list
    """
    image_clean = []
    threshold_grey = 110

    image = image.convert('L')  # 转换为灰度图像，即RGB通道从3变为1
    im2 = Image.new("L", image.size, 255)
    for y in range(image.size[1]):  # 遍历所有像素，将灰度超过阈值的像素转变为255（白）
        for x in range(image.size[0]):
            pix = image.getpixel((x, y))
            if int(pix) > threshold_grey:  # 灰度阈值
                im2.putpixel((x, y), 255)
            else:
                im2.putpixel((x, y), pix)
    image_clean.append(im2)
    return image_clean


def image_split(image):
    """
    :param image:单幅图像
    :return:单幅图像被切割后的图像list
    """
    image_character_num = 1
    image_height = 50
    image_width = 50
    inletter = False  # 找出每个字母开始位置
    foundletter = False  # 找出每个字母结束位置
    start = 0
    end = 0
    letters = []  # 存储坐标
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            pix = image.getpixel((x, y))
            if pix != 255:
                inletter = True
        if foundletter == False and inletter == True:
            foundletter = True
            start = x
        if foundletter == True and inletter == False:
            foundletter = False
            end = x
            letters.append((start, end))
        inletter = False
    print(letters)
    # 因为切割出来的图像有可能是噪声点
    # 筛选可能切割出来的噪声点,只保留开始结束位置差值最大的位置信息
    subtract_array = []  # 存储 结束-开始 值
    for each in letters:
        subtract_array.append(each[1] - each[0])
    reSet = sorted(subtract_array, key=lambda x: x, reverse=True)[0:image_character_num]
    letter_chioce = []  # 存储 最终选择的点坐标
    for each in letters:
        if int(each[1] - each[0]) in reSet:
            letter_chioce.append(each)

    image_split_array = []  # 存储切割后的图像
    print(image.size[1])
    print(letter_chioce)
    for letter in letter_chioce:
        im_split = image.crop((letter[0], 0, letter[1], image.size[1]))  # (切割的起始横坐标，起始纵坐标，切割的宽度，切割的高度)
        im_split = im_split.resize((image_width, image_height))  # 转换格式
        image_split_array.append(im_split)

    return image_split_array[0:int(image_character_num)]


def read_image(file_path):
    image = Image.open(file_path)
    return image


def automation(file_path):
    image = read_image(file_path)
    image_transfer(image)[0].save("transfered_image.jpg")

automation("yanzhengma.jpg")
# print(read_captcha("yanzhengma"))
# image_arry = read_captcha("jpg")
#
# image_arry = image_arry[0:1]
#
# image_clean = image_transfer(image_arry=image_arry)
# image_clean[0].save("jpg/new_image2.jpg", quality=95)
# image_splited = image_split(image_clean[0])
# image_splited[0].save("jpg/new_image.jpg", quality=95)
# image_splited[0].show()
# img = np.array(image_clean[0])
# print(img)
# np.savetxt("img_np_array.txt", img)
