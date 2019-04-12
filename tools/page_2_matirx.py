"""
将图片转化为矩阵特征值进行存储
"""

import load_data
import face_recognition
import numpy as np
import os
import datetime

def face_2_matrix():
    """
    将图片转化为矩阵类型，并提取人脸特征值，存储成*.out类型文件
    """
    num = 0
    for filePath in file_paths:
        path = filePath.split('/')[-1].split('.')[0]+".out"
        try:
            obj = face_recognition.face_encodings(face_recognition.load_image_file(filePath))[0]
        except:
            continue
        absPath = '/cs/face-contrast/static/images/cs/image_matrixs/' + path
        print(absPath)
        if os.path.exists(absPath):
            print("该文件已存在")
            continue
        else:
            np.savetxt(absPath, obj)
        print(num)
        num += 1
    pass






if __name__ == '__main__':
    start_time = datetime.datetime.now()
    dir_path = '/cs/face-contrast/static/images/cs/images'
    file_paths = []
    load_data.load_faces(dir_path,file_paths)
    print(len(file_paths))
    face_2_matrix()
    print((datetime.datetime.now()-start_time).seconds)
