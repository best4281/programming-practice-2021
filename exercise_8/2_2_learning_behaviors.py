
from keras.models import Model
from keras.layers import *
from keras.datasets import mnist
from matplotlib import pyplot as plt
import numpy as np
from keras.utils import np_utils
import tensorflow as tf
import os

model_name = 'test_yes_trained.h5'

(x_train, y_train), (x_test, y_test)= mnist.load_data()

print(x_train.shape)
print(x_train[0].shape)
#plt.imshow(x_train[0])
#plt.show()


#tensorflow (batch, height, width, channels)
#theano (batch, channels, height, width)
#x_train= x_train.reshape(x_train.shape[0],28,28,1)
#x_test= x_test.reshape(x_test.shape[0],28,28,1)
#x_train = np.expand_dims(x_train, -1)
#x_test = np.expand_dims(x_test, -1)
x_train = x_train[:,:,:,np.newaxis]
x_test = x_test[:,:,:,np.newaxis]


print(x_train[0].shape)

x_train= x_train.astype('float32')
x_test= x_test.astype('float32')
x_train/= 255
x_test/= 255

y_train=np_utils.to_categorical(y_train,10) 
y_test=np_utils.to_categorical(y_test,10) 


#print(y_train.shape)
#print(y_train[:10])


############ Loading the model ###################

save_dir = os.path.join(os.getcwd(), 'saved_models')
model_path = os.path.join(save_dir, model_name)
model = tf.keras.models.load_model(model_path)

print("Model loaded...")

# Score trained model.
scores = model.evaluate(x_test, y_test, verbose=1)
print('Test loss:', scores[0])
print('Test accuracy:', scores[1])



