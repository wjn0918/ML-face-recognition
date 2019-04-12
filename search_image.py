from flask import Flask, render_template, Response, request
from db import *



def getImageFromMysql(name):
    sql = "select photo_r from face_recognition where name = %s "
    args = (name,)
    r = executeSql(sql,args)
    # print(r[0][0])
    # fout = open('image.png', 'wb')  #将图片保存到本地
    # fout.write(r[0][0])
    if not r:
        return "没有该人"
    else:
        return r[0][0]
    pass

def getImage(name):
    img = getImageFromMysql(name)
    return img

    pass


def search():
    if request.method == 'POST':
        name = request.form.get('name')

        img = getImage(name)
        if isinstance(img, bytes):
            return Response(img, mimetype="image/jpeg")
        else:
            return img
    return render_template('search.html')



