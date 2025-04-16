#! /usr/bin/python3

# apply_population_tags_to_str.py
# Takes a str file and a csv file of samplenames, population tag integers, and population 
# flag booleans (0 or 1) and applies the tags to the 2nd column of the str file. 
# Assumes whitespace-delimited str files with the samplenames in the 1st column and no 
# header row. Should work on haploid or diploid data with one or two rows per sample--but
# I've only tested on diploid data with 1 row per sample.
# Basically, I want to run structure with preset populations for most samples so I can determine
# which population(s) other samples derive from--identifying the parents of polyploid spp for
# example. I give each preset sample an integer tag and popflag=1 and give the unknown 
# samples zero tags and popflag=0.

# usage: ./apply_population_tags_to_str.py str_file.str tag_file.csv > updated_str_file.str

import sys

# Read the csv tag file
tags = {} # key = samplename, value = tag
flags = {} # key = samplename, value = flag
with open(sys.argv[2]) as csv_file:
    for line in csv_file:
        elements = line.strip().split(",")
        if len(elements) == 3:
            tags[elements[0]] = elements[1]
            flags[elements[0]] = elements[2]
        else:
            print("Invalid tag in csv file!")

# Read the str file and convert it
str_line_length = 0 # We are going to get the length of the first line and check that all lines match to spot problems in the str file
is_firstline = True
with open(sys.argv[1]) as str_file:
    for line in str_file:
        elements = line.strip().split()
        if is_firstline:
            str_line_length = len(elements)
        else:
            if len(elements) != str_line_length:
                print("structure line length problem!")
        samplename = elements[0]
        new_elements = [samplename, tags[samplename], flags[samplename]]
        new_elements += elements[1:]
        print("\t".join(new_elements))
            
