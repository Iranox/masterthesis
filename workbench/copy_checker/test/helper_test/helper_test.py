import unittest
import os
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..')
sys.path.append(os.path.join(ROOT, 'src'))

from helper.helper import *
from helper.write_into_file import *

class Helper_Test(unittest.TestCase):

    def setUp(self):
        pass

    def test_is_dummy(self):
        self.assertTrue(is_dummy_file("testdata/zeugnis/00000001.jpg"))

    def test_dictionary_to_csv(self):
        test = {"1":"3"}
        dictionary_to_csv(test,"test.txt")
        self.assertTrue(os.path.isfile("test.txt"))

    def test_dictionary_to_csv_str(self):
        self.assertEqual( "\"1\",\"2\"\n", dictionary_to_csv_str(key=int(1),
                                                                 my_dict={1:2}))
    def test_allowed_filetyps(self):
        self.assertTrue(allowed_filetyps("000"))
        self.assertTrue(allowed_filetyps("000.jpg"))
        self.assertFalse(allowed_filetyps("000.db"))
        self.assertFalse(allowed_filetyps("Kopie von 000"))

    def test_get_all_files(self):
        self.assertEqual(1,len(get_all_files("testdata")))

    def test_count_files(self):
        tmp = count_files("testdata/")
        self.assertEqual(1,tmp[1])

    def test_check_files_are_dummies(self):
        tmp = check_files_are_dummies("testdata/")
        self.assertTrue(tmp[1])
