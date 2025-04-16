#! /usr/bin/python

# concatenate_nexus_files.py
# Takes two or more nexus files and concatenates them. If a sample is missing in
# a file, that sequence is replaced by ???s in the final concatenation.

# This only gives the new MATRIX block. I only need this once so didn't take the time to figure
# out how to do the excluded characters section...I did it manually.

# usage: ./concatenate_nexus_files.py nexus_file.nex another.nex etc.nex > matrix_block.txt

import sys

# Get the individual nexus file names
file_names = sys.argv[1:]



# Read the nexus files
sample_names = [] # master list of all samples in all files
sequences = {} # key = file name, value = dict of key=sample name, value=sequence
lengths = {} # key = file name, value = length of sequences in the file
longest_sample_name = 0 # We need to know how long the longest sample name is

for file_name in file_names:
    sequences[file_name] = {}
    with open(file_name) as nexus_file:
        is_matrix = False # Keep track of when we reach the matrix of sequence data
        for full_line in nexus_file:
            line = full_line.strip()
            if line == "MATRIX": # Start of the matrix section
                is_matrix = True
            elif is_matrix and line == "END;": # End of the matrix section
                is_matrix = False
            elif is_matrix and line != ";": # This is a sequence line
                elements = line.split()
                sample_name = elements[0]
                sequence = elements[1]
                sequences[file_name][sample_name] = sequence
                if sample_name not in sample_names:
                    sample_names.append(sample_name) # Add sample name to the master list of samples
                    if len(sample_name) > longest_sample_name:
                        longest_sample_name = len(sample_name)
                if file_name not in lengths.keys():
                    lengths[file_name] = len(sequence) # Grab the length of the sequence if we haven't already for this file
sample_names.sort()
for sample_name in sample_names:
    concatenated_sequence = ""
    for file_name in file_names:
        if sample_name in sequences[file_name].keys():
            concatenated_sequence += sequences[file_name][sample_name]
        else:
            concatenated_sequence += "?" * lengths[file_name]
    padding = " " * ((longest_sample_name + 1) - len(sample_name))
    print sample_name +  padding  + concatenated_sequence

for file_name in file_names:
    print file_name, str(lengths[file_name])
