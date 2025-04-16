#! /usr/bin/python2

# parse_and_filter_restrict_output.py
# Takes an emboss restrict output file (table of restriction enzyme sites) and the fasta file
# that restrict used, and gets all restriction fragments beginning with an EcoRI site and ending
# with a MseI site and a length between a specified minimum and maximum.
# Writes the sequences as text, one sequence per line.
# Basically, I want the sequences I'd get from an in silico double digest. In my next step I'm
# to randomly sample from them and write a fastq file so I don't need them in a fancy format yet.

# usage: ./parse_and_filter_restrict_output.py restrict_output_file.restrict fasta_file.fa > filtered_sequences.txt

import sys

min_size = int(sys.argv[3])
max_size = int(sys.argv[4])

# read the fasta file into a dictionary (needs to work for fasta with the sequence broken into multiple lines)

uncut_sequences = {} # key=sequence name, value = DNA sequence string

with open(sys.argv[2]) as sequence_file:
    for line in sequence_file:
        if line[0] == ">": #Fasta name line--make a new entry in the dictionary
            sequence_name = line.strip()[1:]
            uncut_sequences[sequence_name] = ""
        else: # Fasta sequence line--add it to the sequence in the dictionary
            uncut_sequences[sequence_name] += line.strip()

# Step through the restrict file

with open(sys.argv[1]) as restrict_file:
    for line in restrict_file:
        if line[0] == "#": # Comment line
            if "Sequence:" in line: # Contains the name of the sequence
                sequence_name = line.split()[2]
                last_enzyme = ""
                last_5prime = 0
                last_3prime = 0
        else:
            elements = line.strip().split()
            if len(elements) > 0 and elements[0] != "Start": # Not a blank line or the table header
                this_enzyme = elements[3]
                this_5prime = int(elements[5])
                this_3prime = int(elements[6])
                if last_enzyme == "EcoRI" and this_enzyme == "MseI": # We want the forward strand
                    size = this_3prime - last_5prime
                    if size > 40 and size < 1500: # In the size range we want
                        print "C" + uncut_sequences[sequence_name][last_5prime:this_3prime] + "C" # The starting and ending C's make it look like the real reads do after adapters have been applied to the cut ends.
                elif last_enzyme == "MseI" and this_enzyme == "EcoRI": # We want the reverse strand
                    size = this_3prime - last_5prime
                    if size > 40 and size < 1500: # In the size range we want
                        revcomp = ""
                        forward_sequence = uncut_sequences[sequence_name][last_5prime:this_3prime]
                        for base in forward_sequence[len(forward_sequence)::-1]: # Step through the sequence backwards and complement the bases
                            if base == "C" or base == "c":
                                revcomp += "G"
                            elif base == "T" or base == "t":
                                revcomp += "A"
                            elif base == "G" or base == "g":
                                revcomp += "C"
                            elif base == "A" or base == "a":
                                revcomp += "T"
                            else:
                                revcomp += "N" #Just in case there is something unexpected in the sequences (there wasn't)
                        print "C" + revcomp + "C" # The starting and ending C's make it look like the real reads do after adapters have been applied to the cut ends.
                last_enzyme = this_enzyme
                last_5prime = this_5prime
                last_3prime = this_3prime
