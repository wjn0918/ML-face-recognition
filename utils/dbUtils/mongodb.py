from utils.dbUtils.DB import DB
from pymongo import MongoClient


class MongoDB(DB):

    def __init__(self, user, password, host="localhost", port=27017):
        self.user = user
        self.password = password
        self.host = host
        self.port = port

        pass

    def conn(self):
        self.client = MongoClient(
            'mongodb://{user}:{password}@{host}:{port}'.format(user=self.user, password=self.password, host=self.host,
                                                               port=self.port))
        return self.client
        pass

    def close(self):
        self.client.close()
        pass
