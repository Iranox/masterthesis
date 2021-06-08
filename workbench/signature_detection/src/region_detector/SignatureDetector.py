"""
@author Tobias
"""
import cv2
import numpy as np
import csv
import json
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Activation, Dropout, Flatten, Dense
from keras.preprocessing.image import ImageDataGenerator
from keras.regularizers import l2


INPUT_WIDTH = 75
INPUT_HEIGTH = 25


class SignatureDetector(object):
    """docstring for SignatureDetector."""
    def __init__(self):
        super(SignatureDetector, self).__init__()
        self.model = None

    def _create_model(self):
        self.model = Sequential()
        self.model.add(Conv2D(32, (3, 3),kernel_initializer='he_normal',
                     input_shape=(INPUT_WIDTH, INPUT_HEIGTH, 3)))
        self.model.add(Activation("relu"))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Conv2D(64, (3, 3), kernel_initializer='he_normal'))
        self.model.add(Activation("relu"))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Flatten())
        self.model.add(Dense(256, kernel_regularizer=l2(0.01),
                             bias_regularizer=l2(0.01)))
        self.model.add(Activation('relu'))
        self.model.add(Dense(512, kernel_regularizer=l2(0.01),
                             bias_regularizer=l2(0.01)))
        self.model.add(Activation('relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(17, activation='softmax'))
        self.model.compile(loss='categorical_crossentropy', optimizer="adam", metrics=['accuracy'])


    def train_model(self):
        if self.model is None:
            self._create_model()
        batch_size = 128
        train_datagen = ImageDataGenerator(rescale=1./255)
        test_datagen = ImageDataGenerator(rescale=1./255)


        train_generator = train_datagen.flow_from_directory('preview/train',
                                                            target_size=(INPUT_WIDTH,
                                                                         INPUT_HEIGTH),
                                                            batch_size=batch_size,
                                                            class_mode='categorical')
        label_map = (train_generator.class_indices)
        with open('output_mapping.txt', 'w') as file:
            file.write(json.dumps(label_map))


        validation_generator = test_datagen.flow_from_directory('preview/validation',
                                                                target_size=(INPUT_WIDTH,
                                                                INPUT_HEIGTH),
                                                                batch_size=batch_size,
                                                                class_mode='categorical')

        history = self.model.fit_generator(train_generator, steps_per_epoch=40500 // batch_size,
                                 epochs=60, validation_data=validation_generator,
                                 validation_steps=15000 // batch_size)
        plt.plot(history.history['acc'])
        plt.plot(history.history['val_acc'])
        plt.title('Model accuracy')
        plt.ylabel('Accuracy')
        plt.xlabel('Epoch')
        plt.legend(['Train', 'Test'], loc='upper left')
        plt.savefig('model_accuracy.png')
        # Plot training & validation loss values
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('Model loss')
        plt.ylabel('Loss')
        plt.xlabel('Epoch')
        plt.legend(['Train', 'Test'], loc='upper left')
        plt.savefig('model_loss.png')
        self.model.save_weights("models/l2_regularizer.h5",
                                overwrite=True)


    def load_model(self):
        if self.model is None:
            self._create_model()
        self.model.load_weights("models/800/l2_regularizer_daten_0-800_test.h5")


    def predict(self, cv2_image):
        image = cv2.resize(cv2_image, (INPUT_HEIGTH, INPUT_WIDTH))
        image = np.expand_dims(np.true_divide(image, 255), axis=0)
        predict = self.model.predict(image)
        classes = np.where(predict[0] == max(predict[0]))[0]
        return (predict[0], str(classes))

    def vis(self):
        self.load_model()
        from keras.utils import plot_model
        plot_model(self.model, show_layer_names=False, to_file='model_0-400.png')


if __name__ == '__main__':
    MODEL = SignatureDetector()
    MODEL.train_model()
