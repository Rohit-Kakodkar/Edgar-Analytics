#!/bin/bash

#script to run sessionization.py

FILE='test_output/sessionization_file.csv'

if test -f "$FILE"; then
    rm $FILE
fi

touch $FILE

python src/sessionization.py --log_file test_input/log.csv --inactivity_file test_input/inactivity_period.txt --sessionization_file $FILE
