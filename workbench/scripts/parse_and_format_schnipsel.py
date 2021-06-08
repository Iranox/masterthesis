from rdflib import Graph, Literal, URIRef, Namespace
from rdflib.namespace import DC
import json

def get_lehrer_id(lehrer_name):
    tmp = {"Klengel":42,"Rochterkopf":54, "Barfuß":55, "Gabe":53, "Graubau": 52,
           "Böhme":51,"Becker":50, "Richter": 7, "Plaichi":31, "Albert":47,
           "Rochterkopf":54, "Mangel":36, "Hauptmann":39, "David":28 ,
           "Mochelly":57, "Mendelssohn":44}
    return tmp[lehrer_name]


def parse(path):
    sub_template = "http://hmt-leipzig.de/Schnipsel/{}"
    store = Graph()
    store_2 = Graph()
    store_3 = Graph()
    store.load(path, format="turtle")
    store_2.bind("hmd", Namespace("http://hmt-leipzig.de/Data/Model#"))
    store_3.bind("qb", Namespace("http://purl.org/linked-data/cube#"))
    store_3.bind("hmd", Namespace("http://hmt-leipzig.de/Data/Model#"))
    lehrer = {}
    sub_id = {}
    subjects_list = []
    for sub, pre, obj in store:
        if ("Wahrscheinlichkeitsvektor" in pre or "type" in pre
            or "gerateneKlasse" in pre or "TrainingsdatenAnzahl" in pre):
            if "gerateneKlasse" in pre:
                store_3.add((sub, pre,
                            URIRef("http://hmt-leipzig.de/Data/Person/Lehrer/{}".format(get_lehrer_id(str(obj))))))
                continue
            store_3.add((sub, pre, obj))
        elif "coordinates" in pre or ("id" in pre and "David" not in pre) or "Klasse" in pre:
            if "Klasse" in pre:
                l = str(sub).replace("http://hmt-leipzig.de/Experiment/200/", "")
                new_sub = sub_template.format(l)
                store_2.add((URIRef(new_sub), pre,
                            URIRef("http://hmt-leipzig.de/Data/Person/Lehrer/{}".format(get_lehrer_id(str(obj))))))
                continue
            if "id" in pre:
                zeugnis = obj.split("_")
                zeugnis_id, number, schnipsel_id = (None, None, None)
                if len(zeugnis) < 3:
                    zeugnis_id, schnipsel_id = zeugnis
                    number = 0
                else:
                    zeugnis_id,number, schnipsel_id = zeugnis

                l = str(sub).replace("http://hmt-leipzig.de/Experiment/200/", "")
                new_sub = sub_template.format(l)
                sub_id[new_sub] = obj
                zeugnis_uri = "http://hmt-leipzig.de/Data/Model/zeugnis/id/{}/number/{}".format(zeugnis_id, number)
                store_2.add((URIRef(new_sub), URIRef("http://hmt-leipzig.de/Data/Model#Zeugnis"), URIRef(zeugnis_uri)))
                store_2.add((URIRef(new_sub), URIRef("http://hmt-leipzig.de/Data/Model#SchnipselId"), Literal(schnipsel_id)))
                continue

            l = str(sub).replace("http://hmt-leipzig.de/Experiment/200/", "")
            new_sub = sub_template.format(l)
            subjects_list.append(new_sub)
            store_2.add((URIRef(new_sub), pre, obj))
            store_3.add((sub,URIRef("http://hmt-leipzig.de/Data/Model#Schnipsel"),
                        URIRef(new_sub)))
        elif "Schueler" in obj:
            continue
        else:
            lehrer_name = str(pre).replace("http://hmt-leipzig.de/Data/Model#","")
            if sub in lehrer:
                tmp = lehrer[sub]
                tmp[lehrer_name] = float(obj)
                lehrer[sub] = tmp
            else:
                lehrer[sub] = {lehrer_name: float(obj)}

    del store
    for sub in subjects_list:
        store_2.add((URIRef(sub), URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), URIRef("http://hmt-leipzig.de/Data/Model#Schnipsel")))
    for name in lehrer.keys():
        store_3.add((name, URIRef("http://hmt-leipzig.de/Data/Model#Wahrscheinlichkeitsvektor"),
        Literal(json.dumps(lehrer[name]))))
    #store_2.serialize("Schnipsel.ttl", format="turtle")
    #store_3.serialize("Beziehung.ttl", format="turtle")
    #del store_3
    new_beziehung_graph = Graph()
    new_sub_graph = Graph()
    new_sub_graph.bind("hmd", Namespace("http://hmt-leipzig.de/Data/Model#"))
    new_beziehung_graph.bind("hmd", Namespace("http://hmt-leipzig.de/Data/Model#"))

    for sub, pre, obj in store_2:
        if "SchnipselId" in pre:
            continue
        sub_template = "http://hmt-leipzig.de/Schnipsel/{}/Number/{}/ID/{}"
        tmp = sub_id[str(sub)]
        zeugnis = tmp.split("_")
        zeugnis_id, number, schnipsel_id = (None, None, None)
        if len(zeugnis) < 3:
            zeugnis_id, schnipsel_id = zeugnis
            number = 0
        else:
            zeugnis_id,number, schnipsel_id = zeugnis
        new_sub_graph.add((URIRef(sub_template.format(zeugnis_id, number, schnipsel_id)), pre, obj))
    new_sub_graph.serialize("Schnipsel.ttl", format="turtle")
    del new_sub_graph, store_2
    #store_3.serialize("Beziehung.ttl", format="turtle")

    for sub, pre, obj in store_3:
        if "Schnipsel" in pre:
            sub_template = "http://hmt-leipzig.de/Schnipsel/{}/Number/{}/ID/{}"
            tmp = sub_id[str(obj)]
            zeugnis = tmp.split("_")
            zeugnis_id, number, schnipsel_id = (None, None, None)
            if len(zeugnis) < 3:
                zeugnis_id, schnipsel_id = zeugnis
                number = 0
            else:
                zeugnis_id,number, schnipsel_id = zeugnis
            new_beziehung_graph.add((sub, pre, (URIRef(sub_template.format(zeugnis_id, number, schnipsel_id)))))
        else:
            new_beziehung_graph.add((sub, pre, obj))
    new_beziehung_graph.serialize("Beziehung.ttl", format="turtle")




if __name__ == '__main__':
    parse("/home/iranox/Projects/lehrer-schueler-beziehung/workbench/scripts/Beziehung_200.ttl")
