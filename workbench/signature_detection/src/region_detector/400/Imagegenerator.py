"""
@author Tobias
"""
import os
from keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img

INPUT_WIDTH = 175
INPUT_HEIGTH = 75

def generate_augmented_images(path_to_images, number_of_images,
                              validation_data=False, safe_to_dir="preview"):
    print(safe_to_dir)
    image_generator = None
    if validation_data:
        image_generator = ImageDataGenerator(rescale=1./255,
                                             horizontal_flip=False)
    else:
        image_generator = ImageDataGenerator(width_shift_range=0.2,
                                             height_shift_range=0.2,
                                             rescale=1./255, #shear_range=0.2,
                                             zoom_range=0.3,
                                             horizontal_flip=False)

    dir = os.listdir(path_to_images)
    number = 3000/len(dir) + 10
    if validation_data:
        number = 300/len(dir) + 10
    for file in dir:
        path_to_image = "/".join((path_to_images, file))
        img = load_img(path_to_image)
        image_as_array = img_to_array(img)
        image_as_array = image_as_array.reshape((1,) + image_as_array.shape)
        for index, _ in enumerate(image_generator.flow(image_as_array,
                                                       batch_size=1,
                                                       save_to_dir=safe_to_dir,
                                                       save_prefix='signature',
                                                       save_format='jpg')):
            if index > number:
                break
