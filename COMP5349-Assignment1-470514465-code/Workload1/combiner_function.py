#!/usr/bin/python

"""
Combiner combines all keys and stores their values(country|video_id) as list in dictionary for category key.
While storing in this way, it takes unique values of country|video_id and appends it to list.
It returns combined key(category):value(country|video_id unique ones) pairs
However, in this step on AWS, it gives four entries for each category as key as EMR seems to run 4 combiners
So, similar logic has been replicated in reducer. Combiner does help in processing faster as it reduces workload for reducer.

"""


import sys

def read_map_op(file):
    for row in file:
        yield row.strip().split(":",1)
    
def combiner_function():
    current_categ = ""
    combined_map={}
    mapped_data=read_map_op(sys.stdin)   #Take input from mapper. format is category:country|video_id
    for categ,val in mapped_data:
        if current_categ=="":
            combined_map[categ]=[val.strip("'")]   #Assumes first iteration and so adds new entry with value as list to the category key in dictionary
        else:
            if current_categ!= categ:   #Assumes first entry for this category as it is different from previous one as it assumes mapper output is sorted
                combined_map[categ]=[val.strip("'")]
            else:
                combined_map[categ].append(val.strip("'")) #If not first entry append value to the values 
                combined_map[categ]=list(set(combined_map[categ])) #Maintain the values are unique. set helps in getting unique values
        current_categ=categ
    return combined_map   #Return the dictionary formed with category key(almost or fully reduced to unique category keys) and country|video_id values 

if __name__=='__main__':
    combiner_op=combiner_function()
    for categ in list(set(combiner_op.keys())):
        print("{}:{}".format(categ,combiner_op[categ])) #print the dictionary contents to be passed on to reducer


