import glob
import os
import sys
import datetime
import cv2
import numpy as np
from PyQt5 import QtGui
from PyQt5.QtWidgets import QDialog, QApplication
from image_preprocessing.preprocessing import ImagePreprocessing, remove_all_dummy_files
from region_detector.cnn import CNNBuilder
from region_detector.SignatureDetector import SignatureDetector, INPUT_WIDTH, INPUT_HEIGTH
from log.RDFLogger import RDFLogger
from gui.Test import Ui_Dialog
from utilis.utilis import get_lehrer_name_and_id
import csv
import collections
from rdflib import Graph, Literal, URIRef, Namespace
from rdflib.namespace import DC


def save_result(number_of_classes, result, store, id):
    #l = sorted(os.listdir("/home/iranox/1000/200-1000"))

    store.bind("hmd", Namespace("http://hmt-leipzig.de/Data/Model#"))
    store.bind("rdf", Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#"))
    store.bind("qb", Namespace("http://www.w3.org/2002/07/owl#"))
    schuler_uri = "http://hmt-leipzig.de/Experiment/400/{}"
#    l = {"Vitae": 16, "B\u00f6hme": 2, "Papperitz": 11, "Mangel": 8, "Gabe": 4,
#"David": 3, "Graubau": 5, "Becker": 1, "Paul": 12, "Rochterkopf": 15,
#"Albert": 0, "Richter": 14, "Plaichi": 13, "Klengel": 7, "Hauptmann": 6, "Mochelly": 10, "Mendelssohn": 9}

#    for l_i in l:
#        re = sorted(os.listdir("/home/iranox/1000/200-1000/"+l_i))
#        re = [x.split("/")[-1].replace(".jpg","") for x in re]
    for x in result:
#            if x["id"] not in re:
#                continue
            id += 1
            store.add((URIRef(schuler_uri.format(id)),
                       URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),
                       URIRef("http://www.w3.org/2002/07/owl#Observation")))
            store.add((URIRef(schuler_uri.format(id)),
                       URIRef("http://hmt-leipzig.de/Data/Model#TrainingsdatenAnzahl"),
                       Literal(200)))
            #store.add((URIRef(schuler_uri.format(id)),
            #           URIRef("http://hmt-leipzig.de/Data/Model#Klasse"),
            #           Literal(l_i)))
            for lehrer in x:
                if lehrer is "klasse":
                    klasse = x[lehrer].replace("[", "").replace("]","")
                    klasse = get_name(int(klasse))
                    store.add((URIRef(schuler_uri.format(id)),
                               URIRef("http://hmt-leipzig.de/Data/Model#gerateneKlasse"),
                               Literal(klasse)))
                    continue
                if lehrer is "id":
                    schuler = int(x["id"].split("_")[0])
                    store.add((URIRef(schuler_uri.format(id)),
                               URIRef("http://hmt-leipzig.de/Data/Model#Student"),
                               URIRef("http://hmt-leipzig.de/Data/Person/Schueler/{}".format(schuler)) ))
                store.add((URIRef(schuler_uri.format(id)),
                           URIRef("http://hmt-leipzig.de/Data/Model#"+lehrer),
                           Literal(x[lehrer]) ))
    return id


def get_name(index):
    l = {"Vitae": 16, "B\u00f6hme": 2, "Papperitz": 11, "Mangel": 8, "Gabe": 4,
"David": 3, "Graubau": 5, "Becker": 1, "Paul": 12, "Rochterkopf": 15,
"Albert": 0, "Richter": 14, "Plaichi": 13, "Klengel": 7, "Hauptmann": 6, "Mochelly": 10, "Mendelssohn": 9}
    for name in l:
        if index is l[name]:
            return name

def klassifizieren(dicti):
    files = glob.glob(dicti)
    files =remove_all_dummy_files(files)
    files = sorted(files)

    cnn_dec = SignatureDetector()
    predict = 1
    cnn_dec.load_model()
    w = list()
    print(dicti)
    for index, path in enumerate(files):
        image_preprocessing = ImagePreprocessing()
        image = image_preprocessing.extract_text(path)
       # image = [x for x in image
        #         if cnn.predict(rescale_image(x["image"])) > 0.3]
        if image:
            for index, x in enumerate(image):
                height, width, channels = x["image"].shape
                if height < 60 and width < 60:
                    continue
                predict, predicted_class = cnn_dec.predict(x["image"])
                if not os.path.exists("metadata/{}/".format(predicted_class)):
                    os.makedirs("metadata/{}/".format(predicted_class))
                v = collections.OrderedDict({"id": "{}_{}".format(path.split("/")[-1].replace(".jpg", ""), str(index)),
                     "klasse": predicted_class})
                i = { get_name(index): float(x) for index, x in enumerate(predict)}
                v.update(i)
                i = {"coordinates": x["coordinates"], "region":x["region"]}
                v.update(i)
                w.append(v)
                #cv2.imwrite("metadata/{}/{}_{}.jpg".format(predicted_class, path.split("/")[-1].replace(".jpg",""),
                #                                     str(index)),cv2.cvtColor(x["image"], cv2.COLOR_BGR2GRAY))
            del image
        else:
            with open("anomalie.txt", "a") as f:
                f.write(path)
                f.write("\n")
            os.remove(path)
    #print(w)
    return len(predict), w



def build_cnn():
    cnn = CNNBuilder()
    cnn.add_conv2d(number_of_neurons=16, kernel=(3, 3), input=(20, 50, 3))
    cnn.add_conv2d(number_of_neurons=32, kernel=(3, 3))
    cnn.add_Faltten_Layer(dense_size=32, output_size=1)
    cnn.compile_model().load_trained_model('models/region_detection_4.h5')
    return cnn



def rescale_image(image):
    image = cv2.resize(image, (50, 20))
    image = np.expand_dims(np.true_divide(image, 255), axis=0)
    return image


class MainGui(QDialog):
    def __init__(self):
        super().__init__()
        self.index = 0
        self.gui_interface = Ui_Dialog()
        self.gui_interface.setupUi(self)
        self.logg = RDFLogger()
        self.predicted_class = None

        self.gui_interface.ButtonClickMe.clicked.connect(self.dispmessage)
        self.all_files = glob.glob("/home/iranox/Projects/lehrer-schueler-beziehung/Daten/Ressources/Zeugnisse/00000800/*.jpg")
        self.all_files = remove_all_dummy_files(self.all_files)
        self.path = self.all_files.pop()
        print(self.path)
        with open('remove_images.sh', 'a') as file:
            file.write("rm {} \n".format(self.path))
        print(len(self.all_files))
        self.cnn_dec = SignatureDetector()
        self.cnn_dec.load_model()
        self.regions = []
        image_preprocessing = ImagePreprocessing()
        self.image = image_preprocessing.extract_text(self.path)
        cnn = build_cnn()
        print(len(self.image))
        self.image = [x for x in self.image
                     if cnn.predict(rescale_image(x["image"])) > 0.3]
        print(len(self.image))
        self._set_lehrer()
        self.gui_interface.choosenFile.setText("File: {}".format(self.path))
        self._load_image()
        self.show()

    def _remove_empty_region(self):
        count=collections.Counter([d['region'] for d in self.image])
        t = []
        for i in (0,1,2,3,4):
            if count[i] < 6:
                t.append(i)
                self.logg.add_relationship({"file":self.path, "region":i,
                                            "empty":True})
        self.regions = t
        return [i for i in self.image if i["region"] not in t]



    def _split_big_images(self):
        big_images = [x for x in self.image
                      if x["image"].shape[1] > 200]
        self.image = [x for x in self.image
                      if x["image"].shape[1] < 201]

        for i in big_images:
            for smaller_images in sliding_window(i["image"], 100, (250, 150)):
                if smaller_images.shape[1] > 50:
                    tmp = {"image":smaller_images,
                           "coordinates":i["coordinates"],
                           "region":i["region"]}
                    self.image.append(tmp)
            del smaller_images
        del i, big_images
        cnn = build_cnn()
        self.image = [x for x in self.image
                     if cnn.predict(rescale_image(x["image"])) > 0.3]
        del cnn


    def _set_lehrer(self):
        image = self.image[self.index]["image"]
        self.predict, self.predicted_class = self.cnn_dec.predict(image)
        lehrer_name = get_lehrer_name_and_id(self.predicted_class[0])["name"]
        predicted_lehrer = "Lehrer:{}".format(lehrer_name)
        self.gui_interface.Label_Vorhersage.setText(predicted_lehrer)


    def _load_image(self):
        frame = self.image[self.index]["image"]
        frame = cv2.resize(frame, (150, 150))
        height, width = frame.shape[:2]
        self.gui_interface.Image_Label.setScaledContents(True)
        self.gui_interface.Image_Label.setFixedSize(height, width)
        img = QtGui.QImage(frame, width, height, 3 * width,
                           QtGui.QImage.Format_RGB888)
        img = QtGui.QPixmap(img)
        self.gui_interface.Image_Label.setPixmap(img)

    def _check_if_reagion_is_empty(self):
        region = list(set(self.regions))

        for i in range(0,5):
            if i not in region:
                self.logg.add_relationship({"file":self.path.split("/")[-1],
                                            "region":i,
                                            "empty":True})
        self.regions = []

    def _next_item(self, log):
        if self.index < len(self.image) - 1:
            self.index += 1
            if log:
                self.logg.add(log)
            self._load_image()
            self._set_lehrer()
        elif self.index == len(self.image) - 1:
            if self.all_files:
                self.index = 0
                with open('remove_images.sh', 'a') as file:
                    file.write("rm {} \n".format(self.path))
                print(self.path)
                self.path = self.all_files.pop()
                image_preprocessing = ImagePreprocessing()
                self.image = image_preprocessing.extract_text(self.path)
                cnn = build_cnn()
                self.image = [x for x in self.image
                             if cnn.predict(rescale_image(x["image"])) > 0.05]
                if self.image :
                    pass
                else:
                    self._set_lehrer()
                self.gui_interface.choosenFile.setText("File: {}".format(self.path))
                self.logg.save_result()
                print(len(self.all_files))

            else:
                self.logg.save_result()
                sys.exit()

    def dispmessage(self):
        now = datetime.datetime.now()
        k = {"unterschrift":self.image[self.index]["coordinates"],
             "vermutung":get_lehrer_name_and_id(self.predicted_class[0])["id"],
             "region":self.image[self.index]["region"],
             "file":self.path.split("/").pop(), "date": now.strftime("%Y-%m-%d"),
             "predict":self.predict}
        if self.gui_interface.Image_True.isChecked() is True:
            class_p = str(self.predicted_class)
            datei_name = self.path.split("/").pop()
            cv2.imwrite("Ergebnisse/{}/{}_{}.jpg".format(class_p, datei_name,
                                                         str(self.index)),
                        self.image[self.index]["image"])
            k["korrekt"] = True
            k["empty"] = False
            self.logg.add_relationship(k)
            self.regions.append(k["region"])
            self._next_item(k)
        elif self.gui_interface.Image_Falsche.isChecked():
            k["korrekt"] = False
            cv2.imwrite("Ergebnisse/False/{}_{}.jpg".format(self.path.split("/").pop(),
                                                            str(self.index)),
                        self.image[self.index]["image"])
            self._next_item(k)
        elif self.gui_interface.Image_Noise.isChecked():
            self._next_item(None)


if __name__ == '__main__':
    l = sorted(os.listdir("/home/iranox/Projects/lehrer-schueler-beziehung/Daten/Ressources/metadata/"))
    result = list()
    for i in l:
        file = "/home/iranox/Projects/lehrer-schueler-beziehung/Daten/Ressources/metadata/{}/*.jpg".format(i)
        result.append(klassifizieren(file))
    print(len(result))
    id = 0
    store = Graph()
    for number_of_classes, i in result:
        id = save_result(number_of_classes, i, store, id)
        result = list
    store.serialize("test.ttl", format="turtle")
