"""
人像特征数据存储到Mongodb中
1. 读取sqlite中最后一次同步时间
2. 读取mongodb中身份id，图像存储路径
"""

from utils.dbUtils.sqlitedb import SqliteDB
from utils.dbUtils.mongodb import MongoDB
from utils.dbUtils.dmdb import DmDB
from PIL import Image
import face_recognition
import numpy as np
from io import BytesIO as Bytes2Data
from hdfs.client import Client
import pickle
from bson.binary import Binary
import hdfs

db = MongoDB(user='zfw_ww',password='Beiming888',host='10.205.246.50').conn().facedb
get_set = db.face_info
insert_set = db.face_features

sqlite_con = SqliteDB("synctime.db").conn()

sqlite_cursor = sqlite_con.cursor()

# client = Client("http://47.98.207.67:50070")
client = Client("http://10.205.246.37:50070")

dm_cursor = DmDB().conn().cursor()

def appInit():
    sql = """CREATE TABLE IF NOT EXISTS last_time(
        id int not null,
        last_time timestamp
    );"""
    sqlite_cursor.execute(sql)


def syncFace():
    last_time = "1970:01:01"
    update_time(last_time)
    last_time = get_last_time_from_local()
    datas = get_data_from_mongo(last_time)
    sync2db(datas)


def update_time(last_time):
    sql = """
        UPDATE last_time SET last_time = '{last_time}'
    """.format(last_time=last_time)
    sqlite_cursor.execute(sql)


def get_last_time_from_local():
    sql = """
        SELECT last_time from last_time
    """
    sqlite_cursor.execute(sql)
    return max(sqlite_cursor.fetchall())


def get_data_from_mongo(last_time):
    return get_set.find({"ww_xgsj":{"$gte":last_time}})
    pass


def get_data_from_dm(last_time):
    # cursor = dmPython.connect(user='ZFW_WW_BM', password='ZFW_WW_BM', server='10.205.246.50', port=5236,
    #                           # autoCommit=True).cursor()
    sql = "SELECT ww_sfzh, ww_zp FROM t_zdmb_zdryzp WHERE ww_xgsj >= '{last_time}'".format(last_time = last_time)
    dm_cursor.execute(sql)
    return dm_cursor.fetchall()
    pass

def img2array(img_paths):
    # img_path = "D:\soft\dlib\dlib-master\examples\johns\John_Salley\\2.jpg"
    face_encodings = []
    if img_paths is None:
        return "数据为None"
    else:
        img_paths = str(img_paths)[1:-1].split(",")
        if len(img_paths) == 0 :
            return "没有照片信息"
        else:
            # return "有照片"
            try:
                for img_path in img_paths:
                    img_path = contantImagePath(img_path)
                    print(img_path)
                    with client.read(img_path) as reader:
                        content = reader.read()
                    img = Image.open(Bytes2Data(content))
                    r = np.array(img)
                    try:
                        face_features = face_recognition.face_encodings(r)
                    except RuntimeError:
                        face_features = []
                    if len(face_features) > 0:
                        face_encodings.append(face_features[0])
                return face_encodings
            except hdfs.util.HdfsError:
                return "hdfs 上文件不存在"

def contantImagePath(image_path):
    pre = "/document/"
    img_name = image_path.split("/")[-1][:-1]
    sql = "SELECT ww_wjsha FROM T_FILE_WJXX WHERE ww_wjmc = '{img_name}'".format(img_name = img_name)
    dm_cursor.execute(sql)
    try:
        mid = dm_cursor.fetchone()[0]
    except:
        return image_path + "文件地址不存在"
    return pre+mid+img_name
    pass

def sync2db(datas):
    for data in datas:
        id_card = data[0]
        image_path = data[1]
        print(id_card,'\t', image_path)
        face_features = img2array(image_path)
        if isinstance(face_features, str):
            print(face_features, "\t 中不包含人像")
        else:
            for face_feature in face_features:
                record = {'ww_sfz': id_card, 'image_path':image_path,'face_features': Binary(pickle.dumps(face_feature, protocol=-1), subtype=128)}
                insert_set.insert(record)
                print("插入：", image_path)
    pass

def faceStore():
    last_time = "2019-10-17 12:04:11"
    datas = get_data_from_dm(last_time)
    sync2db(datas)




if __name__ == '__main__':
    last_time = ""
    r = get_data_from_dm(last_time)
    print(r)
    # sync2db(r)
