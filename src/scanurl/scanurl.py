#coding=utf-8
import requests
import re,sys,os,time


class Scanner():

    def __init__(self):
        self.session = requests.Session()
        self.timeout = 3
        self.headers = {'Connection':'keep-alive'}
        self.success = []

    def scan(self,url):
        try:
            t = 'try:%s' % (url,)
            print(t,end='')
            r = self.session.get(url,timeout=self.timeout,headers=self.headers)
            time.sleep(0.5)
            if r.status_code != 404:
                print('found url:',url)
                self.success.append(url)
        except Exception as e:
            print('error:',e)
        with open('success.txt','w') as f:
            f.write('\n'.join(self.success))




def main():
    s = Scanner()
    if len(sys.argv) == 2:
        h = sys.argv[1]
    else:
        print('require:host')
        return
    host = h+'{}'

    with open('php_urls.txt','r') as f:
        data = f.readlines()
    urls = [x.strip() for x in data]
    for x in urls:
        s.scan(host.format(x))
    

if __name__ == '__main__':
    main()