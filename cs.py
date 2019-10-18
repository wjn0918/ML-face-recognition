# from utils.dbUtils.mongodb import MongoDB
import pickle
from bson.binary import Binary

# con = MongoDB().conn()
# db = con.facedb
# my_set = db.face_features
#
# import face_recognition
#
# img_path = "D:\soft\dlib\dlib-master\examples\johns\John_Salley\\2.jpg"
#
# img = face_recognition.load_image_file(img_path)
# encoding_face = face_recognition.face_encodings(img)
# r = {"123456": encoding_face}
# my_set.insert({'id_card':'123456','image_path':img_path,'image': Binary(pickle.dumps(encoding_face, protocol=-1), subtype=128)})
# con.close()
#
# print(type(encoding_face))

# con = MongoDB().conn()
# db = con.test
# my_set = db.test_set
# for i in my_set.find():
#     image = pickle.loads(i['image'])
#     print(image)
# con.close()


"""
hive
"""

# from utils.dbUtils.hivedb import HiveDB
#
#
# db = HiveDB(host="10.205.246.37")
# cursor = db.conn().cursor()
# cursor.execute("SELECT * FROM hbzfw.dm_wh_cs LIMIT 100")
# r = cursor.fetchall()
# print(r)





"""
sqlite
"""


# from utils.dbUtils.sqlitedb import SqliteDB
#
# con = SqliteDB("test.db").conn()
# cursor = con.cursor()
#
# sql = """create table IF NOT EXISTS last_time(
#     id int not null,
#     last_time timestamp
# );"""
# cursor.execute(sql)
#
#
# con.close()




"""
1. 读取sqlite中最后一次同步时间
读取hive中身份id，图像存储路径
"""
# from utils.dbUtils.hivedb import HiveDB
# from utils.dbUtils.sqlitedb import SqliteDB
#
#
# table_name = ""
#
# sqlite_con = SqliteDB("synctime.db").conn()
# hive_con = HiveDB(host="10.205.246.37").conn()
# sqlite_cursor = sqlite_con.cursor()
# hive_cursor = hive_con.cursor()
# xgsj_sql = "SELECT WW_XGSJ FROM hbzfw.dm_wh_cs LIMIT 100"
# hive_cursor.execute(xgsj_sql)
# last_time = hive_cursor.fetchall()
# def init():
#     sql = """CREATE TABLE IF NOT EXISTS last_time(
#         id int not null,
#         last_time timestamp
#     );"""
#     sqlite_cursor.execute(sql)
# def update_time(last_time):
#     sql = """
#         UPDATE last_time SET last_time = {last_time}
#     """.format(last_time=last_time)
#     sqlite_cursor.execute(sql)
#
# sqlite_cursor.execute("""
#     SELECT last_time FROM last_time;
# """)
# last_time = max(sqlite_cursor.fetchall())
#
# sql = "SELECT id_card, image_path FROM {table_name} WHERE ww_xgsj > {last_time}".format(table_name=table_name, last_time=last_time)
# hive_cursor.execute(sql)
# r = hive_cursor.fetchall()
#
# sqlite_con.close()
# hive_con.close()



#
# from utils.dbUtils.mongodb import MongoDB
# con = MongoDB().conn()
# db = con.facedb
# my_set = db.face_info
# my_set.insert({'ww_sfz':'123456','image_path':'/test/face/3.jpg','ww_cjsj':'2001:01:01', 'ww_xgsj': '',})


# import face_recognition
# from hdfs.client import Client
# from PIL import Image
# import numpy as np
#
# client = Client("http://10.205.246.37:50070")
# with client.read("/test/face/3.jpg") as reader:
#     content = reader.read()
# im = Image.open(content)
# r = np.array(im)
# print(face_recognition.face_encodings(r))

# from PIL import Image
# import face_recognition
# import numpy as np
# from io import BytesIO as Bytes2Data
# img_path = "D:\soft\dlib\dlib-master\examples\johns\John_Salley\\2.jpg"
# with open(img_path,'rb') as reader:
#     content = reader.read()
# img = Image.open(Bytes2Data(content))
# r = np.array(img)
# face_recognition.face_encodings(r)








"""
hdfs 
"""

# from hdfs.client import Client
import numpy as np
# from io import BytesIO as Bytes2Data
# from PIL import Image
#
# img_path = "/test/face/1.jpg"
# client = Client("http://10.205.246.37:50070")
# with client.read(img_path) as reader:
#     content = reader.read()
# img = Image.open(Bytes2Data(content))
# r = np.array(img)





"""
达梦
"""


import dmPython


from utils.faceStore import cs

cs()





