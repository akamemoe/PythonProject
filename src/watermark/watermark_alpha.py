from PIL import Image,ImageDraw,ImageFont,ImageEnhance

def main():
	im = Image.open('test.jpg')
	w, h = im.size
	watermark = Image.new('RGBA', im.size) # 水印
	draw = ImageDraw.Draw(watermark, 'RGBA')

	# 设置文字大小
	font_size = 100

	# 设置字体
	font_file = "arial.ttf"
	font = ImageFont.truetype(font_file,font_size)
	draw.text((200, 400), 'current date', fill="#ff0000", font=font)

	# 旋转 45 度
	watermark = watermark.rotate(-45, Image.BICUBIC)

	# 透明的
	alpha = watermark.split()[3]
	alpha = ImageEnhance.Brightness(alpha).enhance(0.7)
	watermark.putalpha(alpha)

	# 合成新的图片
	n = Image.composite(watermark, im, watermark)
	n.save('new_watermark.jpg', 'jpeg')
	
main()