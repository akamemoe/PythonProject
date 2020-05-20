# -*- coding:utf-8 -*-
import urllib.request
import random

try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract


# 二值化函数
def initTable(threshold=140):
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return table


# 用别人的网站随机得到一个验证码图片,保存为test.png
ord = random.random()
ord = ord * 10000000000000000000
url = "http://www.afreesms.com/image.php?o=" + str(ord)
urllib.request.urlretrieve(url, './test/test.png')

image = Image.open('./test/test.png')
# 得到的图片为(76,28),下半部分是广告，裁减掉
# (left, upper, right, lower)
cp_img = image.crop((0, 0, 76, 16))
# cp_img.show()


# 彩色图片转为灰度图片，提高识别率
imgry = cp_img.convert('L')

# 二值化，去除背景噪声
out = imgry.point(initTable(), '1')

# -psm 7 =Treat the image as a single text line
# -oem 0 =Original Tesseract only,默认为3，要使用tessedit_char_whitelist只识别数字必须设为0
# -c tessedit_char_whitelist 设置过滤白名单，提高准确率
# lang='eng' eng表示识别的语言为英语 chi-sim表示简体中文
result = pytesseract.image_to_string(out, lang='eng', config='-psm 7 -oem 0 -c tessedit_char_whitelist=1234567890')

# 输出处理后的图片，以识别得到的数字命名图片
out.save('./test/{}.png'.format(result), 'png')
