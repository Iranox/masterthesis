from Imagegenerator import generate_augmented_images

if __name__ == '__main__':
    generate_augmented_images("/home/iranox/Projects/lehrer-schueler-beziehung/workbench/signature_detection/Rauschfilter/Unterschriften"
                              ,30,validation_data=False, safe_to_dir="data/train/signature")
    generate_augmented_images("/home/iranox/Projects/lehrer-schueler-beziehung/workbench/signature_detection/Rauschfilter/Unterschriften"
                              ,4,validation_data=True, safe_to_dir="data/validation/signature")
    generate_augmented_images("/home/iranox/Projects/lehrer-schueler-beziehung/workbench/signature_detection/Rauschfilter/Rauschen"
                              ,4,validation_data=True, safe_to_dir="data/validation/not_signature")
    generate_augmented_images("/home/iranox/Projects/lehrer-schueler-beziehung/workbench/signature_detection/Rauschfilter/Rauschen"
                              ,40,validation_data=False, safe_to_dir="data/train/not_signature")
