#encoding=utf-8

import requests
import re,os,time


anchors = []
huya_url = 'http://www.huya.com/'


def send_msg(text='title',desp='desp'):
    notify_url = 'https://sc.ftqq.com/' + os.getenv('scu_key') +'.send'
    r = requests.post(notify_url,data={'text':text,'desp':desp},timeout=5)
    return r and r.ok and r.json()['errmsg'] == 'success'

def fetch(file_path):
    with open(file_path,'r',encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            # print(line)
            a,b = line.split(':')
            anchors.append((a,b))
    txt = '| 主播 | 标题 | 状态 | 订阅 |\n|:---:|:---:|:---:|:---:|\n'
    for suffix,anchor in anchors:
        # time.sleep(100)
        print('watching:',anchor)
        try:
            r = requests.get(huya_url + suffix,timeout=3)
            html = r.content.decode('utf-8')
            newaddr = re.find(r'更换为.+href="https://www.huya.com/(.+)"',html)
            print(newaddr)
            if newaddr:
                print('NEW:',anchor,suffix,'->',newaddr)
                anchors.append((newaddr,anchor))
                continue
            title = re.findall(r'<h1 id="J_roomTitle">(.+)</h1>',html)[0]
            status = re.findall(r'id="live-count">(.+?)</em></span>',html)
            fans = re.findall(r'id="activityCount">(\d+)</div>',html)[0]
            last_live = '未直播'
            if status and status[0]:
                last_live = status[0]
        except:
            print('ERROR:' + huya_url + suffix)
        else:
            txt += ('|' + anchor + '|' + title + '|' + last_live + '|' + fans + '|\n')
    print(txt)
    return
    if send_msg('主播直播状态',txt):
        print('wechat message push success.')
    else:
        print('wechat message push failed.')

if __name__ == '__main__':
    fetch()