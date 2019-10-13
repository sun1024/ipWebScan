#!/usr/bin/python
# -*- coding:utf-8 -*-
# author:b1ng0

class config():
    # 线程数
    thread_num = 200
    # msyql配置信息
    host = '127.0.0.1'
    port = 3306
    database = 'ip_scan'
    user = 'root'
    password = 'mysql2333'
    # 要扫描的端口
    scan_ports = [80, 8080]
