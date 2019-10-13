#!/usr/bin/python
# -*- coding:utf-8 -*-
# author:b1ng0

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from config import config


#创建对象的基类：
Base = declarative_base()

#定义User对象：
class ip_data(Base):
    #表名：
    __tablename__ = 'ip_data'

    #表结构:
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    url = Column(String(200))
    ip = Column(String(100))
    iporigin = Column(String(100))
    port = Column(String(100))
    httpcode = Column(String(20))
    webcode = Column(LONGTEXT())
    title = Column(String(1000))
    webtype = Column(String(100))
    charsetcode = Column(String(100))

def getEngine():
    #初始化数据库连接
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://' \
        + config.user + ':' \
        + config.password + '@' + config.host + ':' \
        + str(config.port) + '/' + config.database
    engine = create_engine(SQLALCHEMY_DATABASE_URI, encoding="utf-8", poolclass=NullPool)
    Base.metadata.create_all(engine)
    return engine

def addData(data):
    engine = getEngine()

    #创建session类型
    DBSession = sessionmaker(bind=engine)

    #创建session对象
    session = DBSession()

    #创建新的user对象
    new_data = ip_data(url=data[0],\
        ip=data[1],\
        iporigin=data[2],\
        port=data[3],\
        httpcode=data[4],\
        webcode=data[5],\
        title=data[6],\
        webtype=data[7],\
        charsetcode=data[8],\
            )

    #添加单条数据
    session.add(new_data)

    #提交即保存到数据库
    session.commit()

    #关闭session
    session.close()
