# Simple-Captcha-Recognition
Simple CAPTCHA Recognition based on Tesseract OCR<br>
python简单的图片验证码自动识别，基于tesseract

## 效果展示
彩色为验证码原图，黑白的为处理后的图片，名字为识别出的验证码，可以看到正确率100%
![](https://github.com/tiantianwahaha/Simple-Captcha-Recognition/blob/master/example.png)

## 环境
python3.5<br>
ubuntu 16.04

基于tesseract-ocr<br>
tesseract 是一个google支持的开源ocr项目，[项目地址](https://github.com/tesseract-ocr/tesseract)，识别图片文字，需要依赖PIL，pytesseract

### 1.tesseract-ocr安装
```
sudo apt-get install tesseract-ocr
```
默认为英语识别，如果需要中文识别，需要单独install
```
sudo apt install tesseract-ocr-chi-sim
```

### 2.pytesseract安装
```
sudo pip install pytesseract
```
### 3.Pillow 安装
```
sudo pip install pillow
```
## 示例
演示了识别只有数字的验证码
```
python main.py
```


## 重要参数解释
```
pytesseract.image_to_string(iamge, lang='eng', config='-psm 7 -oem 0 -c tessedit_char_whitelist=1234567890')

参数解释
-psm 7 =Treat the image as a single text line
-oem 0 =Original Tesseract only,默认为3，要使用tessedit_char_whitelist只识别数字，此项必须设为0
-c tessedit_char_whitelist 设置过滤白名单，提高准确率，如果需要字母，同理添加进去
lang='eng' eng表示识别的语言为英语 chi-sim表示简体中文
```

如果不需要限定识别范围，可以改为
```
pytesseract.image_to_string(image, config='-psm 7')
```
