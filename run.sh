#!/bin/bash

#script to run sessionization.py


# check if output file exists
FILE='test/output/sessionization_file.csv'

if test -f "$FILE"; then
    rm $FILE
fi
touch $FILE

python src/sessionization.py --log_file test/input/log.csv --inactivity_file test/input/inactivity_period.txt --sessionization_file $FILE
