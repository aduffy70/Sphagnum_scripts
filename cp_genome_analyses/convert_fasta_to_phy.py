#! /usr/bin/python

# convert_fasta_to_phy.py
# Converts a fasta alignment to a phy alignment.
# usage: ./convert_fasta_to_phy.py fasta_alignment.fasta new_phy_alignment.phy

import sys
from Bio import SeqIO

fasta_filename = sys.argv[1]
phy_filename = sys.argv[2]

# Get the list of samples we want to keep and load them into the keys of the dictionary
with open(fasta_filename, "r") as fasta_file:
    with open(phy_filename, "w") as phy_file:
        alignment = SeqIO.parse(fasta_file, "fasta")
        count = SeqIO.write(alignment, phy_file, "phylip")
        print "Sequences in alignment: " + str(count)
