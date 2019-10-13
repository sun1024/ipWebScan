#!/usr/bin/python
# -*- coding:utf-8 -*-
# author:b1ng0

import requests
from lxml import etree
from models import *
import threading
from queue import Queue
from config import config
from qqwry import QQwry
import re

# 使用纯真IP数据库
q = QQwry()
q.load_file('qqwry.dat')

def getTitle(reps):
    try:
        page = etree.HTML(reps.text)
        title = page.xpath('/html/head/title/text()')
        title = title[0].strip()
    except:
        title = ''
    return title


def getIporigin(ip):
    result = q.lookup(ip)
    return result[1]


def parserData(url, ip, port, reps):
    iporigin = getIporigin(ip)
    httpcode = reps.status_code
    webcode = reps.text
    title = getTitle(reps)
    webtype = reps.headers.get('server')
    charsetcode = reps.encoding

    addData([url, ip, iporigin, port, httpcode, webcode, title, webtype, charsetcode])


class scan(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while not self.queue.empty():
            ip, port = self.queue.get()
            url = 'http://%s:%s' % (ip,port)
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'
                }
            print('%s ---------- 开始识别咯~' % url)
            try:
                reps = requests.get(url, headers=headers, timeout=5, allow_redirects=False)
                reps.raise_for_status()
                reps.encoding = reps.apparent_encoding
                parserData(url, ip, port, reps)
            except Exception as e:
                print('%s ---------- web不能访问哟~' % url)
            else:
                print('%s ---------- 已经写入数据库啦~' % url)


def run():
    queue = Queue()

    with open('ip.txt', 'r') as ips:
        for ip in ips:
            # 处理ip段
            try:
                ip_start, ip_stop = ip.split(' ')
                pre_ip = re.findall(r'(\d+\.\d+\.\d+\.)\d+', ip_start)[0]
                start_num = re.findall(r'\d+\.\d+\.\d+\.(\d+)', ip_start)[0]
                stop_num = re.findall(r'\d+\.\d+\.\d+\.(\d+)', ip_stop)[0]
                count = int(stop_num) - int(start_num)
            except:
                raise Exception('ip.txt格式错误~')
            for i in range(count):
                fix_ip = pre_ip + str(int(start_num)+i)
                for port in config.scan_ports:
                    queue.put([fix_ip, port])

    threads = []
    thread_num = config.thread_num

    for i in range(thread_num):
        threads.append(scan(queue))
    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == "__main__":
    run()