import random
import numpy as np
import tensorflow as tf
import keras.layers as layer
from matplotlib import pyplot as plt
from keras.datasets import cifar10
from keras.models import Model
from keras.utils import np_utils
from tensorflow import keras
from tensorflow.keras import optimizers

class ImgDataSet:

	def __init__(self, dataset=cifar10, show=False):
		(train_x, train_y), (test_x, test_y) = dataset.load_data()
		self.showed = []
		if show:
			
			for i,num in enumerate(random.choices(range(10000), k=9)):
				self.showed.append(num)
				plt.subplot(330 + 1 + i)
				plt.imshow(train_x[num])
			plt.show()

		# print(train_y[0]) >>> [6]
		self.train_y = np_utils.to_categorical(train_y)
		self.test_y = np_utils.to_categorical(test_y)
		# print(train_y[0]) >>> [0 0 0 0 0 0 1 0 0 0]

		self.train_x = train_x.astype("float32")
		self.train_x /= 255.
		self.test_x = test_x.astype("float32")
		self.test_x /= 255.
	
	def add_gaussian_noise(self, stddev=0.01, show=False):
		noisy_train_x = tf.keras.layers.GaussianNoise(stddev)(self.train_x, training=True)
		self.noisy_train_x = np.clip(noisy_train_x, 0, 1)
		if show and self.showed:
			for i,num in enumerate(self.showed):
				plt.subplot(330 + 1 + i)
				plt.imshow(self.noisy_train_x[num])
			plt.show()
		print(">>> Gaussian noise was applied to the dataset.")
	
	def pixel_attack(self, show=False):
		self.pixel_train_x = np.ndarray(self.train_x.shape)
		for i, picture in enumerate(self.train_x):
			attacked = picture.copy()
			attacked[random.randint(0,31)][random.randint(0,31)] = np.array([random.random(), random.random(), random.random()])
			self.pixel_train_x[i] = attacked
		if show and self.showed:
			for i,num in enumerate(self.showed):
				plt.subplot(330 + 1 + i)
				plt.imshow(self.pixel_train_x[num])
			plt.show()
		print(">>> One pixel per picture was altered in the dataset.")

class ModelBase:
	
	def fit_and_eval(self, train_x, train_y, test_x, test_y, batch_size=64, epochs=10, verbose=1, train_data:str='', **kwargs):
		history = self.model.fit(train_x, train_y, batch_size=batch_size, epochs=epochs, verbose=verbose, validation_data=(test_x,test_y), **kwargs)
		# Last validation is equal to evaluate on same test dataset, so there is no need.
		# score = self.model.evaluate(test_x, test_y, verbose=verbose)
		if verbose:
			acc_plot = plt.subplot(211)
			acc_plot.plot(history.history["acc"])
			acc_plot.plot(history.history["val_acc"])
			acc_plot.set_title(f"{self.__class__.__name__}: accuracy")
			acc_plot.set_ylabel("accuracy")
			acc_plot.set_xlabel("epoch")
			acc_plot.legend(["train", "validation"], loc="upper left")
			# "Loss"
			loss_plot = plt.subplot(212)
			loss_plot.plot(history.history["loss"])
			loss_plot.plot(history.history["val_loss"])
			loss_plot.set_title(f"{self.__class__.__name__}: loss")
			loss_plot.set_ylabel("loss")
			loss_plot.set_xlabel("epoch")
			loss_plot.legend(["train", "validation"], loc="upper left")
			figManager = plt.get_current_fig_manager()
			figManager.window.state("zoomed")
			plt.show()
		if train_data:
			print(f"\nResult of a model trained with {train_data}")
		print("    Train accuracy:{:10.8f}".format(history.history["acc"][-1]))
		print("    Train loss:{:>14.8f}".format(history.history["loss"][-1]))
		print("    Test accuracy{:>12.8f}".format(history.history["val_acc"][-1]))
		print("    Test loss:{:>15.8f}".format(history.history["val_loss"][-1]))

class ExampleModel(ModelBase):

	def __init__(self, opt=tf.keras.optimizers.Adam):
		input_layer= layer.Input(shape=(32,32,3))
		conv1= layer.Conv2D(32,(3,3),activation='relu')(input_layer)
		conv2 = layer.Conv2D(32,(3,3),activation="relu")(conv1)
		maxpool1 = layer.MaxPooling2D(pool_size=(2,2))(conv2)
		dropout1= layer.Dropout(0.25)(maxpool1)
		flat1= layer.Flatten()(dropout1)
		dense1 = layer.Dense(128,activation="relu")(flat1)
		drouput2= layer.Dropout(0.5)(dense1)
		output = layer.Dense(10,activation="softmax")(drouput2)

		self.model = Model(inputs=input_layer, outputs= output)
		#opt= tf.keras.optimizers.SGD(learning_rate=0.001)
		opt= tf.keras.optimizers.Adam(learning_rate=0.001)
		self.model.compile(loss="categorical_crossentropy", metrics=["acc"])

class Model1(ModelBase):
	
	def __init__(self, opt=tf.keras.optimizers.Adam):
		model = tf.keras.Sequential()
		model.add(layer.Conv2D(32, (3, 3), activation="relu", padding="same", input_shape=(32, 32, 3)))
		model.add(layer.Conv2D(32, (3, 3), activation="relu", padding="same"))
		model.add(layer.MaxPooling2D((2, 2)))
		model.add(layer.Dropout(0.25))
		model.add(layer.Flatten())
		model.add(layer.Dense(128, activation="relu"))
		model.add(layer.Dropout(0.5))
		model.add(layer.Dense(10, activation="softmax"))
		opt = opt(learning_rate=0.001)
		model.compile(loss="categorical_crossentropy", metrics=["acc"])
		self.model = model

class Model2(ModelBase):
	
	def __init__(self, opt=tf.keras.optimizers.Adam):
		model = tf.keras.Sequential()
		model.add(layer.Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=(32, 32, 3)))
		model.add(layer.Conv2D(32, (3, 3), activation='relu', padding='same'))
		model.add(layer.MaxPooling2D((2, 2)))
		model.add(layer.Dropout(0.2))
		model.add(layer.Conv2D(64, (3, 3), activation='relu', padding='same'))
		model.add(layer.Conv2D(64, (3, 3), activation='relu', padding='same'))
		model.add(layer.MaxPooling2D((2, 2)))
		model.add(layer.Dropout(0.2))
		model.add(layer.Conv2D(128, (3, 3), activation='relu', padding='same'))
		model.add(layer.Conv2D(128, (3, 3), activation='relu', padding='same'))
		model.add(layer.MaxPooling2D((2, 2)))
		model.add(layer.Dropout(0.2))
		model.add(layer.Flatten())
		model.add(layer.Dense(128, activation='relu'))
		model.add(layer.Dropout(0.2))
		model.add(layer.Dense(10, activation='softmax'))
		opt = opt(learning_rate=0.001)
		model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["acc"])
		self.model = model