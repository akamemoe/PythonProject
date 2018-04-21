# 一些Python小玩具 #

### 1.扫雷([minesweeper.py](https://github.com/Akame-moe/PythonProject/blob/master/src/toys/minesweeper.py)) ###

- #### 使用：
	在`minesweeper.py`所在的目录下面打开命令行输入：`python minesweeper.py`,游戏开始运行。默认初始化的地图大小为9\*9，雷出现的概率为0.3。  
	游戏运行后你也可以:  
	输入命令`init $size $rate`来重新初始化地图，将地图修改为size\*size大小，雷概率为$rate。例如:`init 12 0.2`;  
	输入命令`click $x $y`来点击对应的点(*0<=x,y<size*)，例如:`click 3 5`;  
	输入命令`flag $x $y`来标记点(x,y)，例如:`flag 4 6`;  
	输入命令`exit`来退出游戏;  

### 2.自动抓取优酷VIP账号([youku.py](https://github.com/Akame-moe/PythonProject/blob/master/src/toys/youku.py)) ###

- #### 说明：  
	本程序可以抓取`http://www.fenxiangdashi.com/youku`和`http://www.vipdaquan.com/youku`页面上的优酷VIP账号和密码。

- #### 使用：  
	```python
	import youku
	
	def main():
		#http://www.fenxiangdashi.com/youku
		yk = youku.Youku_FXDS()
		yk.get_account()
		#http://www.vipdaquan.com/youku
		yk = youku.Youku_VipDQ()
		yk.get_account()
	if __name__ == '__main__':
		main()	
	```
	默认保存在当前目录，你也可以通过`yk.dest_dir`属性来修改。

### 3.自动登陆优酷([youku_autotools.py](https://github.com/Akame-moe/PythonProject/blob/master/src/toys/youku_autotools.py)) ###

- #### 说明：
	本程序借助`pyautogui`模块自动控制键盘鼠标输入优酷账号密码并且点击登录按钮。不同的电脑输入框和按钮位置都不一样，需要自己修改代码中的用户名、密码、登录按钮的位置。  

- #### 使用：
	```python
	from youku_autotools import AutoTools
	
	def main():
		AutoTools.autologin('VIPDQ_2018年04月10日优酷账号.txt')
	
	if __name__ == '__main__':
		main()
	```

### 4.多线程下载器([multithreading_downloader.py](https://github.com/Akame-moe/PythonProject/blob/master/src/toys/multithreading_downloader.py)) ###

- #### 说明：
	本程序通过控制http协议请求头中的`Range`参数实现多线程分块下载，并且支持断线续传。  

- #### 使用：
	```python
	from multithreading_downloader import Downloader
	
	def main():
		file_url = 'http://www.domain.com/download.zip'
		#第一个参数文件地址，第二参数保存的文件名，第三个参数为下载的线程数
		mydownloader = Downloader(file_url,'some.zip',3)
		mydownloader.download()
	```

### 5.遗传算法([genetic_algorithm.py](https://github.com/Akame-moe/PythonProject/blob/master/src/toys/genetic_algorithm.py)) ###

- #### 说明：
	本程序为遗传算法的示例程序，程序中已经有详细注释。  

### 6.发送邮件([mailutils.py](https://github.com/Akame-moe/PythonProject/blob/master/src/toys/mailutils.py)) ###  

- #### 说明：
	本程序封装了邮件发送方法，只需要调用一个方法就可以发送邮件。

- #### 使用：
	```python
	from mailutils import MailUtils
	import sys,configparser
	#email.ini文件内容
	'''
	[EMAIL]
	#发送邮件使用
	smtphost = smtp.sina.cn
	smtpport = 25
	#接收邮件使用
	pophost  = pop.sina.cn
	popport  = 110
	user     = sender@sina.cn
	password = abc123
	'''
	def main():
		util = MailUtils()
		
		cfg = configparser.ConfigParser()
		cfg.read('email.ini',encoding='utf-8')
		info = cfg['EMAIL']
		sender_info = {
			'user':info['user'],
			'password':info['password'],
			'host':info['smtphost'],
			'port':int(info['smtpport']),
			'nick':'Server酱'
		}
		util.set_user(**sender_info)
		# util.print_config()
		util.send_to_multi(['aa@domain.com','bb@domain.com'],'尊敬的用户你好','你确定收到了吗')
	if __name__ == '__main__':
		main()
	```

### 7.抓取[电影天堂](https:/www.dy2018.com)下载链接([dytt.py](https://github.com/Akame-moe/PythonProject/blob/master/src/toys/dytt.py)) ###

- #### 说明：  
	可以在命令行搜索电影天堂的电影，免的去看网站那些广告了。

- #### 使用：
	直接运行`python dytt.py`根据提示操作即可。
	

### 8.蜻蜓代理([qtproxy.py](https://github.com/Akame-moe/PythonProject/blob/master/src/toys/qtproxy.py)) ###

- #### 说明：  
	蜻蜓代理API的封装。