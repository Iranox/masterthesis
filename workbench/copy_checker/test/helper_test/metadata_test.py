import unittest
import os
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..')
sys.path.append(os.path.join(ROOT, 'src'))

from helper.rdf_metadata import *

class Metadata_Test(unittest.TestCase):

    def setUp(self):
        pass

    def test_format_number(self):
        self.assertEqual("00000001",format_number(1))

    def test_parse_csv_to_rdf(self):
        self.assertEqual(18,len(parse_csv_to_rdf("testdata/test_metadata_student.csv" ,
                            "testdata/test_anzahl_der_dateien.csv", "testdata/isDummy.csv" )))
