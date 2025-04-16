#! /usr/bin/python2

# cleanup_ustr_for_R.py
# Takes a ustr file from ipyrad and removes blank columns and adds a header row with locus
# names (just numbers them) so it will work properly with df2ind in R.
# usage: ./cleanup_ustr_for_R.py ustr_file.ustr > cleaned_ustr_for_R.ustr

import sys
import random

is_first_line = True

# Read and cleanup the ustr file
with open(sys.argv[1]) as ustr_file:
    for line in ustr_file:
        elements = line.strip().split("\t")
        cleaned_string = elements[0]
        column_count = 0
        for element in elements[1:]:
            if element: # Not a blank column
                cleaned_string += "\t" + element
                column_count += 1
        if is_first_line:
            #Create header row
            header_row = ""
            for x in range(0,column_count):
                header_row += "\tLocus" + str(x)
            print header_row.lstrip()
            is_first_line = False
        print cleaned_string
