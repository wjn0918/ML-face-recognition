"""主程序"""
import face_recognition
import pickle

import numpy as np

from PIL import Image
from bson.binary import Binary

from tools.db import executeSql, conn_redis, conn_mongodb
from io import BytesIO as Bytes2Data
from io import BufferedReader


def init():
    """
    初始化函数，对底库数据进行加载、特征提取、存储（定时执行,最好实现增量转换）
    :return:
    """
    cs = []
    sql = 'select id_card,image from face_recognition'
    datum = executeSql(sql, returnDict=True)
    db = conn_mongodb()
    data_set = db.id_face
    for item in datum:
        print(item)
        image = item['image']
        # 过滤掉没有图片的数据
        if image != b'':
            faceFeature = featureExt(image)
            data_set.insert_one({'id_card':item['id_card'],'image': Binary(pickle.dumps(faceFeature, protocol=-1), subtype=128)})
    pass


def accUnkownImage():
    """
    接收需要检索的人像
    :return:
    """
    pass


def image2Matrix(filename):
    """
    将传入的图像转化为矩阵
    :@param filename: 可以传入1、图像路径 2、图像文件 3、图像字符串流
    :return:new_data图像矩阵类型  numpy.matrix
    """

    # 读取图片
    print(type(filename))
    if isinstance(filename, str) or isinstance(filename, BufferedReader):
        im = Image.open(filename)
    elif isinstance(filename, bytes):
        im = Image.open(Bytes2Data(filename))
    im = im.convert('RGB')
    return np.array(im)


# 对接收的人像进行特征提取
def featureExt(filename):
    """
    提取人像特征数据
    :param filename: 可以传入1、图像路径 2、图像文件 3、图像字符串流
    :return:图像中人像特征矩阵类型数据(只获取图像中第一个人像)
    """
    imageMatrix = image2Matrix(filename)
    faceFeature = face_recognition.face_encodings(imageMatrix)[0]

    return faceFeature


def loadKnownImage():
    """
    加载mongodb库id_face中人像的特征数据
    :return:[(身份证号：特征数据),]
    """
    idImages = []
    db = conn_mongodb()
    my_set = db.id_face
    for i in my_set.find():
        id_card = i['id_card']
        image = pickle.loads(i['image'])
        idImages.append((id_card,image))
    return idImages

def searchSimImage(unKnowImage):
    """
    特征匹配，返回相似人员信息
    :param unKnowImage: 可以传入1、图像路径 2、图像文件 3、图像字符串流
    :return:
    """
    unknown_face_encodings = featureExt(unKnowImage)
    similar_size = 0.48
    index = 0
    results = []
    id_cards, known_faces = zip(*loadKnownImage())
    id_cards = list(id_cards)
    known_faces = list(known_faces)
    if len(unknown_face_encodings) > 0:
        face_distances = face_recognition.face_distance(known_faces, unknown_face_encodings)
        for face_distance in face_distances:
            if face_distance < similar_size:
                results.append({"score":face_distance,"id_card":id_cards[index]})
                index += 1
            else:
                index += 1
                continue
        sorted_results = sorted(results, key=lambda k: k["score"])
        if len(sorted_results) > 5:
            return sorted_results[0:5]
        else:
            if len(sorted_results) == 0:
                return "数据库中不存在"
            else:
                return sorted_results
    else:
        return "上传图片中未识别到人脸"



def action(image):
    """程序入口"""
    searchSimImage(image)



if __name__ == '__main__':
    r = searchSimImage('cs.jpg')
    print(r)


