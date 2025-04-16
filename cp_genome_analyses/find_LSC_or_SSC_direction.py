#! /usr/bin/python

# find_LSC_or_SSC_direction.py
# Takes a csv format blast output file of a cpgenome consensus sequence blasted against an LSC or SSC sequence and uses the longest hit strand to determine if the LSC ir SSC in the genome is oriented correctly.
# Outputs a csv string of:
# sample, longest hit length, strand

# usage: find_LSC_or_SSC_direction.py blast_output.csv > output_file.csv

import sys

blastfilename = sys.argv[1]

# Parse blast output. Find the longest hit.
longest_length = 0
output_string = ""
with open(blastfilename, "r") as blastfile:
    for line in blastfile:
        elements = line.strip().split(",")
        if elements[-1] != "x": #Ignore any lines ending in "x" so I can manually exclude hits when needed.
            sample = elements[0]
            strand = elements[3]
            hit_length = int(elements[4])
            if hit_length > longest_length: #this is the longest so far
                output_string = sample + "," + str(hit_length) + "," + strand
                longest_length = hit_length
    if len(output_string) == 0: #There were no hits
        output_string = "no_hits"
print output_string
