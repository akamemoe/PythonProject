#coding=utf-8

from datetime import datetime
import requests
import re,os,time


def print_time():
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

class Youku(object):

    def __init__(self):
        self.page_urls = []
        self.vips = []
        self.dest_dir = '.'

    def _get_header(self):
        return {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
                'Referer':self.base_url}
    
    def _request(self,url):
        time.sleep(1)
        print('request:',url)
        r = requests.get(url,headers=self._get_header())
        if r:
            return r.text
        else:
            print('request failed:'+url)
            return ''

    def _current_date(self):
        return time.strftime('%Y{y}%m{m}%d{d}').format(y='年', m='月', d='日')

    def _write2file(self,filename):
        #先按照账号长短排序，长度相同则按照字典序排序
        vip_list = sorted(self.vips,key=lambda u:(len(u[0]),u[0]))
        with open(os.path.join(self.dest_dir,filename),'w',encoding='utf-8') as f:
            for x in vip_list:
                f.write('账号:'+x[0]+' 密码:'+x[1]+'\n')
        self.vips = []



class Youku_FXDS(Youku):
    '''
    http://www.fenxiangdashi.com/youku
    '''

    def __init__(self):
        super().__init()
        self.base_url = 'http://www.fenxiangdashi.com/youku'
        
    def _get_pages(self):
        '''
        获取包含账号密码的页面
        '''
        for x in range(1,20):
            html = self._request(self.base_url + '/page-'+str(x)+'.html')
            urls = set(re.findall(r'href="/youku/(.+)" tar.+"优酷土豆会员账号'+self._current_date()+'更新',html))
            if urls and len(urls)>0:
                self.page_urls.extend(urls)
            else:
                #如果列表为空说明已经获取了所有当日的页面
                return

    def get_account(self):
        '''
        遍历包含账号密码的页面获取所有的vip账号
        '''
        self._get_pages()
        for url in self.page_urls:
            html = self._request(self.base_url + '/' + url)
            txt = re.findall(r'<br/>优酷土豆会员账号\d+年\d+月\d+日更新(.+)',html)[0]
            lst = txt.split('<br/>')
            for item in lst:
                rs = re.search(r'账号：(.+) 密码：(.+)',item)
                if rs:
                    self.vips.append((rs.group(1),rs.group(2)))

        self._write2file('FXDS_'+self._current_date()+'优酷账号.txt')


class Youku_VipDQ(Youku):
    '''
    http://www.vipdaquan.com/youku
    '''
    def __init__(self):
        super().__init__()
        self.base_url = 'http://www.vipdaquan.com/youku'

    def _get_pages(self):
        for x in range(1,2):
            html = self._request(self.base_url+'/page/'+str(x))
            urls = re.findall(r'http://www\.vipdaquan\.com/youku/(\d+\.html)',html)
            urls = set(urls)
            # print(urls)
            if urls and len(urls)>0:
                self.page_urls.extend(urls)
            else:
                return

    def get_account(self):
        self._get_pages()
        for url in self.page_urls:
            html = self._request(self.base_url+'/'+url)
            ac_list = re.findall(r'<li>优酷会员账号：(.+)，优酷会员密码：(.+)</li>',html)
            if ac_list and len(ac_list)>0:
                self.vips.extend(ac_list)
            # title = re.findall(r'<title>(.+)</title>',html)
            # print(ac_list)
            # print(title,url)
            # time.sleep(5)

        self._write2file('VIPDQ_'+self._current_date()+'优酷账号.txt')

def main():
    vip_youku = Youku_VipDQ()
    vip_youku.get_account()


if __name__ == '__main__':
     main()