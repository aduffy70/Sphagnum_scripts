#! /usr/bin/python

# make_contig_names_unique.py
# Takes a fasta file and renames the sequences in it with sequential numbers so they are all unique.
# usage: ./make_contig_names_unique.py fasta_file.fasta > renamed_fasta.fasta

import sys
import os
import HTSeq

fastafilename = sys.argv[1]

fastafile = HTSeq.FastaReader(fastafilename)
count = 0
for read in fastafile:
    print ">" + str(count)
    print read.seq
    count += 1
