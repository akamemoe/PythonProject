# coding:utf-8

import requests
import re

def main():
	r = requests.get('https://www.baidu.com')
	print(r.status_code)
	# print(r.content.decode('utf-8'))
	title = re.findall(r'<title>(.*)</title>',r.content.decode('utf-8'))
	print('title:',title)

if __name__ == '__main__':
	main()