#! /usr/bin/python

# keep_fastas_on_list-rename-sort.py
# Takes a file of fasta sequences and a csv list of sequence names and corrected names.
# Outputs the fasta sequences for just the ones on the list, renamed and in the same order
# as the csv list. The list can have additional columns, but the script uses the first column
# as the orignial sequence name and the second column as the corrected name.

# usage: ./keep_fastas_on_list.py fasta_file.fasta list_of_sequence_names_to_keep.csv > just_the_listed_fastas.fasta

import sys
import HTSeq

fastafilename = sys.argv[1]
keepfilename = sys.argv[2]
sequence_order = [] # corrected sequence names in order
original_to_corrected_names = {} # key = original name, value = corrected name
kept_sequences = {} # key = corrected name, value = sequence

# Get the list of samples we want to keep
with open(keepfilename,"r") as keepfile:
    for line in keepfile:
        elements = line.strip().split(',')
        sequence_order.append(elements[1])
        original_to_corrected_names[elements[0]] = elements[1]

# Read the fasta file and store the records we want to keep in a dictionary under their corrected names
fastafile = HTSeq.FastaReader(fastafilename)
for read in fastafile:
    if read.name in original_to_corrected_names.keys():
        kept_sequences[original_to_corrected_names[read.name]] = read.seq

# Print the kept sequences in order in fasta format
for sequence in sequence_order:
    print ">" + sequence
    print kept_sequences[sequence]
