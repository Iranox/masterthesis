from keras.models import Sequential, load_model
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.preprocessing.image import ImageDataGenerator
from keras.applications import imagenet_utils


class CNNBuilder(object):
    """docstring for CNNBuilder."""
    def __init__(self):
        super(CNNBuilder, self).__init__()
        self.model = Sequential()

    def add_conv2d(self,kernel,number_of_neurons,input=None, maxpool=True):
        if input is not None:
            self.model.add(Conv2D(number_of_neurons, kernel, input_shape=input))
        else :
            self.model.add(Conv2D(number_of_neurons, kernel))
        self.model.add(Activation('relu'))
        if maxpool is True:
            self.model.add(MaxPooling2D(pool_size=(2, 2)))
        return self

    def add_Faltten_Layer(self, dense_size, output_size, dropout=0.5):
        self.model.add(Flatten())
        self.model.add(Dense(dense_size))
        self.model.add(Activation('relu'))
        self.model.add(Dropout(dropout))
        self.model.add(Dense(output_size))
        self.model.add(Activation('sigmoid'))
        return self

    def compile_model(self):
        self.model.compile(loss='binary_crossentropy',
                      optimizer='rmsprop',
                      metrics=['accuracy'])
        return self

    def train_model(self, model_name, path_to_data='data/'):
        batch_size = 16

        train_datagen = ImageDataGenerator(rescale=1./255)

        test_datagen = ImageDataGenerator(rescale=1./255)

        train_generator = train_datagen.flow_from_directory(
                path_to_data + 'train',
                target_size=(20, 50),
                batch_size=batch_size,
                class_mode='binary')


        validation_generator = test_datagen.flow_from_directory(
                path_to_data + 'validation',
                target_size=(20, 50),
                batch_size=batch_size,
                class_mode='binary')

        self.model.fit_generator(
                train_generator,
                steps_per_epoch=830 // batch_size,
                epochs=5,
                validation_data=validation_generator,
                validation_steps=80 // batch_size)
        self.model.save_weights(model_name, overwrite=True)

    def predict(self, image):
        preds = self.model.predict(image)
        return preds

    def load_trained_model(self, path_to_model):
        self.model.load_weights(path_to_model)

if __name__ == '__main__':
    cnn = CNNBuilder()
    cnn.add_conv2d(number_of_neurons=16, kernel=(3, 3),
                   input=(20, 50, 3)).add_conv2d(number_of_neurons=32,
                   kernel=(3, 3)).add_Faltten_Layer(dense_size=32,
                   output_size=1).compile_model().train_model("region_detection_4.h5")
