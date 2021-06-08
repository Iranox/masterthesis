"""
@autor Tobias
Diese Modul extrahiert die historischen und aktuellen Länder aus dem Metadaten.
Diese Länder könnten für eine Anreicherung der Metadaten benutzt werden.
"""
import csv


def write_into_file(name, liste):
    """
    Schreibt die Liste in eine Datei
    """
    file = open(name, "w")
    for item in liste:
        file.write(item)
        file.write('\n')
    file.close()

def remove_duplicate_in_list(liste, column_name):
    """
    Entfernt die Dupliate aus einer Liste.
    """
    return list(set([row[column_name] for row in liste]))

if __name__ == '__main__':

    METADATA = open('/home/iranox/Projects/lehrer-schueler-beziehung'
                    + '/Daten/HMT1-6200.csv', mode='r')
    METADAT_PARSED = [row for row in csv.DictReader(METADATA, delimiter=';')]
    LAND_AKTUELL = remove_duplicate_in_list(METADAT_PARSED, 'Land_aktuell')
    write_into_file("Land_aktuell.txt", LAND_AKTUELL)
    LAND_HISTORISCH = remove_duplicate_in_list(METADAT_PARSED,
                                               'Land_historisch')
    write_into_file("Land_historisch.txt", LAND_HISTORISCH)
