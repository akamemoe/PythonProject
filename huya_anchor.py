#encoding=utf-8

import requests
import re


anchors = []
base_url = 'http://www.huya.com/'

def send_msg(text='title',desp='desp'):
    base_url = 'https://sc.ftqq.com/' + os.getenv('scu_key') +'.send'
    r = requests.post(base_url,params={'text':text,'desp':desp})
    return True if r and r.status_code == 200 else False

def fetch():
    with open('anchors.txt','r',encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            print(line)
            a,b = line.split(':')
            anchors.append((a,b))
    txt = '|  主播   |      标题      |  状态 |\n|:----------:|:-------------:|:------:|\n'
    for suffix,anchor in anchors:
        r = requests.get(base_url + suffix)
        html = r.content.decode('utf-8')
        title = re.findall(r'<h1 id="J_roomTitle">(.+)</h1>',html)[0]
        status = re.findall(r'<span class="host-prevStartTime"><i></i><span>(.+)</span></span>',html)
        last_live = '直播中'
        if status and status[0]:
            last_live = status[0]
        # print(anchor + '->' + title + '->' + last_live)
        txt += ('|' + anchor + '|' + title + '|' + last_live + '|\n')
    # with open('result.txt','w',encoding='utf-8') as f:
    #     f.write(txt)
    if send_msg('主播直播状态',txt):
        print('wechat message push success.')
    else:
        print('wechat message push failed.')

if __name__ == '__main__':
    fetch()