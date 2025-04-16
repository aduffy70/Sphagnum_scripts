#! /usr/bin/python2

# trim_and_get_all_sample_fragments.py
# Takes the output of my parse_and_filter_restrict_output.py script and makes a specified
# number of copies of each sequence trimmed to a specified length and writes them to a fastq file
# (with perfect quality scores)
# Basically, I'm generating a fake RADseq sample from the insilico digested Smag reference genome
# that includes ALL loci, rather than a randomly sampled subset. I want to know... if I put all
# the loci in the genome into ipyrad, how many get combined because of similarity? How many get
# filtered out for other reasons? It is a chance to better understand what is happening in the
# ipyrad process without the added noise of sequencing error and contamination.

# usage: ./trim_and_get_all_sample_fragments.py file_of_sequence_fragments.txt number_of_desired_reads max_length_of_trimmed_reads > fake_RADseq_sample.fastq

import sys
import random

desired_read_copies = int(sys.argv[2])
desired_read_length = int(sys.argv[3])

# trim the fragments and output the desired number of copies of each in fastq format
trimmed_reads = []

total_printed = 0 # Keep track of the reads as they are printed and provide a unique name for each

with open(sys.argv[1]) as fragment_file:
    for line in fragment_file:
        line = line.strip()
        fragment_length = len(line)
        if fragment_length > 0: # Not a blank line
            if fragment_length > desired_read_length: # It needs to be trimmed
                sequence = line[0:desired_read_length]
                sequence = sequence.rstrip("N") # Remove any trailing Ns
            else: # No trimming needed
                sequence = line
            for copy in range(desired_read_copies):
                print "@in_silico_" + str(total_printed)
                print sequence
                print "+"
                print "E" * len(sequence) # Make a fake quality line... E seems to be a typical quality level on our datasets and will pass the ipyrad quality filter
                total_printed += 1
