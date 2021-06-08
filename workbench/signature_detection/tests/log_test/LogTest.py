# -*- coding: utf-8 -*-
import unittest
import os
import sys
import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                r'../..')))
from  src.log.RDFLogger import RDFLogger, format_student


class RDFLoggerTest(unittest.TestCase):

    def test_init(self):
        test = RDFLogger()
        self.assertTrue(test)

    def test_format_student(self):
        self.assertEquals(format_student("/000001.jpg"), "1")

    def test_save_results(self):
        test_results = {"region": "test", "vermutung": "test", "korrekt": "test",
                         "file": "test", "date": "test"}
        test_RDFLog = RDFLogger()
        test_RDFLog.add(test_results)
        test_RDFLog.save_result()
        now = datetime.datetime.now()
        file_name = "{}_{}.ttl".format("Ergebnisse_von",
                                       now.strftime("%Y-%m-%d-%H:%M"))
        self.assertTrue(os.path.isfile(file_name))
        os.remove(file_name)

if __name__ == "__main__":
    unittest.main()
