#!/usr/bin/python

"""
Reducer reads from combiner output and calculates average value.
It ensures that keys it get are unique and not repeated entries from combiner. If there are repeated entries in case of multiple combiners,
it will merge them all and makes a dictionary with single entry for each category as key and all values unique mapped against them. 
Since on AWS, 4 combiners were running this has been built.

Once dictionay is ensured has unique categories as keys and all their unique values are mapped to them, 
for each category we make a dictionary with video_id as key and all unique countries for it as values by making split based on | delimiter and 
then using count of keys as denominator and sum of unique countries list as numerator average is calculated

"""

import sys

def read_map_op(file):
    for row in file:
        yield row.strip().split(":",1) #read input from combiner

def reducer_function():
    mapped_data=read_map_op(sys.stdin)
    unique_categ_map={}
    for categ, mappings in mapped_data: #By reading from combiner output this makes dictionary with category as key and ensures each category has 1 entry
        mappings=mappings.strip("[]").lstrip("'").rstrip("'").strip("'").split(",")
        mappings=[x.strip().strip("'") for x in mappings]
        if categ not in unique_categ_map.keys():
            unique_categ_map[categ]=mappings
        else:
            unique_categ_map[categ].extend(mappings) #extend is used instead of append as it will add elements of list at the end of this list instead of adding the complete list itself
    final_op={}
    for categ_val in unique_categ_map.keys():
        id_cntry_cnt_map={} # for each category, initialisng dictionary to store video_id as key and all its counries(unique) as values
        for map_val in unique_categ_map[categ_val]: #Read all country|video_id for a category
            map_val=map_val.strip().split("|")
            id_val=map_val[1].strip("'")  #extract video_id
            country=map_val[0]  #extract country
            if id_val not in id_cntry_cnt_map.keys():  #If video id is being parsed for first time, country is added to its value as list type in dict
                id_cntry_cnt_map[id_val]=[country]
            else:
                id_cntry_cnt_map[id_val].append(country) #Otherwise, it will append country for the video id
                id_cntry_cnt_map[id_val]=list(set(id_cntry_cnt_map[id_val])) #Keep and mainatin unique country values for a video id
        average_val=(sum([len(id_cntry_cnt_map[id_val]) for id_val in id_cntry_cnt_map.keys()])*1.0)/len(id_cntry_cnt_map.keys()) #Average is calcualted for the category. Numerator is sum of distinct countries per video and denominator is distinct number of video ids. *1.0 is done in numerator to convert to float type
        final_op[categ_val]=round(average_val,2) #Store category and its average value in dictionary
    return final_op  #Return back dictionary containing category and average value mapping

if __name__=='__main__':
    output=reducer_function()
    for key in output.keys():
        print("{}:{}".format(key,output[key]))  #Print output from dictionary containing category and average value mapping
