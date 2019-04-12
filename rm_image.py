"""删除图片"""


from flask import Flask, render_template, Response, request
from flask.json import jsonify

from com.beiming.人脸识别.db import conn_mysql, executeSql


def rmImageFromMysql(name):
    sql = "delete from t_face_recognition where name = %s "
    args = (name,)
    r = executeSql(sql,args)
    print(r)
    print(type(r))
    if not r:
        return jsonify({"success": 0, "msg": "删除成功"})
    else:
        return r[0][0]
    pass

def rmImage(name):
    img = rmImageFromMysql(name)
    return img

    pass


def rm():
    if request.method == 'POST':
        name = request.form.get('name')
        return rmImage(name)
    return render_template('rm.html')


if __name__ == '__main__':
    rmImage("张三")

