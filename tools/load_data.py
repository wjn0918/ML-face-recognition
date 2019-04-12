import os
"""
将"dir_path"目录下的文件绝对路径加载到file_paths数组中

"""

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'out'}
def allowed_file(filename):
    """
    允许的文件格式
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



def load_faces(dir_path,file_paths):
    """
    加载图片库
    :param dir_path:图片存储目录路径
    :return: 所有图片组成的数组
    """
    if os.path.isdir(dir_path):
        for file in os.listdir(dir_path):
            file_abspath = dir_path + '/' + file
            # print(file_abspath)
            if os.path.isdir(file_abspath):
                #print(file_abspath)
                load_faces(file_abspath, file_paths)
            else:
                if allowed_file(file_abspath):
                    file_paths.append(file_abspath)
    else:
        if allowed_file(dir_path):
            file_paths.append(filePath)
    return file_paths

#dir_path = '/root/cs/face_recognize/photoes'
#file_paths = []
#load_faces(dir_path, file_paths)
#print(len(file_paths))
