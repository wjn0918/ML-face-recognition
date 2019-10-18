"""
图像预处理
"""
import face_recognition
import pickle
from utils.dbUtils.mongodb import MongoDB
from hdfs.client import Client
import hdfs
from PIL import Image
import numpy as np
from io import BytesIO as Bytes2Data
from utils.faceStore import contantImagePath

client = Client("http://10.205.246.37:50070")

def ifContainFace(file_path):
    try:
        file_path = contantImagePath(file_path)
        with client.read(file_path) as reader:
            content = reader.read()
        img = np.array(Image.open(Bytes2Data(content)))
    except hdfs.util.HdfsError:
        return file_path
    try:
        face_features = face_recognition.face_encodings(img)
    except RuntimeError:
        face_features = []

    # try:
    #     img = face_recognition.load_image_file(file_path)
    # except FileNotFoundError:
    #     return "文件不存在"
    # face_features = face_recognition.face_encodings(img)
    if len(face_features) > 0:
        return face_features[0]
    else:
        return "图像中不包含人像"
    pass



def ifInDB(rec_face_features):
    """
    是否存在于数据库中
    :param file_path:
    :return:
    """
    similar_size = 0.48
    r = []

    db = MongoDB(user='zfw_ww',password='Beiming888',host='10.205.246.50').conn().facedb
    my_set = db.face_features
    for i in my_set.find():
        distance = face_recognition.face_distance(pickle.loads(i['face_features']), rec_face_features)[0]
        if distance < similar_size:
            print(distance)
            r.append({'id_card': i['id_card'], 'image_path': i['image_path'], 'distance': distance})
    # 按相似度进行排序
    r = sorted(r, key=lambda k: k['distance'])
    if len(r) > 0 :
        return r
    else:
        return "库中不存在"