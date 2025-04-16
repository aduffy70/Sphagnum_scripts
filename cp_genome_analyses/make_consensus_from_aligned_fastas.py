#! /usr/bin/python

# make_consensus_from_aligned_fastas.py
# Takes a fasta file of aligned sequences and makes a single consensus sequence in fasta format.
# Gaps are ignored unless an entire column is gaps, which is removed.
# Columns with conflicts are converted to Ns.
# * are treated as gaps.
# Final sequence name comes from the file name (everything before the first period).
# usage: ./make_consensus_from_aligned_fastas.py aligned_fasta_file.fasta > consensus_fasta.fasta

import sys
import os
import HTSeq

fastafilename = sys.argv[1]
seqname = fastafilename.split("/")[-1].split(".")[0]
sequences = [] # to store the sequences in the alignment

# Read the aligned sequences into a list and check they are the same length
is_first_sequence = True
is_equal_lengths = True
fastafile = HTSeq.FastaReader(fastafilename)
for read in fastafile:
    if is_first_sequence:
        length = len(read.seq)
        is_first_sequence = False
        sequences.append(read.seq)
    elif length != len(read.seq):
        print "Error! Lengths don't match. Problem with the alignment?"
        is_equal_lengths = False
    else:
        sequences.append(read.seq)

# Make the consensus sequence from the individual aligned sequences
if is_equal_lengths:
    consensus = ""
    for x in range(0, length):
        this_base = []
        for sequence in sequences:
            if sequence[x] not in ["-", "*"]:
                if sequence[x].upper() in ["A", "G", "T", "C", "N"]:
                    this_base.append(sequence[x].upper())
                else:
                    this_base.append("N")
                    #print sequence[x]
        if len(this_base) > 0:
            if "N" in this_base:
                consensus += "N"
            elif this_base[1:] == this_base[:-1]: # True if all items in list are identical
                consensus += this_base[0]
            else:
                consensus += "N"
    print ">" + seqname
    print consensus
#if length != len(consensus):
#    print seqname,
#    print str(length-len(consensus))
