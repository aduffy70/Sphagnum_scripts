#! /usr/bin/python

# find_fixed_bases.py
# Takes a fasta alignment file and finds variable positions in the alignment where each
# S. magellanicum "subspecies" is fixed.
# Outputs a table of alignment positions, and the fixed base for each subspecies.
# A lot of stuff is hardcoded. Sorry, not a super-flexible script. And probably memory hungry too.

# usage: ./find_fixed_bases.py fasta_alignment_file.fasta > just_the_listed_fastas.fasta

import sys
import HTSeq

fastafilename = sys.argv[1]
alignment_columns = [] # list of string of the bases in each column of the alignment
is_first_sequence = True

# Read the fasta file and store it by column
fastafile = HTSeq.FastaReader(fastafilename)
for read in fastafile:
    if is_first_sequence:
        seq_length = len(read.seq)
        for x in range(0, seq_length):
            alignment_columns.append(read.seq[x])
        is_first_sequence = False
    else:
        for x in range(0, len(read.seq)):
            alignment_columns[x] += read.seq[x]

# Find alignment columns that are variable and where each subspecies is fixed
for x in range(0, len(alignment_columns)):
    is_fixed_med = False
    is_fixed_div2 = False
    is_fixed_magni = False
    is_fixed_SA = False
    is_fixed_div1 = False
    med = "?"
    div2 = "?"
    magni = "?"
    SA = "?"
    div1 = "?"
    if len("".join(list(set(alignment_columns[x]))).replace("N","")) > 1: # This is a variable column (ignoring Ns)
        if len("".join(list(set(alignment_columns[x][0:8]))).replace("N","")) == 1:
            is_fixed_med = True
            med = "".join(list(set(alignment_columns[x][0:8]))).replace("N","")[0]
        if len("".join(list(set(alignment_columns[x][8:14]))).replace("N","")) == 1:
            is_fixed_div2 = True
            div2 = "".join(list(set(alignment_columns[x][8:14]))).replace("N","")[0]
        if len("".join(list(set(alignment_columns[x][14:22]))).replace("N","")) == 1:
            is_fixed_magni = True
            magni = "".join(list(set(alignment_columns[x][14:22]))).replace("N","")[0]
        if len("".join(list(set(alignment_columns[x][22:24]))).replace("N","")) == 1:
            is_fixed_SA = True
            SA = "".join(list(set(alignment_columns[x][22:24]))).replace("N","")[0]
        if len("".join(list(set(alignment_columns[x][24:56]))).replace("N","")) == 1:
            is_fixed_div1 = True
            div1 = "".join(list(set(alignment_columns[x][24:56]))).replace("N","")[0]
        if is_fixed_med and is_fixed_div2 and is_fixed_magni and is_fixed_SA and is_fixed_div1:
            print x, alignment_columns[x], med, div2, magni, SA, div1
