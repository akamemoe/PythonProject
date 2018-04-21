#encoding=utf-8

import requests
import re,os,time


anchors = []
huya_url = 'http://www.huya.com/'


def send_msg(text='title',desp='desp'):
    notify_url = 'https://sc.ftqq.com/' + os.getenv('scu_key') +'.send'
    r = requests.get(notify_url,params={'text':text,'desp':desp})
    return True if r and r.status_code == 200 else False

def fetch(file_path):
    with open(file_path,'r',encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            print(line)
            a,b = line.split(':')
            anchors.append((a,b))
    txt = '| 主播 | 标题 | 状态 | 订阅 |\n|:---:|:---:|:---:|:---:|\n'
    for suffix,anchor in anchors:
        # time.sleep(1000)
        print('watching:',anchor)
        try:
            r = requests.get(huya_url + suffix,timeout=3)
            html = r.content.decode('utf-8')
            title = re.findall(r'<h1 id="J_roomTitle">(.+)</h1>',html)[0]
            status = re.findall(r'<span class="host-prevStartTime"><i></i><span>(.+)</span></span>',html)
            fans = re.findall(r'<div id="activityCount">(\d+)</div>',html)[0]
            last_live = '直播中'
            if status and status[0]:
                last_live = status[0]
        except:
            print('ERROR:' + huya_url + suffix)
        else:
            txt += ('|' + anchor + '|' + title + '|' + last_live + '|' + fans + '|\n')
    if send_msg('主播直播状态',txt):
        print('wechat message push success.')
    else:
        print('wechat message push failed.')

if __name__ == '__main__':
    fetch()