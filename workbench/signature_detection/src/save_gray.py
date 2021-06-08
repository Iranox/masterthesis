import cv2
import os
import glob

def save_as_binary(image):
    grey = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    _, image_binary = cv2.threshold(grey, 0, 255,
                                    cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    del _, grey
    return image_binary

path_prefix = "/home/iranox/Projects/lehrer-schueler-beziehung/workbench/signature_detection/src/metadata/manuel_validierte"
l = sorted(os.listdir(path_prefix))
result = list()
for i in l:
    file = path_prefix + "/{}/*.jpg".format(i)
    if not os.path.exists("metadata/binary/{}/".format(i)):
        os.makedirs("metadata/binary/{}/".format(i))
    files = glob.glob(file)
    for x in files:
        cv2.imwrite("metadata/binary/{}/{}".format(i, x.split("/")[-1]),
                   save_as_binary(cv2.imread(x)))
