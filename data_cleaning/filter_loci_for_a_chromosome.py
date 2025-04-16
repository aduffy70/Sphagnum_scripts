#! /usr/bin/python2

# filter_loci_for_a_chromosome.py
# Takes the .loci output of ipyrad, a list of sample names, and the name of a chromosome, and
# outputs a fasta format concatenated alignment of all the loci on the chromosome for all
# samples in the list.
# Basically, I want to do analyses by chromosome for radseq data and this is a simple way to
# get the data for a single chromosome. The .loci format doesn't include samples at a locus that
# are entirely missing data, so I need the list of samples to make sure I know which samples
# are missing at each locus so I can insert missing data of the correct length to keep the
# alignment aligned.
# Use 1 for the data flag to get the alignment. 0 to just get the locus count
# usage: ./filter_loci_for_a_chromosome.py ipyrad_loci_file.loci list_of_samplenames.csv chromosome_name_string dataflag_int > filtered_alignment.fasta

import sys
import random

chromosome_to_keep = (sys.argv[3]) + ":" # Include the : in the chromosome name to be certain if we ask for LG1 we won't get LG11, LG12, LG13... and so on.
output_alignment = int(sys.argv[4]) # 1= output alignment; 0=output locus count

# Get the list of samples
samplenames = [] # list to hold the sample names
sample_sequences = {} # dictionary to hold the sequences for each sample. key=samplename, value=sequence
locus_count = 0 # Keep track of how many loci we find for testing purposes

with open(sys.argv[2]) as samplenames_file:
    for line in samplenames_file:
        samplename = line.strip()
        samplenames.append(samplename)
        sample_sequences[samplename] = ""

# Read the loci and save the sequences for the desired chromosome
this_locus = {} # dictionary to hold the sequences for the current locus til we get to the end and know if it is on the desired chromosome. key=samplename, value = sequence

locus_length = 0 # keep track of the current locus length
with open(sys.argv[1]) as loci_file:
    for line in loci_file:
        elements = line.strip().split()
        if elements[0] == "//": # End of a locus. Let's process it...
            if chromosome_to_keep in elements[-1]: #This locus is on the desired chromosome
                locus_count += 1
                for samplename in samplenames:
                    if samplename in this_locus.keys():
                        sample_sequences[samplename] += this_locus[samplename]
                    else: #sample is missing data for this locus. fill with Ns
                        sample_sequences[samplename] += "N" * locus_length
            this_locus = {}
            locus_length = 0
        else: # this is a data line. Store it til we reach the end of the locus
            samplename = elements[0]
            sequence = elements[1]
            locus_length = len(sequence)
            this_locus[samplename] = sequence

if output_alignment == 1:
    for samplename in samplenames:
        print ">" + samplename
        print sample_sequences[samplename]
else:
    print locus_count
