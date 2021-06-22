
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
x_train = np.expand_dims(x_train, -1)
x_test = np.expand_dims(x_test, -1)
#x_train = x_train[:,:,:,np.newaxis]
#x_test = x_test[:,:,:,np.newaxis]


x_train= x_train.astype('float32')
x_test= x_test.astype('float32')
x_train/= 255
x_test/= 255


#print(y_train.shape)
#print(y_train[0])

y_train=np_utils.to_categorical(y_train,10) 
y_test=np_utils.to_categorical(y_test,10) 

#print(y_train.shape)
#print(y_train[0])

#quit()

#print(y_train.shape)
#print(y_train[:10])


############ Creating the model ###################

input_layer= Input(shape=(28,28,1))
conv1= Conv2D(32,(3,3),activation='relu')(input_layer)
conv2 = Conv2D(32,(3,3),activation="relu")(conv1)
maxpool1 = MaxPooling2D(pool_size=(2,2))(conv2)
dropout1= Dropout(0.25)(maxpool1)
flat1= Flatten()(dropout1)

dense1 = Dense(128,activation="relu")(flat1)
drouput2= Dropout(0.5)(dense1)
output = Dense(10,activation="softmax")(drouput2)

model = Model(inputs=input_layer, outputs= output)
#opt= tf.keras.optimizers.SGD(learning_rate=0.001)
opt= tf.keras.optimizers.Adam(learning_rate=0.001)
model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])

print(model.summary())
print(model.output_shape)

model.fit(x_train, y_train, batch_size=32, epochs=1, verbose=1)

# Score trained model.
scores = model.evaluate(x_test, y_test, verbose=1)
print('Test loss:', scores[0])
print('Test accuracy:', scores[1])


####################################################


save_dir = os.path.join(os.getcwd(), 'saved_models')
# Save model and weights
if not os.path.isdir(save_dir):
    os.makedirs(save_dir)
model_path = os.path.join(save_dir, model_name)
model.save(model_path)
print('Saved trained model at %s ' % model_path)

