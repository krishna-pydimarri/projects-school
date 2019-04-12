#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Invalid number of parameters!"
    echo "Usage: spark_submit_withRDD.sh [input_location] [output_location]"
    exit 1
fi

spark-submit \
    --master local[1] \
   top_trending_diffs_withRDD.py --input $1  --output $2 
