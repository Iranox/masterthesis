def is_dummy_file(path_to_image):
    file_size_in_bytes = os.path.getsize(path_to_image)
    conversion_factor_byte_megabyte = math.pow(1024, 2)
    file_size_in_mb = round(file_size_in_bytes /
                            conversion_factor_byte_megabyte, 3)
    return file_size_in_mb < 1
import glob
import os
import math

all_files = glob.glob("/home/iranox/Projects/lehrer-schueler-beziehung/Daten/Ressources/Zeugnisse/00000800/*.jpg")
dummy_files = [file for file in all_files if is_dummy_file(file)]
with open('remove_dummies.sh', 'a') as file:
    for i in dummy_files:
        file.write("rm {} \n".format(i))
