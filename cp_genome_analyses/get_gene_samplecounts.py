#! /usr/bin/python

# get_gene_sample_counts.py
# Takes a folder of fasta files (one for each sample) and determines How many samples have
# sequence data for each gene. Outputs a table of gene names and sample counts in csv format.
# usage: ./get_gene_sample_counts.py path_to_fasta_files > outputfile.csv

import sys
import os
import HTSeq

genes = {} # key = gene, value = list of samples with that gene
samples = [] # List of all sample names
folderpath = sys.argv[1]

for filename in os.listdir(folderpath):
    if filename.endswith(".fasta"):
        samplename = filename[0:-6]
        samples.append(samplename)
    fastafile = HTSeq.FastaReader(os.path.join(folderpath,filename))
    for read in fastafile:
        genename = read.name
        if genename in genes.keys():
            genes[genename].append(samplename)
        else:
            genes[genename] = [samplename]


for gene in genes.keys():
    print "%s,%s" % (gene, str(len(genes[gene])))
