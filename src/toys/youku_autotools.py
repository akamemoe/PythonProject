#coding=utf-8

import pyautogui
import re,time

pyautogui.PAUSE = 1

class AutoTools():
    '''
    自动控制键盘鼠标登陆优酷，用于验证网上抓取的VIP账号的可用性。
    '''

    #用户名输入框位置
    userArea = (905,328)
    #密码区输入框位置
    pwdArea = (840,390)
    #登陆按钮位置
    loginBtn = (820,480)

    @staticmethod
    def _autofill(username,password):
        '自动填充用户名密码'

        pyautogui.click(AutoTools.userArea)
        pyautogui.hotkey('ctrl','a')
        pyautogui.press('backspace')
        pyautogui.typewrite(username,interval=0.2)

        pyautogui.click(AutoTools.pwdArea)
        pyautogui.hotkey('ctrl','a')
        pyautogui.press('backspace')
        pyautogui.typewrite(password,interval=0.2)

        pyautogui.click(AutoTools.loginBtn)


    @staticmethod
    def autologin(account_file):
        '根据账号密码文件自动登陆并验证是否登陆成功'

        accounts = []
        with open(account_file,'r',encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                rs = re.search(r'账号:(.+) 密码:(.+)',line)
                accounts.append((rs.group(1),rs.group(2)))

        time.sleep(5)
        try:
            for u,p in accounts:
                AutoTools._autofill(u,p)
                if AutoTools._check_success():
                    print('SUCCESS:',u,p)
                time.sleep(5)
        except:
            print('force stop')


    @staticmethod
    def _check_success():
        '效验页面上的登陆提示：目前未完成'
        # pyautogui.localOnScreem()
        return True


if __name__ == '__main__':
    AutoTools.autologin('VIPDQ_2018年04月10日优酷账号.txt')
