# -*- coding: UTF-8 -*-

import smtplib,sys,configparser
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from email import utils


class MailUtils():

	def set_user(self,user,password,host,port,nick):
		self._user = user
		self._password = password
		self._host = host
		self._port = port
		self._nick = nick

	def print_config(self):
		print(self._user,self._password)

	def _send_mail(self,receiver,subject,content,fmt='plain'):
		'''
		fmt(format):plain/html
		return:true/false
		'''

		# 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
		message = MIMEText(content, fmt, 'utf-8')
		message['From'] = formataddr([self._nick,self._user])
		message['To'] =  formataddr(['To',receiver])
		message['Subject'] = Header(subject, 'utf-8')

		try:
			server = smtplib.SMTP()
			# server.set_debuglevel(1)
			server.connect(self._host,self._port)
			server.login(self._user,self._password)
			server.sendmail(self._user, [receiver], message.as_string())
			print("email send successful.")
		except smtplib.SMTPException as e:
			print("email send failed. >> ",e)
			return False
		finally:
			server.quit()
		return True

	def send_html_mail(self,receiver,subject,content):
		self._send_mail(receiver,subject,content,fmt='html')

	def send_text_mail(self,receiver,subject,content):
		self._send_mail(receiver,subject,content,fmt='plain')

	def send_to_multi(self,receivers,subject,content,fmt='plain'):
		message = MIMEText(content, fmt, 'utf-8')
		message['From'] = formataddr([self._nick,self._user])
		message['To'] =  formataddr(['你的昵称',u','.join(receivers)])
		message['Subject'] = Header(subject, 'utf-8')

		try:
			server = smtplib.SMTP()
			# server.set_debuglevel(1)
			server.connect(self._host,self._port)
			server.login(self._user,self._password)
			server.sendmail(self._user, receivers, message.as_string())
			print("email send successful.")
		except smtplib.SMTPException as e:
			print("email send failed. >> ",e)
			return False
		finally:
			server.quit()
		return True
