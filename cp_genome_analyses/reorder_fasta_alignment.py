#! /usr/bin/python

# reorder_fasta_alignment.py
# Takes a fasta format alignment and a csv table of original sample names and new sample names in a desired order and outputs a new fasta format alignment with the samples renamed and in the correct order--no other changes to the alignment. If you don't want to change the names, put the original name in the new names column too. I suppose these don't have to be aligned fastas. It would work on any fasta sequences.

# usage: ./reorder_fasta_alignment.py alignment.fasta order_and_newname_table.csv > renamed_reordered_fasta_alignment.fasta

import sys
import HTSeq

fastafilename = sys.argv[1]
orderfilename = sys.argv[2]
sequences = {} # key = original samplename, value = alignment sequence

# Read the fasta sequences into the sequences dictionary.
fastafile = HTSeq.FastaReader(fastafilename)
for read in fastafile:
    sequences[read.name] = read.seq

#Read the sample order file and output the sequences in order with the new name
with open(orderfilename,'r') as orderfile:
    for line in orderfile:
        elements = line.strip().split(",")
        if elements[0] in sequences.keys():
            print ">" + elements[1]
            print sequences[elements[0]]
        else:
            print "Error " + elements[0] +  "not in original alignment"
