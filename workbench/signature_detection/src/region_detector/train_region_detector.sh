#!/bin/bash
python SignatureDetector.py

rm ../models/model_name.h5
mv models/model_name.h5 ../models/
