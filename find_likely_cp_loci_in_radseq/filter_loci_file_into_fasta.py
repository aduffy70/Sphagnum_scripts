#! /usr/bin/python2

# filter_loci_file_into_fasta.py
# Takes a .loci file from ipyrad and a list of locus names (numbers) and returns
# a fasta file with a just the sequences from the loci on the list. The list file needs to
# be a tab-delimited file with the locus names in the first column. Other columns are ignored.
# (The output of "samtools view -F 4 ...." will work just fine.)
# Basically, I have a list of the chloroplast-mapping loci and I want to extract
# just those sequences in a format I can use to build trees and such.
# usage: ./filter_loci_file_into_fasta.py loci_file.loci list_of_ > output_fasta.fa

import sys

loci_to_keep = [] # list of the loci we want to keep
with open(sys.argv[2]) as list_file:
    for line in list_file:
        elements = line.strip().split()
        loci_to_keep.append(elements[0])

#This is ugly but I am going to read the file twice. Once to make sure I have a complete list of all the samples and then a second time to actually get the sequences for the loci of interest. Not all samples are listed under each locus so I can't be certain I've seen every sample til I've been through the file. There are more elegant ways to do this, but this is the fastest way to write the code and I'm probably never going to use it again. It's lazy coding. Sorry.

sample_sequences = {} #  key = sample name, value = concatenated sequences for the desired loci

with open(sys.argv[1]) as loci_file:
    for line in loci_file:
        elements = line.strip().split()
        if elements[0] != "//":
            if elements[0] not in sample_sequences.keys():
                sample_sequences[elements[0]] = ""

with open(sys.argv[1]) as loci_file:
    current_sequences = {} # key = sample name, value = sequence for current locus
    locus_length = 0
    for line in loci_file:
        elements = line.strip().split()
        if elements[0] == "//": #End of a locus alignment
            locus_name = elements[-1].split("|")[1]
            if locus_name in loci_to_keep:
                #print locus_name, locus_length
                for sample in sample_sequences.keys():
                    if sample in current_sequences.keys():
                        sample_sequences[sample] += current_sequences[sample]
                    else:
                        buffer_sequence = "-" * locus_length
                        sample_sequences[sample] += buffer_sequence
            locus_length = 0
            current_sequences = {}
        else: #A sample/sequence in the alignments
            current_sequences[elements[0]] = elements[1]
            locus_length = len(elements[1])

for sample in sample_sequences.keys():
    print ">" + sample
    print sample_sequences[sample]
