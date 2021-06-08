"""
@author Tobias
"""
import csv

def format_number(number):
    """
    @parameter number
    Funktioniert nur, wenn Dateien das Schema 00000001 hat.
    """
    test = ''
    for _ in range(0, len("00000001")-len(str(number))):
        test = test +  "0"
    test = test + str(number)
    return test

def write_metadata_to_file(rdf_metadata):
    """
    @parameter rdf_metadata
    """
    metadata_file = open("Studenten.ttl", "w")
    for triple in rdf_metadata:
        metadata_file.write(triple)
    metadata_file.close()

def get_prefix():
    """
    @return String with all prefixes
    """
    return ("@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> ."
            + "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n"
            + "@prefix owl: <http://www.w3.org/2002/07/owl#> .\n"
            + "@prefix foaf: <http://xmlns.com/foaf/0.1/> .\n"
            + "@prefix org: <http://www.w3.org/ns/org#> .\n"
            + "@prefix hd: <http://hmt-leipzig.de/Data/Model#> .\n"
            + "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n"
            + "@prefix cc: <http://creativecommons.org/ns#> .\n"
            + "@prefix dct: <http://purl.org/dc/terms/> .\n"
            + "\n")

def parse_csv_to_rdf(csv1, csv2, csv3):
    """
    @parameter csv1
    @parameter csv2
    @parameter csv3
    """
    rdf_metadata = []
    rdf_metadata.append(get_prefix())

    csv_anzahl_dateien = open(csv2, mode='r')
    csv_dummys = open(csv3, mode='r')
    matadata = open(csv1, mode='r')
    metadata_students = [row for row in csv.DictReader(matadata, delimiter=';')]
    metadata_numbers = [row for row in csv.DictReader(csv_anzahl_dateien,
                                                      delimiter=',')]
    metadata_dummys = [row for row in csv.DictReader(csv_dummys, delimiter=',')]

    for x in range(0, len(metadata_numbers)):
        rdf_metadata.append("<http://hmt-leipzig.de/Data/Person/P."+ str(metadata_students[x]['Nr'])
                            + "> a foaf:Person ;\n"
                            + "  foaf:firstname \""
                            + str(metadata_students[x]['Vorname'])
                            + "\";"  + "\n"
                            + "  foaf:lastname \"" + str(metadata_students[x]['Nachname'])
                            + "\";" + "\n"
                            + "  hd:Herkunftsort \""
                            + str(metadata_students[x]['Ort'] + "\";") + "\n"
                            + "  hd:HerkunftslandAlt \""
                            + str(metadata_students[x]['Land_historisch'] + "\";")
                            + "\n" + "  hd:HerkunftslandNeu \""
                            + str(metadata_students[x]['Land_aktuell'] + "\";") + "\n"
                            + "  hd:Immatrikulationsjahr \""
                            + str(metadata_students[x]['JahrInskription'] + "\";") + "\n"
                            + "  hd:Inskription  <http://hmt-leipzig.de/Data/Inskription/"
                            + format_number(metadata_students[x]['Inskription']) + ">;" + "\n"
                            + "  hd:Zeugnis <http://hmt-leipzig.de/Data/Zeugnis/"
                            + format_number(metadata_students[x]['Zeugnis']) + ">;" + "\n"
                            + "  hd:AnzahlZeugnisse "
                            + metadata_numbers[x]["Anzahl Dateien"] + ";\n")
        if metadata_numbers[x]["Anzahl Dateien"] is "1":
            rdf_metadata.append("  hd:Zeugnisdatei \"" +
                                format_number(metadata_students[x]['Zeugnis'])
                                + ".jpg\";\n")
        else:
            for i in range(1, int(metadata_numbers[x]["Anzahl Dateien"])+1):
                rdf_metadata.append("  hd:Zeugnisdatei \""
                                    + format_number(metadata_students[x]['Zeugnis']) +
                                    "_"+ str(i) + ".jpg\";\n")
        rdf_metadata.append("hd:ZeugnisIsDummy \"" + metadata_dummys[x]['Ist DUMMY']+"\";\n")
        rdf_metadata.append("  hd:Status \"Student\"; \n dct:modified \"2018-12-03\".\n")
    return rdf_metadata
