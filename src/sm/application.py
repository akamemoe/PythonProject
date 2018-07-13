#coding=utf-8

from flask import Flask,Response
from flask import request,redirect,render_template,make_response,jsonify,abort
from flask import g
from PIL import Image
import os,time,re,datetime,json
import sqlite3,logging,shortuuid
from werkzeug.contrib.fixers import ProxyFix


app = Flask(__name__)
#修正在有nginx等前置代理的情况下自身的log打印的IP总是127.0.0.1的问题
app.wsgi_app = ProxyFix(app.wsgi_app)

CONFIG = {
    'project_folder':'/home/<user>/sm',
    'folder':'upload',
    'host':'https://www.gentlehu.com',
    'id_name':'_uid',
    'dbpath':'./sm.db'
}
#log config
DEFAULT_FORMATTER = logging.Formatter(
    fmt='%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
fhandler = logging.FileHandler('smserver_run.log', mode='a')
fhandler.setFormatter(DEFAULT_FORMATTER)
fhandler.setLevel(logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(fhandler)
logger.setLevel(logging.INFO)

init_sql = '''
create table if not exists records(
    uid varchar(25) not null,
    path text not null,
    hashval text not null,
    created timestamp not null default (datetime(current_timestamp,'localtime'))
);
'''

def getconn():
    conn = getattr(g,'_conn',None)
    if conn is None:
        print('connect to db.')
        conn = g._conn = sqlite3.connect(CONFIG['dbpath'])
    return conn

@app.before_first_request
def inittables():
    with app.app_context():
        conn = getconn()
        conn.cursor().executescript(init_sql)
        conn.commit()

@app.teardown_appcontext
def close_conn(ex):
    conn = getattr(g,'_conn',None)
    if conn:
        conn.close()


def insert(uid,path,hashval):
    con = getconn()
    c = con.cursor()
    c.execute('insert into records(uid,path,hashval) values(?,?,?)',(uid,path,hashval))
    con.commit()
    c.close()

def query(column,val):
    con = getconn()
    #不知道为什么把列名也用?占位会不起作用。
    c = con.execute('select uid,path,hashval,created from records where {} = ? order by created desc'.format(column),(val,))
    return c.fetchall()

def deletebyhash(hashval):
    con = getconn()
    c = con.execute('delete from records where hashval = ?',(hashval,))
    c.close()
    con.commit()

def now_time():
    return int(round(time.time() * 1000))

def makedict(fname,sname,path,hashval):
    rs = {
        'status':'success',
        'data':{
            'filename': fname,#上传的文件名
            'storename': sname,#存储时候的文件名
            'path': path,
            'hash': hashval,
            'url':'{}/{}'.format(CONFIG['host'],path),
            'delete': 'https://www.gentlehu.com/api/delete/{}'.format(hashval)
        }
    }
    return rs


@app.route('/api/upload',methods=['POST'])
def api_upload():

    try:
        uid = request.cookies.get(CONFIG['id_name'])
        if not uid:
            uid = shortuuid.uuid()
        file = request.files['smfile']
        extname = os.path.splitext(file.filename)[1].lower()
        if extname not in ['.jpg','.jpeg','.png']:
            return make_response(jsonify({'status':'error','msg':'image format not support.'}))
        fdate = time.strftime("%Y/%m/%d", time.localtime())
        cur_time = now_time()
        #存储文件名由uid前三位 + 时间戳 + 原扩展名组成
        storename = '{}{}{}'.format(uid[:3],cur_time,extname)
        fdir = '{}/{}'.format(CONFIG['folder'],fdate)
        if not os.path.exists(fdir):
            os.makedirs(fdir)
        path = '{}/{}'.format(fdir,storename)
        file.save(path)
        file.close()

        logger.info('upload -> uid:%s - ip:%s - storename:%s - origin:%s', uid, request.headers.get('X-Real-IP'),storename,file.filename)
        hashval = shortuuid.ShortUUID().random(length=12)
        jsondata = makedict(file.filename,storename,path,hashval)  
        outdate = datetime.datetime.today() + datetime.timedelta(days=180)
        resp = make_response(json.dumps(jsondata))
        resp.set_cookie(CONFIG['id_name'],uid,expires=outdate)
        insert(uid,path,hashval)
        return resp
    except Exception as e:
        logger.error('an error occur ex:%s',e)
        return jsonify({'status':'error','msg':'upload error.please try again later.'})

@app.route('/api/list',methods=['GET'])
def imagelist():
    uid = request.cookies.get(CONFIG['id_name'])
    if uid:
        rs = query('uid',uid)
        urls = [{'date':c,
                'url':'{}/{}'.format(CONFIG['host'],p),
                'delete':'{}/api/delete/{}'.format(CONFIG['host'],h)} for (u,p,h,c) in rs]
        jsondata = {'status':'success','count':len(urls),'urls':urls,'uid':uid}
        return jsonify(jsondata)
    else:
        return jsonify({'status':'success','msg':'not found.'})

@app.route('/api/delete/<hashval>',methods=['GET'])
def delete(hashval):
    uid = request.cookies.get(CONFIG['id_name'])
    r = query('hashval',hashval)
    if r and r[0]:
        safe_remove(uid,r[0][1])
        deletebyhash(hashval)
        return jsonify({'status':'success','msg':'success deleted.'})
    abort(404)


@app.route('/showip',methods=['GET'])
def showip():
    return jsonify({'ip':request.headers.get('X-Real-IP')})


def safe_remove(uid,path):
    #只允许删除上传目录的内容，防止构造URL(类似：/path/../../a.jpg)删除其他文件
    apath = os.path.abspath(path)
    allow_floder = os.path.abspath(CONFIG['folder'])
    if apath.startswith(allow_floder):
        os.remove(apath)
    else:
        logger.warn('permission denied to delete [%s],uid:%s',apath,uid)

def main():
    app.run()

if __name__ == '__main__':
    main()