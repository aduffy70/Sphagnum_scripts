#! /usr/bin/python

# make_alignment_from_contig_blasthits.py
# Takes a fasta file of contigs and a file of blast hits against an IR-flanked cp genome and
#makes a rough alignment of the sequences against the genome by padding the start of each sequences
# to shift it into position. Writes output in fasta format.
# usage: ./make_alignment_from_contig_blasthits.py contig_file.fasta blast_output.csv > rough_alignment.fasta

import sys
import os
import HTSeq
from Bio.Seq import Seq

fastafilename = sys.argv[1]
blastfilename = sys.argv[2]

fastafile = HTSeq.FastaReader(fastafilename)
# Store the sequences in a dictionary
sequences = {} # key=seqname, value = sequence
for read in fastafile:
    sequences[read.name] = read.seq

# Parse blast output
with open(blastfilename, "r") as blastfile:
    is_firstline = True
    for line in blastfile:
        elements = line.strip().split(",")
        query = elements[0]
        if is_firstline:
            best_elements = elements[:]
            last_query = query
            is_firstline = False
        elif query != last_query:
            query_length = int(best_elements[1])
            strand = best_elements[3]
            qstart = int(best_elements[5])
            qend = int(best_elements[6])
            sstart = int(best_elements[7])
            send = int(best_elements[8])
            if strand == "plus": # forward hit
                pad_size = sstart - qstart
                pad = "-" * pad_size
                new_sequence = pad + sequences[last_query]
            else:
                pad_size = send - (query_length - qend)
                pad = "-" * pad_size
                revcomp = Seq(sequences[last_query]).reverse_complement()
                new_sequence = pad + revcomp
            print ">" + last_query
            print new_sequence
            #print best_elements
            #print str(pad_size)
            best_elements = elements[:]
            last_query = elements[0]
        else:
            if int(best_elements[4]) < int(elements[4]): #This alignment is the longest we have found
                best_elements = elements[:]
# Handle the last line
query_length = int(best_elements[1])
strand = best_elements[3]
qstart = int(best_elements[5])
qend = int(best_elements[6])
sstart = int(best_elements[7])
send = int(best_elements[8])
if strand == "plus": # forward hit
    pad_size = sstart - qstart
    pad = "-" * pad_size
    new_sequence = pad + sequences[last_query]
else:
    pad_size = send - (query_length - qend)
    pad = "-" * pad_size
    revcomp = Seq(sequences[last_query]).reverse_complement()
    new_sequence = pad + revcomp
print ">" + last_query
print new_sequence
#print best_elements
#print str(pad_size)
best_elements = elements[:]
last_query = elements[0]
