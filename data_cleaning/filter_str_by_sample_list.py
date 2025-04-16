#! /usr/bin/python2

# filter_str_by_sample_list.py
# Takes a str (or ustr) file and a file with a list of samples and outputs
# a new str file with only the samples in the list.
# Basically, I have ustr output from ipyrad and I want to make different
# sample subsets for structure analysis.
# usage: ./filter_str_by_sample_list.py str_file.str list_of_samples.txt > filtered_str_file.str

import sys
import random

# Get the list of samples to keep
samplenames = [] # list to hold the sample names
with open(sys.argv[2]) as samplenames_file:
    for line in samplenames_file:
        samplename = line.strip()
        samplenames.append(samplename)

# Read the str file and only output lines for samples on the list.
with open(sys.argv[1]) as str_file:
    for line in str_file:
        elements = line.strip().split()
        if elements[0] in samplenames:
            print line.strip()
