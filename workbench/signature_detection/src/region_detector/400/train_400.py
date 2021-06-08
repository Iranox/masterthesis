import os

dict = [x[0] for x in os.walk("200-400")]
del dict[0]
for i in dict:
    if not os.path.exists("/nfs/user/gs289biny/new_train/400/preview/train/" + i.split("/")[1]):
        os.makedirs("/nfs/user/gs289biny/new_train/400/preview/train/" + i.split("/")[1])
    generate_augmented_images(i,0, safe_to_dir="/nfs/user/gs289biny/new_train/400/preview/train/" + i.split("/")[1])

for i in dict:
    if not os.path.exists("/nfs/user/gs289biny/new_train/400/preview/train/" + i.split("/")[1]):
        os.makedirs("/nfs/user/gs289biny/new_train/400/preview/train/" + i.split("/")[1])
    generate_augmented_images(i,0, validation_data=True, safe_to_dir="/nfs/user/gs289biny/new_train/400/preview/train/" + i.split("/")[1])
