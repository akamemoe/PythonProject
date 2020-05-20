
# coding: utf-8

# In[13]:


import tensorflow as tf
from matplotlib import pyplot as plt
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Dropout,Activation,Flatten,Conv2D,MaxPooling2D
import cv2
import os
import numpy as np
import random
import pickle
import time


# 加载所有图片数据，每个图片都resize成IMG_SIZE大小。整体打乱并将数据集写入文件，方便下次直接读取数据集而不是遍历文件夹一个一个的读取图片。

# In[14]:

IMG_SIZE = 40
DATA_SET_NAME = 'data_set.pickle'

def prepare_data(storage=True):
    impath = ['datasets/English/Img/Sample%03d' % (x+1) for x in range(10)]
    data_set = []
    for p in impath:
        label = impath.index(p)
        for pp in os.listdir(p):
            try:
                im = cv2.imread(os.path.join(p,pp),cv2.IMREAD_GRAYSCALE)
                new_im = cv2.resize(im,(IMG_SIZE,IMG_SIZE))
                data_set.append([new_im,label])
            except Exception as e:
                pass
    random.shuffle(data_set)
    if storage:
        with open(DATA_SET_NAME,'wb') as f:
            pickle.dump(data_set,f)
    return data_set

# 将直接从文件中把数据集恢复。

def load_train_data():
    images = []
    labels = []
    with open(DATA_SET_NAME,'rb') as f:
        pickle_data = pickle.load(f)
    for x in pickle_data:
        images.append(x[0])
        labels.append(x[1])
    return images,labels

# 定义模型
def define_model():
    model = Sequential()
    #第一卷积层
    model.add(Conv2D(128,(3,3),input_shape=(IMG_SIZE,IMG_SIZE,1)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    #第二卷积层
    model.add(Conv2D(64,(3,3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))

    #平化层
    model.add(Flatten())
    model.add(Dense(64))

    #model.add(Dropout(0.2))

    model.add(Dense(10))
    model.add(Activation('softmax'))

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model

def predict(image_path,model,labels):
    im = cv2.imread(image_path,cv2.IMREAD_GRAYSCALE)
    data = cv2.resize(im,(IMG_SIZE,IMG_SIZE)) / 255.0
    pred = model.predict([data])
    print(labels[int(np.argmax(pred[0]))])


def main():
    X_train,Y_train = load_train_data()
    #print(Y_train[:10])
    #因为读取出来的数据是列表。所以需要用numpy把其reshape成numpy的数组
    #X_train = np.reshape(X_train,(-1,IMG_SIZE,IMG_SIZE))
    X_train = np.reshape(X_train,(-1,IMG_SIZE,IMG_SIZE,1))
    Y_train = np.reshape(Y_train,(-1,))

    # 将0-255的数据缩放到0-1之间
    X_train = X_train / 255.0
    #配置tensorboard
    filename = 'mymodel-{}.ckpt'.format(int(time.time()))
    tensorboard = TensorBoard(log_dir='logs/{}'.format(filename))
    model = define_model()
    #validation_split：测试数据和训练数据的分离比例。因为这两个其实是一样的数据，之前版本需要手动传入测试集，
    #现在只需要定义一下比例，tensorflow自动会按比例随机选取测试样本
    model.fit(X_train,Y_train,batch_size=10,validation_split=0.2,epochs=10,callbacks=[tensorboard])

    model.save('CNN-128-64-64-with-98-acc.model')
    #tf.kares.models.load_model('CNN-128-64-64-with-98-acc.model')

if __name__ == '__main__':
    main()