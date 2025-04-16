#! /usr/bin/python

# concatenate_fastas.py
# Takes multiple fasta files and concatenates all the sequences for samples with the same
# name. Keeps the samples in the same order they are found in the files. Notice: If a sample is missing from a file it doesn't try to insert gaps to match.

# usage: ./concatenate_fastas.py fasta_1.fasta fasta_2.fasta fasta_etc.fasta > consensus_fasta.fasta

import sys
import HTSeq

fastafilenames = sys.argv[1:]
cat_sequences = {} # key = samplename, value = sequences
sample_order = [] # list of samplenames in the order found

# Read the fasta files and concatenate the sequences
for fastafilename in fastafilenames:
    fastafile = HTSeq.FastaReader(fastafilename)
    for read in fastafile:
        if read.name in cat_sequences.keys():
            cat_sequences[read.name] += read.seq
        else:
            cat_sequences[read.name] = read.seq
            sample_order.append(read.name)

# Output the concatenated sequences in fasta format
for sample in sample_order:
    print ">" + sample
    print cat_sequences[sample]
