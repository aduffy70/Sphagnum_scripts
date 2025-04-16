#! /usr/bin/python

# concatenate_fasta_alignments.py
# Takes a list of samples, a list of genes, and a folder of fasta alignment files (one for each
# gene) and outputs single alignment in fasta format. Inserts gaps when a sample is missing
# a gene. Only genes and samples in the lists will be included, even if other gene alignment
# files are present or other samples are included within the alignments. Also outputs a file
# showing the order of the genes within the concatenated alignment.
# usage: ./concatenate_fasta_alignments.py list_of_samples.txt list_of_genes.txt path_to_fasta_alignment_files > concatenated_alignment.fasta

import sys
import os
import HTSeq

genes = [] # list of genes to include
samples = {} # Key=sample, value=concatenated sequences for the alignment
list_of_samples_filename = sys.argv[1]
list_of_genes_filename = sys.argv[2]
alignment_folderpath = sys.argv[3]

# Get the list of samples we want to keep and load them into the keys of the dictionary
with open(list_of_samples_filename, "r") as list_of_samples_file:
    for line in list_of_samples_file:
        samplename = line.strip()
        samples[samplename] = ""


# Get the list of genes we want to keep
with open(list_of_genes_filename, "r") as list_of_genes_file:
    for line in list_of_genes_file:
        genename = line.strip()
        genes.append(genename)
#print "genes to keep: " + str(len(genes))

# Read the alignment by gene files and append the sequences to the correct sample
gene_order_file = open("concatenated_gene_order.txt", "w")
for filename in sorted(os.listdir(alignment_folderpath)):
    if filename.endswith(".align.fasta"):
        genename = filename[0:-12]
        if genename in genes:
            gene_order_file.write(genename + "\n")
            current_gene_sequences = {} #key=samplename, value=sequence string
            fastafile = HTSeq.FastaReader(os.path.join(alignment_folderpath,filename))
            for read in fastafile:
                samplename = read.name
                if samplename in samples.keys():
                    current_gene_sequences[samplename] = read.seq
                    current_gene_length = len(read.seq)
            for sample in samples.keys():
                if sample in current_gene_sequences.keys():
                    samples[sample] += current_gene_sequences[sample]
                else:
                    missing_data_string = "-" * current_gene_length
                    samples[sample] += missing_data_string
gene_order_file.close()

# Write the new alignment fasta data
for sample in sorted(samples.keys()):
    print ">" + sample
    print samples[sample]
