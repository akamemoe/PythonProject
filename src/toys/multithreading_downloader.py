#coding=utf-8

import requests
import time,os,re
import hashlib
import threading
import argparse


class Downloader():

    def __init__(self,url,finalname,threadCount,timeout=10):
        self.url = url
        self.finalname = finalname
        self.threadCount = threadCount
        self.timeout = timeout
        self.md5 = hashlib.md5(self.url.encode('utf-8')).hexdigest()
        self.threads = []
        self.dirctory = '.'

    def query_content_length(self):
        r = requests.head(self.url,timeout=self.timeout)
        if r and r.headers['Content-Length']:
            return int(r.headers['Content-Length'])
        else:
            return 0

    def download(self):
        filesize = self.query_content_length()
        blocksize = filesize // self.threadCount
        n = self.threadCount - 1
        #先下载整除的部分然后下载剩余部分
        for order in range(n):
            self._build_threads(order,order*blocksize,(order+1)*blocksize-1)
        self._build_threads(n,n*blocksize,filesize)
        self._start_threads()
        self._merge_file()

    def _start_threads(self):
        for t in self.threads:
            t.start()
            t.join()

    def _build_threads(self,order,start,end):
        tmpfile = os.path.join(self.dirctory,'{}.download-{}'.format(self.md5,order))
        task = DownloadTask(self.url,tmpfile,start,end,self.timeout)
        self.threads.append(task)

    def _rewrite(self,fw,fr):
        chunksize = 1024 * 1024 #1M
        while True:
            chunk = fr.read(chunksize)
            if chunk:
                fw.write(chunk)
            else:
                break

    def _merge_file(self):
        filelist = os.listdir(self.dirctory)
        with open(os.path.join(self.dirctory,self.finalname),'wb') as fw:
            for order in range(self.threadCount):
                pth = os.path.join(self.dirctory,'{}.download-{}'.format(self.md5,order))
                if os.path.exists(pth):
                    with open(pth,'rb') as fr:
                        self._rewrite(fw,fr)


class DownloadTask(threading.Thread):
    def __init__(self,url,tmpfile,start,end,timeout):
        super().__init__()
        self._url = url
        self._tmpfile = tmpfile
        self._start = start
        self._end = end
        self._timeout = timeout
        self._postion = os.stat(self._tmpfile).st_size if os.path.exists(self._tmpfile) else 0
        self._chunksize = 1024

    def run(self):
        print('START[DownloadTask]:{}->{}#{}-{}'.format(self._url,self._tmpfile,self._start,self._end))
        headers = {
            'Range':'bytes={}-{}'.format(self._start+self._postion,self._end)
        }
        with requests.get(self._url,headers=headers,timeout=self._timeout,stream=True) as r:
            if r.status_code != 200 and r.status_code != 206:
                return
            with open(self._tmpfile,'ab') as f:
                print('r.headers:',r.headers)
                for chunk in r.iter_content(self._chunksize):
                    f.seek(self._postion)
                    f.write(chunk)
                    self._postion+=len(chunk)

        print('END[DownloadTask]:{}->{}#{}-{}'.format(self._url,self._tmpfile,self._start,self._end))


def main():
    parse = argparse.ArgumentParser()
    parse.add_argument("-u",type=str,help="file url.",required=True)
    parse.add_argument("-n",type=int,default=3,help="the number of threading.",choices=range(1,10))
    parse.add_argument("-o",type=str,default='',help="file name.")
    args = parse.parse_args()

    if args.o is None or args.o == '':
        args.o = args.u[args.u.rindex('/')+1:]
    # print(args)
    downloader = Downloader(args.u,args.o,args.n)
    try:
        downloader.download()
    except Exception as e:
        print('download error!-->',e)
    else:
        print('downloader done.')
        

def processer():
    ch = '■'
    for x in range(1,21):
        ss = 'downloading[{}]({}%)'.format(ch*x,int(x/20*100))
        print(ss,end='',flush=True)
        time.sleep(1)
        print('\b'*90,end='')


if __name__ == '__main__':
    main()
