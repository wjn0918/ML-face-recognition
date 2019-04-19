"""
使用连接池连接数据库，执行sql

"""
import pymysql
import redis
from DBUtils.PooledDB import PooledDB

from pymongo import MongoClient

from configparser import ConfigParser
#读取配置
from pymysql.cursors import DictCursor

cf = ConfigParser()
cf.read('conf/db.ini')


def conn_mysql():
    """
    通过线程池，创建MySQL连接对象，线程数设为5
    :return:
    """
    items = dict(cf.items('mysql'))
    host = items['host']
    user_name = items['user_name']
    password = items['password']
    db = items['db']
    pool = PooledDB(pymysql, 5, host=host, user=user_name, passwd=password, db=db, port=3306, setsession=['SET AUTOCOMMIT = 1'])
    # 5为连接池里的最少连接数，setsession=['SET AUTOCOMMIT = 1']是用来设置线程池是否打开自动更新的配置，0为False，1为True
    conn = pool.connection()
    return conn


def conn_mongodb():
    """
    获取mongodb连接
    :return:
    """
    items = dict(cf.items('mongodb'))
    host = items['host']
    client = MongoClient(host, 27017)
    # 连接mydb数据库,账号密码认证
    db = client.cs
    return db


def conn_redis():
    """
    连接redis
    :return:redis 连接对象、管道
    pipe = r.pipeline(transaction=True)
    r.set('name', 'zhangsan')
    r.set('name', 'lisi')
    pipe.execute()
    """

    items = dict(cf.items('redis'))
    host = items['host']
    pool = redis.ConnectionPool(host=host, port=6379, db='', decode_responses=True)
    r = redis.Redis(connection_pool=pool)
    pipe = r.pipeline(transaction=True)
    return r, pipe




def executeSql(sql,args=None,returnDict=False):
    """
    执行sql
    :param sql:sql 语句
    :param args: sql 中的参数
    :param returnDict: 是否创建返回字典类型游标
    :return: 查询的所有结果
    """
    conn = conn_mysql()
    if returnDict:
        cursor = conn.cursor(DictCursor)
    else:
        cursor = conn.cursor()
    cursor.execute(sql, args)
    r = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return r
    pass


if __name__ == '__main__':
    conn_mongodb()