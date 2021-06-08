import datetime


def format_student(student):
    formated_student = student.split("/")[-1]
    formated_student = formated_student.replace(".jpg", "").lstrip("0")
    if "_" in formated_student:
        return formated_student.split("_")[0]
    return formated_student



class RDFLogger():
    def __init__(self):
        super(RDFLogger, self).__init__()
        prefix = ("@prefix rdf: <http://www.w3.org/1999/02/" +
                       "22-rdf-syntax-ns#> .\n"
                       + "@prefix qb: <http://www.w3.org/2002/07/owl#> .\n"
                       + "@prefix hd: <http://hmt-leipzig.de/Data/Experiment#> .\n"
                       + "@prefix dct: <http://purl.org/dc/terms/> .\n"
                       + "@prefix hdLehrer: <http://hmt-leipzig.de/Data/Person/Lehrer> .\n"
                       + "@prefix hdSchueler: <http://hmt-leipzig.de"
                       + "/Data/Person/Schueler/> .\n")
        self.template = ("<http://hmt-leipzig.de/Experiment/{}/{}>  a "
                         + "qb:Observation; \n hd:Region \"{}\";\n"
                         + " hd:Vermutung hdLehrer:{};\n"
                         #+ " hd:korrekterLehrer hdLehrer:{};\n"
                         + " hd:Korrekt   \"{}\";\n"
                         + " hd:Dateiname \"{}\";\n"
                         + " dct:modified \"{}\";\n"
                         + " hd:Wahrscheinlichkeit \"{}\".\n")

        self.empty_region_templage = ("<http://hmt-leipzig.de/Experiment/{}> a"
                                       + " qb:Observation; \n hd:Region \"{}\";\n"
                                       + " hd:Dateiname \"{}\";\n"
                                       + " hd:Empty \"True\";\n"
                                       + " hd:Lehrer hdSchueler:{}.\n" )
        self.template_relationship = ("<http://hmt-leipzig.de/Data/Experiment/{}> a qb:Observation;\n"
                                      + "   qb:dataSet hd:dataset1;\n"
                                      + "   hd:Schueler hdSchueler:{};\n"
                                      + "   hd:Lehrer hdLehrer:{};\n"
                                      + "   hd:Wahrscheinlichkeit \"{}\";\n"
                                      + "   hd:Region \"{}\" ;\n"
                                      + "   hd:LehrerUnterschrift \"{}\" ;\n")
                                     # + "   hd:Fach\"{}\"@de.\n")
        self.result = []
        self.relationship = []
        now = datetime.datetime.now()
        self.file1 = "Ergebnisse_von_{}.ttl".format(now.strftime("%Y-%m-%d-%H:%M"))
        self.index_of_rela = 933
        self.index_of_result = 0

        file_rdf_log = open(self.file1, "w")
        file_rdf_log.write(prefix)
        file_rdf_log.close()
        self.file2 = "Beziehung_801_1000.ttl"
        file_rdf_log = open(self.file2, "a")
        #file_rdf_log.write(prefix)
        file_rdf_log.close()

    def add_empty_region(self, region):
        self.empty_region.append(region)

    def add(self, result):
        self.result.append(result)

    def add_relationship(self, relationship):
        relationship["student"] = format_student(relationship["file"])
        self.relationship.append(relationship)

    def _write_into_file(self, file_name, text_generate_function):
        now = datetime.datetime.now()
        file_rdf_log = open(file_name, "a")
        file_rdf_log.write("\n")
        for item in text_generate_function():
            file_rdf_log.write(item)
        file_rdf_log.close()

    def _create_results(self):
        now = datetime.datetime.now()
        template = self.template
        for counter, value in enumerate(self.result):
            self.index_of_result = 1 + self.index_of_result
            yield(template.format(now.strftime("%Y-%m-%d"),
                                 str(self.index_of_result), str(value["region"]),
                                 str(value["vermutung"]), str(value["korrekt"]),
                                 str(value["file"]), str(value["date"]),
                                 value["predict"]))
            yield("\n")

    def _save_relationship(self):
        template = self.template_relationship
        empty_region_templage = self.empty_region_templage
        for counter, value in enumerate(self.relationship):
            self.index_of_rela = 1 + self.index_of_rela
            if value["empty"]:
                yield(empty_region_templage.format(self.index_of_rela, value["region"]+1,
                      value["file"].split("/")[-1], format_student(value["file"])))
            else:
                yield(template.format(str(self.index_of_rela), str(value["student"]),
                                      str(value["vermutung"]),value["predict"],
                                      str(value["region"]+1 ),
                                      str(value["unterschrift"])))

    def save_result(self):
        if self.result:
            self._write_into_file(self.file1, self._create_results)
            self.result = []
        if self.relationship:
            self._write_into_file(self.file2, self._save_relationship)
            self.relationship = []
