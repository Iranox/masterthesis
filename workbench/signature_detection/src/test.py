import json
import math
from itertools import chain
import glob
import statistics
import os

files = [str(name.replace(".jpg", "")) for name in os.listdir("/home/iranox/Projects/lehrer-schueler-beziehung/workbench/signature_detection/src/200/Hauptmann")]

def distance(x, y):
    r = 0
    x_d = sum([x[l] for l  in x.keys() if l !=  "id" and l != "klasse"])
    y_d = sum([y[l] for l  in y.keys() if l !=  "id" and l != "klasse"])
    m = y_d + x_d
    for l in x.keys():
        if l !=  "id" and l != "klasse":
            r += x[l] * y[l]
    return (2*r)/m

with open("/home/iranox/Projects/lehrer-schueler-beziehung/workbench/signature_detection/src/200/json/data_6.json") as json_data:
    data = json.load(json_data)
data = [x for x in data if x["id"] in files]
files = [x["id"] for x in data if x["id"] in files]

for l in files:
    tmp = [x for x in data if l == x["id"] ]
    for i in range(0,14):
        #print(tmp)
        with open("data_{}.json".format(i)) as json_data:
            data2 = json.load(json_data)
            data2 = [x for x in data2 if x["id"] in files]
        r = list()
        data2 = [x for x in data2 if l == x["id"]]
        if data2 and tmp:
            print("======================")
            print(tmp[0]["id"])
            print(tmp[0])
            print(data2[0])
            print(distance(tmp[0], data2[0]))
            print(data2[0]["klasse"])
            print("Hautpmann & {} & {} // \hline")
