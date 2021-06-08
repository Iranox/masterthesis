import os
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.append(os.path.join(ROOT, 'src'))

from helper.helper import *

if __name__ == '__main__':
    import timeit
    print(timeit.timeit("is_dummy_file(\"../test/testdata/zeugnis/00000001.jpg\")",
          setup="from helper.helper import is_dummy_file",number=6200))
