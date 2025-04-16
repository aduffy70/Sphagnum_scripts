#! /usr/bin/python2

# get_example_seq_from_ipyrad_loci.py
# Takes a .loci file from ipyrad and returns a fasta file with a randomly chosen
# sequence for each locus with any gaps removed. Won't choose sequences from
# a list of samples so I can be sure to just get ingroup sequences.
# usage: ./get_example_seq_from_ipyrad_loci.py loci_file.loci > output_fasta.fa

import sys
from random import randint

with open(sys.argv[1]) as loci_file:
    sample_count = 0
    outgroup = ["SB5423_2018-311_affine_ME", "SB5519_2018-65_GA", "SB5427_2018-326_ME_O"]
    sequences = [] # list of sequences in an alignment
    fasta_header = ">"
    for line in loci_file:
        elements = line.strip().split()
        if elements[0] == "//": #End of a locus alignment
            fasta_header = fasta_header + elements[-1].split("|")[1] + "\t" + str(sample_count)
            example_sequence = sequences[randint(0,len(sequences) - 1)] #grab a randomly selected sequence
            example_sequence = example_sequence.replace("-","") #Get rid of the gaps
            print fasta_header
            print example_sequence
            sample_count = 0
            sequences = []
            fasta_header = ">"
        else: #A sample/sequence in the alignments
            if elements[1] not in outgroup:
                sample_count += 1
                sequences.append(elements[1])
