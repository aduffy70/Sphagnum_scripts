#! /usr/bin/python

# make_fasta_for_each_gene.py
# Takes a list of genes and a folder of fasta files (one for each sample) and outputs a file
# file for each gene with all of the sequences from all samples for that gene. The new files
# are written to a specified folder.
# usage: ./make_fasta_for_each_gene.py list_of_genes.txt path_to_fasta_files_by_sample path_for_new_fasta_files_by_gene

import sys
import os
import HTSeq

genes = {} # key = gene, dict with key=sample and value=sequence
samples = [] # List of all sample names
list_of_genes_filename = sys.argv[1]
in_folderpath = sys.argv[2]
out_folderpath = sys.argv[3]

# Get the list of genes we want to keep
with open(list_of_genes_filename, "r") as list_of_genes_file:
    for line in list_of_genes_file:
        genename = line.strip()
        print genename
        genes[genename] = {}

# Read the fastas by sequence and store the sequences by gene in the dictionary
for filename in os.listdir(in_folderpath):
    if filename.endswith(".fasta"):
        samplename = filename[0:-6]
        samples.append(samplename)
        fastafile = HTSeq.FastaReader(os.path.join(in_folderpath,filename))
        for read in fastafile:
            genename = read.name
            if genename in genes.keys():
                genes[genename][samplename] = read.seq

# Write the new fasta files by gene
for gene in genes.keys():
    outputfile = open(os.path.join(out_folderpath, gene + ".fasta"), "w")
    for sample in genes[gene].keys():
        outputfile.write(">" + sample + "\n")
        outputfile.write(genes[gene][sample] + "\n")
    outputfile.close()
