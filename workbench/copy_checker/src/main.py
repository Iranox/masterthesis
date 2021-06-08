"""
@author Tobias
"""
import sys
import getopt

from helper.helper import dictionary_to_csv, count_files, check_files_are_dummies
from helper.rdf_metadata import parse_csv_to_rdf, write_metadata_to_file
from helper.write_into_file import dictionary_to_csv

if __name__ == '__main__':
    INPUTFILE, OUTPUTFILE = '', "out.csv"
    DUMMY = False
    ARGS = sys.argv[1:]
    RDF, CSV1, CSV2,CSV3 = '', '', '',''
    try:
        OPTS, ARGS = getopt.getopt(ARGS, "hp:c:d", ["path=", "csv=", "dummy",
                                                    "rdf", "csv1=", "csv2=","csv3="])
    except getopt.GetoptError:
        print("Error")
        sys.exit(2)
    for opt, arg in OPTS:
        if opt == '-h':
            sys.exit()
        elif opt in ("-p", "--path"):
            INPUTFILE = arg
        elif opt in ("-c", "--csv"):
            OUTPUTFILE = arg
        elif opt in ("-d", "--dummy"):
            DUMMY = True
        elif opt in "--csv1":
            CSV1 = arg
        elif opt in "--csv2":
            CSV2 = arg
        elif opt in "--csv3":
            CSV3 = arg
    if INPUTFILE is not '' and not DUMMY:
        dictionary_to_csv(my_dict=count_files(INPUTFILE), path=OUTPUTFILE)
    elif INPUTFILE is not '' and DUMMY is True:
        dictionary_to_csv(my_dict=check_files_are_dummies(INPUTFILE),
                          path="DUMMY.csv", header="\"Nr\",\"Ist DUMMY\"\n")
    elif CSV1 is not '' and CSV2 is not '':
        write_metadata_to_file(parse_csv_to_rdf(CSV1, CSV2,CSV3))
    else:
        print("Error")
