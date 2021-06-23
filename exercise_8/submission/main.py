from DNN import *
from keras.datasets import cifar10

show_pic = False #True will show 9 random images in the dataset every time it was altered.
epochs = 2
verbose = 1
noise_strength = 0.1
train_data = "CIFAR10"
dnn = Model1

imgs = ImgDataSet(cifar10, show=show_pic)
model_normal = dnn()
model_noisy = dnn()
model_pixel = dnn()
dnn().fit_and_eval(imgs.train_x, imgs.train_y, imgs.test_x, imgs.test_y, epochs=epochs, verbose=verbose, train_data="Normal " + train_data)

# More difference when noise is stronger
imgs.add_gaussian_noise(noise_strength, show=show_pic)
dnn().fit_and_eval(imgs.noisy_train_x, imgs.train_y, imgs.test_x, imgs.test_y, epochs=epochs, verbose=verbose, train_data=train_data + " with Gaussian noise")

# Not so much difference (May work well on test dataset, not train dataset)
imgs.pixel_attack(show=show_pic)
dnn().fit_and_eval(imgs.pixel_train_x, imgs.train_y, imgs.test_x, imgs.test_y, epochs=epochs, verbose=verbose, train_data=train_data + " with One pixel altered")