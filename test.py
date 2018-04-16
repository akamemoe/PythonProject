# coding:utf-8

import requests
import re,os
import time
from src.huya import huya_anchor as huya


def get_env_var():
	print('NAME->',os.getenv('name'))


def main():
	huya.fetch()

if __name__ == '__main__':
	main()
