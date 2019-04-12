#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Invalid number of parameters!"
    echo "Usage: ./average_country_number.sh [input_location] [output_location]"
    exit 1
fi

#hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.9.0.jar  \
hadoop jar /usr/lib/hadoop/hadoop-streaming-2.8.5-amzn-1.jar   \
-D mapreduce.job.reduces=1 \
-D mapreduce.job.name='Category and Trending Correlation' \
-file mapper_function.py \
-mapper mapper_function.py \
-file combiner_function.py \
-combiner combiner_function.py \
-file reducer_function.py \
-reducer reducer_function.py \
-input $1 \
-output $2
