import pickle

import numpy as np

from tools.db import conn_mongodb

a = np.arange(10)
a = a.reshape((2,5))
print(type(a))
db = conn_mongodb()
my_set = db.id_face
for i in my_set.find():
    a = pickle.loads(i['image'])
    print(a)
