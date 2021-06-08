#!/bin/bash
preview="preview/train/*";
for entry in "$preview";do
  rm $entry/*.jpg;
done

preview="preview/validation/*";
for entry in "$preview";do
  rm $entry/*.jpg;
done

python generate_signature_train_data.py
python SignatureDetector.py

#mv ../models/model_name_epochen_50_steps_all.h5 ../models/model_name_epochen_50_steps_all_old.h5
#mv models/model_name_epochen_50_steps_all.h5 ../models/
