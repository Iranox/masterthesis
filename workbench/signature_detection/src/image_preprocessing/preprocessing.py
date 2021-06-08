import os
import math
import cv2
import numpy as np

def sliding_window(image, stepSize, windowSize):
    for y in range(0, image.shape[0], stepSize):
        for x in range(0, image.shape[1], stepSize):
            yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]])

def is_dummy_file(path_to_image):
    file_size_in_bytes = os.path.getsize(path_to_image)
    conversion_factor_byte_megabyte = math.pow(1024, 2)
    file_size_in_mb = round(file_size_in_bytes /
                            conversion_factor_byte_megabyte, 3)
    return file_size_in_mb < 1

def remove_all_dummy_files(path_to_folder=None):
    return [file for file in path_to_folder if is_dummy_file(file) is False]

class ImagePreprocessing():
    def __init__(self):
        self.image = None
        self.cropped_images = []
        self.kernel = np.ones((5, 5))
        self.path = None


    def _remove_white_rand(self):
        grey = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
        _, image_binary = cv2.threshold(grey, 0, 255,
                                        cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        ctr, _ = cv2.findContours(image_binary, cv2.RETR_EXTERNAL,
                                     cv2.CHAIN_APPROX_SIMPLE)
        del _
        largest_countour = max(ctr, key=cv2.contourArea)
        box = np.int0(cv2.boxPoints(cv2.minAreaRect(largest_countour)))
        x_max, y_max = np.max(box, axis=0)
        x_min, y_min = np.min(box, axis=0)
        self.image = self.image[y_min:y_max, x_min:x_max]

    def _extract_contours(self, contours, img, region):
         for i in contours:
            box = np.int0(cv2.boxPoints(cv2.minAreaRect(i)))
            x_max, y_max = np.max(box, axis=0)
            x_min, y_min = np.min(box, axis=0)
            if (x_max - x_min > 60 and y_max - y_min > 60) and (
            x_max - x_min < 250 and y_max - y_min < 250
            ):
                t = img[y_min:y_max, x_min:x_max]
                if t.size > 0:
                    tmp = {"image":img[y_min:y_max, x_min:x_max],
                           "region":region, "coordinates":[y_min, x_max,
                                                           y_max, x_max]}
                    self.cropped_images.append(tmp)


    def _split_in_regions(self):
        region_head = self.image[0:1200, :]
        region_class_1 = self.image[1200:1600, :]
        region_class_2 = self.image[1600:1900, :]
        region_class_3 = self.image[1900:2200, :]
        region_class_4 = self.image[2200:2600, :]
        region_class_5 = self.image[2600:3000, :]
        cv2.imwrite("regionen/" + self.path.replace(".jpg","").split("/")[-1] + "_R1.jpg", region_class_1)
        cv2.imwrite("regionen/" + self.path.replace(".jpg","").split("/")[-1] + "_R2.jpg", region_class_2)
        cv2.imwrite("regionen/" + self.path.replace(".jpg","").split("/")[-1] + "_R3.jpg", region_class_3)
        cv2.imwrite("regionen/" + self.path.replace(".jpg","").split("/")[-1] + "_R4.jpg", region_class_4)
        cv2.imwrite("regionen/" + self.path.replace(".jpg","").split("/")[-1] + "_R5.jpg", region_class_5)

        region_class_1 = self.image[1200:1600, 1500:2000]
        region_class_2 = self.image[1600:1900, 1500:2000]
        region_class_3 = self.image[1900:2200, 1500:2000]
        region_class_4 = self.image[2200:2600, 1500:2000]
        region_class_5 = self.image[2600:3000, 1500:2000]
        return (region_head, region_class_1, region_class_2, region_class_3,
                region_class_4, region_class_5)


    def extract_text(self, path):
        self.image = cv2.imread(path)
        self.path = path

        if self.image is None:
            raise OSError('Image is None. Path is wrong or Image is empty')
        self._remove_white_rand()
        image_regions = list(self._split_in_regions())
        self.image = None

        del image_regions[0]
        for index, img in enumerate(image_regions):
            try:
                grey = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            except:
                print(path)
                return None
            _, image_binary = cv2.threshold(grey, 0, 255, cv2.THRESH_BINARY_INV |
                                            cv2.THRESH_OTSU)
            image_binary = cv2.dilate(image_binary, self.kernel, iterations=3)
            contours, _ = cv2.findContours(image_binary, cv2.RETR_TREE,
                                              cv2.CHAIN_APPROX_SIMPLE)
            del _
            self._extract_contours(contours, img, index)
        return self.cropped_images


    def extract_text_and_save_as_image(self, path):
        for index, image in enumerate(self.extract_text(path)):
            cv2.imwrite("canny/test_canny_{}.jpg".format(index), image["image"])

if __name__ == '__main__':
    TEST = ImagePreprocessing()
    TEST.extract_text_and_save_as_image('/home/iranox/Projects/Z/00000025.jpg')
