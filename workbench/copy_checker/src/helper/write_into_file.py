"""
@author Tobias
"""
def dictionary_to_csv(my_dict, path, header="\"Nr\",\"Anzahl Dateien\"\n"):
    """
    Schreibt Dictionary in ein File.
    """
    file = open(path, "w")
    file.write(header)
    for key in sorted(my_dict):
        file.write(dictionary_to_csv_str(key, my_dict))
    file.close()

def dictionary_to_csv_str(key, my_dict):
    """
    Formatiert ein Dictionary in ein csv-String.
    Form: "key","value"
    """
    return "\"" + str(key) + "\",\"" + str(my_dict[key]) + "\"\n"
