# coding:utf-8

import requests
import re,os
import time

gui.PAUSE = 1

def get_env_var():
	print('NAME->',os.environ('name'))


def main():
	r = requests.get('https://www.baidu.com')
	print(r.status_code)
	# print(r.content.decode('utf-8'))
	title = re.findall(r'<title>(.*)</title>',r.content.decode('utf-8'))
	print('title:',title)
	get_env_var()

if __name__ == '__main__':
	main()
