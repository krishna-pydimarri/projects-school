#!/usr/bin/python
"""
This script loads input file into rdd.  
Reads the relevant fields: video_id,trending_date,category/category_id,views,likes,dislikes,country and converts date to datetime type.
Sorts the rdd based on video_id,trending_date
Makes new key based on video_id|country|category and store values (likes,dislikes).
Does a groupBy key and maps values as list of (likes,dislikes). Since the records are sorted based on trending date,video id the first two tuples after group by are the first two consecutive trending date (likes,dislikes)
Using these values, find difference of likes and dislikes and find gap
Sort results based on difference in descending order and take top 10 for output
"""

import argparse
from pyspark import SparkContext, SparkConf
from datetime import datetime


"""
Below functions extracts first two consecutive trending date's likes,dislikes and gets difference of them. For those which dont have any difference, we assign -999999 as default to push them to bottom
"""
def extract_top_2(rec):
    key_val,list_vals=rec
    video_Id=key_val.split("|")[0]  #Key has three parts - id,country,category
    country=key_val.split("|")[1]
    category=key_val.split("|")[2]
    if len(list_vals)>1:  #If at all there are two trending appearances
        first_time=list_vals[0]
        second_time=list_vals[1]
        diff_val=(int(second_time[1])-int(first_time[1]))-(int(second_time[0])-int(first_time[0]))
    else:
        diff_val=-999999
    return key_val,list_vals,int(diff_val),video_Id,country,category

"""
Below function extracts required fields when applied in map on rdd
"""
def extractingFields(record):
    try:
        video_id,trending_date,category_id,category,publish_time,views,likes,dislikes,comment_count,ratings_disabled,video_error_or_removed,country = record.split(",")
        #trending_date=datetime.strptime(trending_date, '%y.%d.%m')
        return (video_id, trending_date,category_id,category,views,likes,dislikes,country)
    except:
        return ()


if __name__ == "__main__":
    sc = SparkContext(appName="Top trending videos with more dislikes-RDD")
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="the input path",
                        default='~/assign1_part2/')  #defining input argument
    parser.add_argument("--output", help="the output path. Default is trending_dislikes_growth", 
                        default='trending_dislikes_growth_withRDD') #defining output argument
    args = parser.parse_args()
    input_path = args.input
    output_path = args.output
    input_file=input_path + "AllVideos_short.csv"
    input_data=sc.textFile(input_file)
    input_rdd=input_data.map(extractingFields) #Apply map to extract required fields
    input_rdd=input_rdd.filter(lambda x: x[1] != "trending_date") #Exclude header
    input_rdd=input_rdd.map(lambda rec: (rec[0], datetime.strptime(rec[1], '%y.%d.%m'),int(rec[2]),rec[3],int(rec[4]),int(rec[5]),int(rec[6]),rec[7],rec[0]+"|"+rec[7]+"|"+rec[3],(rec[5],rec[6]))).sortBy(lambda x: (x[0],x[1])) #Convert datetime as string to datetime field, ints to ints etc. Last two columns will be used as key and value. Key is video_id|country|category and value is (likes,dislikes)
    kv_input=input_rdd.map(lambda rec: (rec[8],rec[9])) #Keep key value in separate rdd
    processed_kv_input=kv_input.groupByKey().mapValues(list) #Do group by on key and values are converted into list of values.
    output=processed_kv_input.map(extract_top_2) #Extract difference value based on first two consecutive values
    final_output=output.sortBy((lambda x: x[2]),ascending=False) #Sort the resulting rdd based on difference value in descending order
    final_output=sc.parallelize(final_output.map(lambda x:(str(x[3]),x[2],str(x[5]),str(x[4]))).take(10)) #Select top 10 values and convert to strings to avoid u' characters
    final_output.saveAsTextFile(output_path) #save to output file
