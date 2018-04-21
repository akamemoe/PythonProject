#coding=utf-8

import requests
import sys,os,time,re,random
from bs4 import BeautifulSoup


headers = {
    'authority': 'www.dy2018.coms',
    'path': '/e/search/index.php',
    'scheme': 'https',
    'content-type': 'application/x-www-form-urlencoded',
    'user-agent':'baiduspider',
    # 'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
    'referer': 'https://www.dy2018.com/html/gndy/dyzz/',
}

class DYTT():
    '''
    电影天堂电影搜索
    '''
    
    def __init__(self):
        self.base_url = 'https://www.dy2018.com'
        self.search_url = 'https://www.dy2018.com/e/search/index.php'
        self.session = requests.Session()
        self.session.headers.update(headers)
        self.session.get(self.base_url,timeout=10)#get cookie
        self._encoding = 'GB2312' #页面默认编码是gb2312
        self.proxypool = []
        self.use_proxy = False

    def init_proxy_pool(self,size):
        '初始化代理池'
        try:
            #私人的蜻蜓代理类,如要使用需要有账号信息
            from qtproxy import QTProxy
        except:
            pass
        else:
            self.proxypool = QTProxy.get_proxy(size)

    def _get(self,*args,**kw):
        p = None
        if self.use_proxy:
            p = random.choice(proxypool)
            print('proxy:',p)
        return self.session.get(*args,headers=headers,timeout=10,proxies=p,**kw).content.decode(self._encoding,'ignore')

    def _post(self,*args,**kw):
        p = None
        if self.use_proxy:
            p = random.choice(proxypool)
            print('proxy:',p)
        return self.session.post(*args,headers=headers,timeout=10,proxies=p,**kw).content.decode(self._encoding,'ignore')

    def search(self,title):
        '根绝标题搜索电影'
        data = [
            ('show', 'title,smalltext'),
            ('tempid', '1'),
            ('keyboard', title.encode(self._encoding))
        ]
        txt = self._post(self.search_url,data=data)
        # txt = ''
        # with open('b.html','r',encoding='gb2312') as f:
        #     txt = f.read()
        # print(len(txt))
        return self._get_result(txt)



    def _get_result(self,txt):
        '提取所有搜索结果'
        soup = BeautifulSoup(txt,'lxml')#html.parser
        # print(soup.original_encoding)
        rs = []
        for x in soup.find_all('table'):
            tds = x.find_all('td')
            try:
                title = tds[2].get_text().strip()
                page_url = tds[2].find('a')['href'].strip()
                date = tds[4].get_text().strip().split('\n')[0]
                summary = tds[5].get_text().strip()
                # print('title&link:',tds[2].get_text().strip(),tds[2].find('a')['href'].strip())
                # print('date&click',tds[4].get_text())
                # print('content:',tds[5].get_text())
            except Exception as e:
                pass
                # print('error:',e)
            else:
                rs.append((title,page_url,date,summary))
        return rs
               

    def parse_download_urls(self,page_url):
        '在详情页面提取所有下载链接(ftp/magnet/http)'
        txt = self._get(self.base_url+page_url)
        # txt = ''
        # with open('d.html','rb') as f:
        #     txt = f.read().decode('gb2312')
        soup = BeautifulSoup(txt,'lxml')
        tables = soup.find_all('table')
        links = []
        for i,tab in enumerate(tables):
            for link in tab.find_all('a'):
                if re.match(r'^[ftp|magnet|http].+',link['href']):
                    # print('link:',link['href'])
                    links.append(link['href'])
            # print('='*20)
        return links


def main():
    dytt = DYTT()
    name = input('movie:')
    rs = dytt.search(name)
    print('result count:',len(rs))
    for i,x in enumerate(rs):
        print('INDEX:',i,x)
        print('='*20)

    n = input('choice:')
    download_urls = dytt.parse_download_urls(rs[int(n)][1])
    print(download_urls)
    # dytt.parse_download_urls('af')

if __name__ == '__main__':
    main()
    # rs = QTProxy.get_proxy(5)
    # for p in rs:
    #     print(QTProxy.test(p),p)
    # print(q)









