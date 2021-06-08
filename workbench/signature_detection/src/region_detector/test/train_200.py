from Imagegenerator import generate_augmented_images
import os

dict = [x[0] for x in os.walk("0-200")]
del dict[0]
for i in dict:
    if not os.path.exists("preview/train/" + i.split("/")[1]):
        os.makedirs("preview/train/" + i.split("/")[1])
    generate_augmented_images(i,0, safe_to_dir="preview/train/" + i.split("/")[1])
