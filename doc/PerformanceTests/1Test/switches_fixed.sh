#!/bin/bash
FILE_CAP=$1
sed -i -e "s/'//g" $FILE_CAP ; cat $FILE_CAP  | tr '[];,' ' ' | sort --field-separator=" " --key=3 | tr -s " " > $FILE_CAP+_test.csv
