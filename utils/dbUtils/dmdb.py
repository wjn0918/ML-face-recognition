from utils.dbUtils.DB import DB
import dmPython

class DmDB(DB):
    def __init__(self):
        pass

    def conn(self, user='ZFW_WW_BM', password='ZFW_WW_BM', server='10.205.246.50', port=5236):
        return dmPython.connect(user, password, server, port, autoCommit=True)
        pass


