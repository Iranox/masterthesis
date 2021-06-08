"""
@author Tobias
"""
import os

def check_files_are_dummies(path):
    """
    Geht alle Dateien durch und überprueft ob es eine Dummy-Datei ist.
    """
    folders = get_all_files(path)
    dummyies = {}
    for folder in folders:
        for file in os.listdir(folder):
            matrikel = file.replace('.jpg', '')
            if (matrikel not in dummyies and "_" not in matrikel and
                    allowed_filetyps(matrikel)):
                dummyies[int(matrikel)] = is_dummy_file(folder+"/"+file)
            elif "_" in matrikel and allowed_filetyps(matrikel):
                matrikel = matrikel.split("_")[0]
                dummyies[int(matrikel)] = False
    return dummyies

def count_files(path):
    """
    Ermittelt die Anzahl der Zeugnisse pro Matrikel
    """
    folders = get_all_files(path)
    files_pro_matrikel = {}
    for folder in folders:
        for file in os.listdir(folder):
            matrikel = file.replace('.jpg', '')
            if matrikel not in files_pro_matrikel and allowed_filetyps(matrikel):
                if "_" in matrikel:
                    newfile = matrikel.split("_")[0]
                    if int(newfile) not in files_pro_matrikel:
                        files_pro_matrikel[int(newfile)] = 1
                    else:
                        files_pro_matrikel[int(newfile)] = files_pro_matrikel[int(newfile)] + 1
                elif allowed_filetyps(matrikel):
                    files_pro_matrikel[int(matrikel)] = 1
    return files_pro_matrikel

def get_all_files(path):
    """
    Ermittelt alle Ordner in dem Pfad. Der erste Inhalt ist der Pfad selber,
    dieser wird daher gelöscht.
    """
    folders = [x[0] for x in os.walk(path)]
    del folders[0]
    return folders


def allowed_filetyps(file_name):
    """
    Es sollen nur jpg Dateien benutzt werden
    """
    if "Kopie" in file_name:
        return False
    if "." not in file_name:
        return True
    typ = str(file_name).split(".")[1]
    return typ not in ["db", "png"]

def is_dummy_file(file_name):
    """
    @parameter file_name
    """
    import math
    file_size_in_bytes = os.path.getsize(file_name)
    conversion_factor_byte_megabyte = math.pow(1024, 2)
    file_size_in_mb = round(file_size_in_bytes / conversion_factor_byte_megabyte, 3)
    return file_size_in_mb < 1
