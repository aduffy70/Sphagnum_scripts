#! /usr/bin/python2

# get_read_lengths_from_fasta.py
# Takes a fasta file and returns a csv table of readnames and read lengths.
# Basically, I want to know how long each contig is in a reference genome.
# usage: ./get_read_lengths_from_fasta.py fasta_file.fa > output_table.csv

import sys

with open(sys.argv[1]) as fasta_file:
    readname = ""
    readlength = 0
    for line in fasta_file:
        line_text = line.strip()
        if line_text[0] == ">": #It is a header line
            if readname != "": # It isn't the very first line
                print readname + "," + str(readlength)
            readname = line_text[1:]
            readlength = 0
        else: #It is a sequence line
            readlength += len(line_text)
