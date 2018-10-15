#!/bin/bash
FILE_CAP=$1
sed -i -e "s/'//g" $FILE_CAP ; cat $FILE_CAP  | tr '();,' ' ' | sort --field-separator=' ' --key=2 | tr -s " " | cut -c 2- > $FILE_CAP+test.csv
