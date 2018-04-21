#coding=utf-8

import requests

class QTProxy():

    @staticmethod
    def get_free_proxy():
        params = {
            'app_id':'XXXXXXXXXXXXXXX',
            'format':'json',
            # 'loc_name':''
        }
        r = requests.get('http://proxy.horocn.com/api/free-proxy',params=params)
        rs = []
        for x in r.json():
            p = {'http':'http://{}:{}'.format(x['host'],x['port']),'https':'https://{}:{}'.format(x['host'],x['port'])}
            if QTProxy.test(p):
                #选择有效代理
                rs.append(p)
        return rs


    @staticmethod
    def get_proxy(n):
        params = {
            'order_id':'xxxxxxxxxxxxxxxxx',
            'format':'json',
            'line_separator':'win',
            'num':n
        }
        r = requests.get('https://proxy.horocn.com/api/proxies',params=params,timeout=5)
        rs = []
        for x in r.json():
            rs.append({'http':'http://{}:{}'.format(x['host'],x['port']),'https':'https://{}:{}'.format(x['host'],x['port'])})
        return rs

    @staticmethod
    def test(proxy,timeout=5):
        try:
            print('proxy testing:',proxy,end='->')
            r1 = requests.get('http://www.baidu.com',proxies=proxy,timeout=timeout)
            r2 = requests.get('https://www.baidu.com',proxies=proxy,timeout=timeout)
        except:
            print('NO',flush=True)
            return False
        else:
            print('OK',flush=True)
            return r1 and r2


if __name__ == '__main__':
    r = QTProxy.get_free_proxy()
    print(r)