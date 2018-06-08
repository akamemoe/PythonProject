#coding=utf-8

from flask import Flask
from flask import request,redirect,render_template
from PIL import Image

import json
import os,time

app = Flask(__name__)

config = {
    'project_folder':'/home/<user>/sm',
    'folder':'upload',
    'host':'http://www.gentlehu.com'
}
def now_time():
    return int(round(time.time() * 1000))

def makejson(w,h,filename,storename,content_length,pth,cur_time):
    rs = {
        'status':'success',
        'data':{
            'width': w,
            'height': h,
            'filename': filename,#上传的文件名
            'storename': storename,#存储时候的文件名
            'size': content_length,
            'path': pth,
            'hash': '9527',
            'timestamp': cur_time,
            'url':'{}/{}'.format(config['host'],pth),
            'delete': 'http://www.gentlehu.com/api/delete/9527#not_support_yet'
        }
    }
    return rs


@app.route('/api/upload',methods=['POST'])
def api_upload():

    try:
        file = request.files['smfile']
        fdate = time.strftime("%Y/%m/%d", time.localtime())
        cur_time = now_time()
        storename = '{}{}'.format(cur_time,os.path.splitext(file.filename)[1])
        fdir = '{}/{}'.format(config['folder'],fdate)
        if not os.path.exists(fdir):
            os.makedirs(fdir)
        pth = '{}/{}'.format(fdir,storename)
        file.save(pth)
        img = Image.open(file,mode='r')
        w,h = img.size
        cl = file.content_length
        img.close()
        file.close()
        rs = makejson(w,h,file.filename,storename,cl,pth,cur_time)  
        return json.dumps(rs)
    except Exception as e:
        print(e)
        return json.dumps({'status':'error','msg':'upload error.please try again later.[{}]'.format(e)})

# @app.route('/',methods=['GET'])
# def hello():
#     return redirect('index.html')

def main():
    app.run()

if __name__ == '__main__':
    main()