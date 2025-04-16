#! /usr/bin/python

# find_IR_from_selfblast_hits.py
# Takes a csv format blast output file of a cpgenome consensus sequence blasted against itself,
# and uses the reverse-direction hits to try to identify which sections are inverted repeat.
# Outputs a csv string of:
# sample, length, 1st Single copy fragment length, 1st IR fragment length, 2nd Single copy fragment length, 2nd IR fragment length.... and so on.

# usage: ./find_IR_from_selfblast_hits.py blast_output.csv > output_file.csv

import sys

blastfilename = sys.argv[1]
invert_sections = {} # dictionary of invert sections. key = startbase, value = endbase

# Parse blast output. We only need query OR subject hits since they duplicate each other in a self-blast.
with open(blastfilename, "r") as blastfile:
    for line in blastfile:
        elements = line.strip().split(",")
        if elements[-1] != "x": #Ignore any lines ending in "x" so I can manually exclude hits when needed.
            sample = elements[0]
            strand = elements[3]
            sequence_length = int(elements[1])
            if strand == "minus": #this is an inverted section
                query_start = int(elements[5])
                query_end = int(elements[6])
                if query_start not in invert_sections.keys():
                    invert_sections[query_start] = query_end
# Combine overlapping blast hits
filtered_invert_sections = {} # dictionary of invert sections. key = startbase, value = endbase
previous_start = 0
previous_end = 0
is_first_section = True
for section_start in sorted(invert_sections.keys()):
    if is_first_section:
        previous_start = section_start
        previous_end = invert_sections[section_start]
        is_first_section = False
    elif section_start >= previous_start and section_start <= previous_end: # overlapping sections
        previous_end = max(previous_end, invert_sections[section_start])
    else: #not overlapping
        filtered_invert_sections[previous_start] = previous_end
        previous_start = section_start
        previous_end = invert_sections[section_start]
filtered_invert_sections[previous_start] = previous_end

output_string = sample + "," + str(sequence_length)
x = 0
previous_end = 0
for section in sorted(filtered_invert_sections.keys()):
    #print section, invert_sections[section]
    sc_length = section - previous_end - 1
    ir_length = filtered_invert_sections[section] - section + 1
    output_string = output_string + "," + str(sc_length) + "," + str(ir_length)
    previous_end = filtered_invert_sections[section]
sc_length = sequence_length - previous_end
output_string = output_string + "," + str(sc_length)
print output_string
