import pymysql
from DBUtils.PooledDB import PooledDB

from configparser import ConfigParser
#读取配置
cf = ConfigParser()
cf.read('conf/db.conf')


def conn_mysql():
    host = cf.get('mysql','host')
    user_name = cf.get('mysql','user_name')
    password = cf.get('mysql', 'password')
    db = cf.get('mysql', 'db')
    pool = PooledDB(pymysql, 5, host=host, user=user_name, passwd=password, db=db, port=3306, setsession=['SET AUTOCOMMIT = 1'])  
    # 5为连接池里的最少连接数，setsession=['SET AUTOCOMMIT = 1']是用来设置线程池是否打开自动更新的配置，0为False，1为True
    conn = pool.connection()
    return conn


def executeSql(sql,args=None):
    """
    执行sql
    :param sql:sql 语句
    :param args: sql 中的参数
    :return: 查询的所有结果
    """
    conn = conn_mysql()
    cursor = conn.cursor()
    cursor.execute(sql,args)
    r = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return r
    pass


if __name__ == '__main__':
    conn = conn_mysql()
    cursor = conn.cursor()
    sql = 'select * from face_recognition'
    cursor.execute(sql)
    print(cursor.fetchall())
    conn.commit()
    cursor.close()
    conn.close()
