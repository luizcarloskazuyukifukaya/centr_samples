#!/bin/bash

# Specify the target manifest file
TARGET_MANIFEST_FILE="/mnt/c/Users/i_lov/Downloads/manifest.csv"

# Print the variable
python3 check_object_presense.py $TARGET_MANIFEST_FILE

# How to execute this bash script while outputing to the standard I/O
#bash this_script.sh | tee -a output.log
