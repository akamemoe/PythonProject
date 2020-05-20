#coding=utf-8
import requests
import re,os,sys,time
import json
from pyquery import PyQuery
import click
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Weibo():
    
    BASE_URL = 'https://m.weibo.cn/api/container/getIndex'
    def __init__(self,name,uid,debug=False):
        self.name = name
        self.uid = uid
        self.headers={
        "User-Agent":"BaiduSpider",
        "Cookie":"MLOGIN=0; _T_WM=11286988042; WEIBOCN_FROM=1110006030",
        "x-requested-with":"XMLHttpRequest",
        "mweibo-pwa":'1',
        "referer":"https://m.weibo.cn",
        "accept":"application/json, text/plain, */*"}
        self.sess = requests.session()
        self.debug = debug

    #
    def _build_params(self,page):
        params = {
            'uid' : self.uid,
            'luicode' : '10000011',
            'type' : 'uid',
            'value' : self.uid,
            'containerid' : '107603'+self.uid,
            'page' : str(page),
            'standalone' : '0'
        }
        return params
        
    #可能是107603+uid
    def _query_containerid(self):
        try:
            r = requests.get(Weibo.BASE_URL,params={'uid':self.uid,'type':'uid','value':self.uid},headers=self.headers)
            for t in r.json()['data']['tabsInfo']['tabs']:
                if t['tabKey'] == 'weibo':
                    return t['containerid']
        except Exception as e:
            with open('error.json','wb') as f:
                f.write(r.content)
            print("找不到containerid,请检查weibo是否更改了json结构",e)
            sys.exit()
        return '00000000000000000'

    def fetch(self,page=1):
        
        r = self.sess.get(Weibo.BASE_URL,params=self._build_params(page),headers=self.headers)
        r.encoding = 'utf-8'
        rs = r.json()
        if self.debug:
            with open('{}_page_{}.log'.format(self.name,page),'w',encoding='utf-8') as f:
                f.write(json.dumps(rs,ensure_ascii=False))
        
        if rs['ok'] != 1:
            logger.warning('fetch error. rs["ok"] != 1 msg={}'.format(rs['msg']))
            return
        infos = {}
        infos['total'] = rs['data']['cardlistInfo']['total']
        infos['page_count'] = rs['data']['cardlistInfo']['v_p']
        weibos = []
        for item in rs['data']['cards']:
            if item['card_type'] != 9:
                logger.warning('unexcepted card type:{} at page:{}'.format(item['card_type'],page))
                continue
            blog = {}
            blog['itemid'] = item.get('itemid','0')
            blog['date'] = item['mblog']['created_at']
            blog['raw'] = item['mblog']['text']
            blog['text'] = PyQuery(item['mblog']['text']).text()
            blog['comments_count'] = item['mblog']['comments_count']
            
            pics = item['mblog'].get('pics',None)
            if pics:
                blog['images'] = []
                for x in pics:
                     blog.get('images',[]).append(x['large']['url'])
            logger.info('#{}[{}]{} (P{})'.format(page,blog['date'],blog['text'],len(blog.get('images',[]))))
            
            page_info = item['mblog'].get('page_info',None)
            if page_info:
                ptype = page_info['type']
                if ptype == 'video':
                    blog['video'] = {}
                    blog['video']['cover'] = page_info['page_pic']['url']
                    blog['video']['view_url'] = page_info['media_info']['h5_url']
                    blog['video']['mp4_src'] = page_info['media_info']['mp4_hd_url']
                    blog['video']['duration'] = page_info['media_info']['duration']

            weibos.append(blog)

        infos['weibos'] = weibos
        if self.debug:
            with open('{}_infos_{}.log'.format(self.name,page),'w',encoding='utf-8') as f:
                f.write(json.dumps(infos,ensure_ascii=False))
        return infos


@click.command()
@click.option('-u','--uid',required=True,type=str,prompt='uid',help='用户uid')
@click.option('-n','--name',required=True,type=str,prompt='name',help='昵称')
@click.option('-p','--page',type=int,default=1,show_default=True,help='抓取第几页微博数据')
@click.option('--all','isall',is_flag=True,help='是否抓取全部微博')
@click.option('--download',is_flag=True,help='是否下载图片和视频')
@click.option('-t','--threads',type=int,default=4,show_default=True,help='下载图片和视频的线程数量')
@click.option('-f','--folder',type=str,default='./data',help='下载图片和视频的目录')
@click.option('--delay',type=int,default=1,show_default=True,help='睡眠时间，防止爬取太快被ban')
@click.option('--debug',is_flag=True,help='是否开启debug模式打印log')
def main(uid,name,page,isall,download,threads,folder,delay,debug):
    # print(uid,name,page,all,download,threads,folder,debug)
    w = Weibo(name,uid)
    data = {'total':0,'weibos':[]}
    if isall:
        for x in range(10000):
            time.sleep(delay)
            r = w.fetch(x)
            if not r:
                break
            data['weibos'].extend(r['weibos'])
        data['total'] = len(data['weibos'])
    else:
        data = w.fetch(page)
    with open('{}_result.json'.format(name),'w',encoding='utf-8') as f:
        f.write(json.dumps(data,ensure_ascii=False))

if __name__ == '__main__':
    main()
    # wb = Weibo('萧璇','3959587945')
    # for x in range(1,11):
        # wb.fetch(page=x)
        # time.sleep(1)