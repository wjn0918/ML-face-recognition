"""
hive 数据库连接
"""
from utils.dbUtils.DB import DB
from pyhive import hive

class HiveDB(DB):
    def __init__(self, host):
        self.host = host
        pass


    def conn(self):
        self.con = hive.connect(self.host, auth='NOSASL')
        return self.con
        pass

