#!/usr/bin/python
"""
This script is to extract required elements from the input file.
It extracts category, country and video id from input file
Passes on category as key and country|video_id as value to combiner and reducer
"""
import sys

def mapper_function():
    for row in sys.stdin:
        row=row.strip()
        field_values=row.split(',')  #Since reading input as coma separated file
        if len(field_values) != 12:
            continue
        id_value=field_values[0]
        country=field_values[11]
        categ=field_values[3]
        if categ != "category":
            print("{}:'{}|{}'".format(categ,country,id_value)) #printing output key value to be consumed by combiner

if __name__=='__main__':
    mapper_function()
