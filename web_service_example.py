"""
实现上传图片，与库中图片进行比对
"""
import os
import cv2
import face_recognition
from flask import Flask,jsonify, request, redirect, render_template
from werkzeug.utils import secure_filename
import numpy as np
import sys

#sys.path.append('../')
from tools import load_data

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/cs')
def hello():
    return "hello"

@app.route('/upload', methods=['POST', 'GET'])  # 添加路由
def upload():
    if request.method == 'POST':
        f = request.files['file']
 
        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"})

        r = [{"path":"images/lfw/Manuel_Gehring/Manuel_Gehring_0001.jpg","score":1}]
        return render_template('index.html',images=r)
 
    return render_template('upload.html')




@app.route('/',methods=['GET','POST'])
def upload_image():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            #basepath = '../'
            #upload_path = os.path.join(basepath, 'static/images', secure_filename(file.filename))
            #file.save(upload_path)
            # 使用Opencv转换一下图片格式和名称
            #img = cv2.imread(upload_path)
            #cv2.imwrite(os.path.join(basepath, 'static/images', 'test.jpg'), img)
            #return detect_faces_in_image(file)
            r = detect_faces_in_image(file)
            print(r)
            return render_template('index.html',images=r)

    return render_template('upload.html')

def init_data():
    """
    将文件路径，文件内容加载到对应列表中
    """
    known_face_encodings = []
    dir_path = '/cs/face-contrast/static/images/cs/image_matrixs'
    known_face_encodings_index = []
    file_paths = []
    for data in load_data.load_faces(dir_path, file_paths):
        #图片存储在各自的文件夹中
        data_name = data.split('/')[-1].split('.')[0]
        dir_name = '_'.join(data_name.split('_')[0:-1])
        data_path = 'images/cs/images/'+ dir_name + "/" + data_name + '.jpg'
        known_face_encodings_index.append(data_path)
        known_face_encodings.append(np.loadtxt(data))
    return known_face_encodings_index,known_face_encodings



def detect_faces_in_image(file_stream):
    # Load the uploaded image file
    img = face_recognition.load_image_file(file_stream)
    # Get face encodings for any faces in the uploaded image
    unknown_face_encodings = face_recognition.face_encodings(img)
    if len(unknown_face_encodings) > 0:
        face_fount  = True
        face_distances = face_recognition.face_distance(known_face_encodings, unknown_face_encodings[0])
        index = 0
        results = []
        for face_distance in face_distances:
            if face_distance < similar_size:
                results.append({"score":face_distance,"path":known_face_encodings_index[index]})
                index += 1
            else:
                index += 1
                continue
        sorted_results = sorted(results, key=lambda k: k["score"])
        #print(sorted_results) 
        #return (jsonify(sorted_results))
        if len(sorted_results) > 5:
            return sorted_results[0:5]
        else:
            return sorted_results
    else:
        return "图片中未识别到人脸"
if __name__ == '__main__':
    similar_size = 0.48
    known_face_encodings_index, known_face_encodings = init_data()
    app.run(host='0.0.0.0',port=5001,debug=True)




