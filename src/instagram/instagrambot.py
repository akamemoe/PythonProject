#coding=utf-8

import re,os,sys,time,json
import requests
import logging


#log config

logging.basicConfig(filename=os.path.join(os.path.dirname(os.path.abspath(__file__)),'instagrambot.log'),
                    filemode='a',
                    format='%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

class Instagram():
    host = 'https://www.instagram.com'

    headers = {
        "Origin": "https://www.instagram.com/",
        "Referer": "https://www.instagram.com/",
        "User-Agent": "GoogleBot/3.0",
        "Host": "www.instagram.com"
    }
    proxies = {'http':'http://127.0.0.1:1080','https':'https://127.0.0.1:1080'} if 'win' in sys.platform else None

    def __init__(self,user,nickname):
        self.profile_url = Instagram.host + '/' + user
        self.nickname = nickname
        self.session = requests.Session()

    def request(self,url):
        time.sleep(2)
        logger.info('request:'+url)
        try:
            r = self.session.get(url,headers=Instagram.headers,proxies=Instagram.proxies)
            return r.text
        except Exception as e:
            logger.error('failed request:'+url)
            return ''


    def fetch_profile_data(self,profile_url):
        html = self.request(profile_url)
        for line in html.split('\n'):
            line = line.strip()
            if line.startswith('<script type="text/javascript">window._sharedData = '):
                json_data = line.replace('<script type="text/javascript">window._sharedData = ','').replace(';</script>','')
                # print('fetch_profile_data:',json_data)
                return json.loads(json_data)
        return None

    def fetch_detail_data(self,detail_url):
        html = self.request(detail_url)
        for line in html.split('\n'):
            line = line.strip()
            if line.startswith('<script type="text/javascript">window._sharedData = '):
                json_data = line.replace('<script type="text/javascript">window._sharedData = ','').replace(';</script>','')
                # print('fetch_detail_data:',json_data)
                return json.loads(json_data)
        return None

    def parse_post_pages(self,profile_data):
        post_pages = []
        edges = profile_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]
        logger.info('edges length:%d' % len(edges))
        for edge in edges:
            node = edge['node']
            post_pages.append({
                'type':node['__typename'],
                'detail_url':'https://www.instagram.com/p/'+node['shortcode'],
                'text': '' if not node['edge_media_to_caption']['edges'] else node['edge_media_to_caption']['edges'][0]['node']['text'],
                'timestamp':node['taken_at_timestamp'],})
        logger.info('post_pages length:%d' % len(post_pages))
        return post_pages

    def parse_image_urls(self,detail_data):
        posts = []
        medias = detail_data['entry_data']['PostPage'][0]['graphql']['shortcode_media']
        if medias['__typename'] == 'GraphImage':#这种情况表示只有一张图片
            posts.append(medias['display_resources'][-1]['src'])
        elif medias['__typename'] == 'GraphSidecar':#这种情况表示是多个图片
            edges = medias['edge_sidecar_to_children']['edges']
            for edge in edges:
                #display_resources中包含多个图片大小，只取分辨率最高的，也即最后一张
                image_url = edge['node']['display_resources'][-1]['src']
                posts.append(image_url)
        elif medias['__typename'] == 'GraphVideo':#这种情况表示是视频
            posts.append(medias['video_url'])
        logger.info('posts length:%d' % len(posts))
        return posts

    def fetch_all(self,after='2017-01-01'):
        '''
        after : "XXXX-XX-XX" 只抓取这个时间之后的图片
        '''
        after = int(time.mktime(time.strptime(after, '%Y-%m-%d')))
        profile_data = self.fetch_profile_data(self.profile_url)
        post_pages = self.parse_post_pages(profile_data)
        result = []
        for item in post_pages:
            if item['timestamp'] > after:
                detail_data = self.fetch_detail_data(item['detail_url'])
                posts = self.parse_image_urls(detail_data)
                result.append({'time':time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item['timestamp'])),
                    'url':item['detail_url'],
                    'text':item['text'],
                    'posts':posts})
        logger.info('result lenght:%d->%s',json.dumps(result,ensure_ascii=False))
        return result

    def build_markdown(self,result):
        if not result:
            logger.info('检测到(%s)instagram更新了' % self.nickname)
            return '### {} instagram没有更新\n'.format(self.nickname)
        template = '### {} instagram有更新\n----\n\n'.format(self.nickname)
        for item in result:
            template += '###### {}\n\n'.format(item['time'])
            template += '> {}\n\n'.format(item['text'].replace('\n',''))
            for u in item['posts']:
                if u.endswith('.jpg'):
                    template += '![]({})\n'.format(u)
                elif u.endswith('.mp4'):
                    template += '<video><source src="{}"  type="video/mp4"></video>\n'.format(u)


            template += '-----\n\n'
        return template

def send_msg(text='title',desp='desp'):
    notify_url = 'https://sc.ftqq.com/${scu_key}.send'
    r = requests.post(notify_url,data={'text':text,'desp':desp},timeout=5)
    return r and r.ok and r.json()['errmsg'] == 'success'

def main():
    ins = Instagram('sandra0314','马思纯')
    #crontab: 0 59 23 * * ? python instagrambot.py
    today = time.strftime('%Y-%m-%d', time.localtime())
    r = ins.fetch_all(after=today)
    # with open('result.json','w',encoding='utf-8') as f:
    #     f.write(json.dumps(r,ensure_ascii=False))
    if r:
        mktxt = ins.build_markdown(r)
        send_msg(text='马思纯instagram更新了',desp=mktxt)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.error(e)

    