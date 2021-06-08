import unittest
from helper_test.helper_test import *
from helper_test.metadata_test import *
def suite():
    """
        Gather all the tests from this module in a test suite.
    """
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(Helper_Test))
    test_suite.addTest(unittest.makeSuite(Metadata_Test))
    return test_suite

if __name__ == '__main__':
    mySuit=suite()
    runner=unittest.TextTestRunner()
    runner.run(mySuit)
