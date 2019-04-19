"""主程序"""
import face_recognition
import numpy as np

from PIL import Image

from tools.db import executeSql, conn_redis
from io import BytesIO as Bytes2Data
from io import BufferedReader


def init():
    """
    初始化函数，对底库数据进行加载、特征提取、存储（定时执行,最好实现增量转换）
    :return:
    """
    sql = 'select id_card,image from face_recognition'
    datum = executeSql(sql, returnDict=True)
    r, pipe = conn_redis()
    for item in datum:
        id_card = item['id_card']
        image = item['image']
        # 过滤掉没有图片的数据
        if image != b'':
            feceFeature = featureExt(image)
            # 矩阵类型转为字符串类型
            imageStr = np.array2string(feceFeature)
            r.set(id_card, imageStr)
    pipe.execute()

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
    # 显示图片
    # im.show()
    width, height = im.size
    im = im.convert("L")
    data = im.getdata()
    data = np.matrix(data, dtype='float') / 255.0
    new_data = np.reshape(data, (height, width))
    return new_data


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
    加载底库中人像的特征数据
    :return:[(身份证号：特征数据),]
    """
    r, pipe = conn_redis()
    pipe = r.pipeline()
    keys = r.keys()
    for key in keys:
        pipe.get(key)
        IdImages = zip(keys, pipe.execute())
    return IdImages

def searchSimImage(unKnowImage):
    """
    特征匹配，返回相似人员信息
    :param unKnowImage: 可以传入1、图像路径 2、图像文件 3、图像字符串流
    :return:
    """
    unknown_face_encodings = featureExt(unKnowImage)
    similar_size = 0.48
    ids, knownImages = zip(*loadKnownImage())
    ids = list(ids)
    knownImages = list(knownImages)
    index = 0
    results = []
    if len(unknown_face_encodings) > 0:
        face_distances = face_recognition.compare_faces(knownImages, unKnowImage, tolerance=0.50)
        for face_distance in face_distances:
            if face_distance < similar_size:
                results.append({"score":face_distance,"path":ids[index]})
                index += 1
            else:
                index += 1
                continue
        sorted_results = sorted(results, key=lambda k: k["score"])
        if len(sorted_results) > 5:
            return sorted_results[0:5]
        else:
            return sorted_results
    else:
        return "图片中未识别到人脸"



def action(image):
    """程序入口"""
    searchSimImage(image)



if __name__ == '__main__':
    action('cs.jpg')
