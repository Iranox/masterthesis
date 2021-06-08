# -*- coding: utf-8 -*-
import unittest
from log_test.LogTest import RDFLoggerTest
import os
import sys


def suite():
    """
        Gather all the tests from this module in a test suite.
    """
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(RDFLoggerTest))
    return test_suite

mySuit=suite()

runner=unittest.TextTestRunner()
runner.run(mySuit)
