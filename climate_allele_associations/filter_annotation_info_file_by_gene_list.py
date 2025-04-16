#! /usr/bin/python2

# filter_annotation_info_file_by_gene_list.py
# I have a JGI genome annotation info file and I want just the lines for a list of genes.
# usage: ./filter_annotation_info_file_by_gene_list.py file_with_list_of_genes.csv Smagellanicum_521_v1.1.annotation_info.txt > just_the_lines_with_info_for_my_genes.txt

import sys

#Read the file with the list of genes
gene_names_list_column = 1 # Which column (starting with zero) of the list file contains the gene names?
gene_names = [] # List to hold the gene names for which we want the info lines
with open(sys.argv[1]) as gene_list_file:
    for line in gene_list_file:
        if line[0] != "#": # It is not a header line
            elements = line.strip().split(",")
            gene_name = elements[gene_names_list_column]
            if gene_name not in gene_names:
                gene_names.append(gene_name)
#print("\n".join(gene_names))

# Read the annotation info file
already_printed = [] # If a gene is in the list more than once (multiple transcripts) we only want to print it the first time
gene_names_info_column = 1 # The gene name I want to match is in column 1 (starting with zero) of this file
with open(sys.argv[2]) as annotation_info_file:
    for line in annotation_info_file:
        elements = line.strip().split()
        gene_name = elements[gene_names_info_column]
        if gene_name in gene_names and gene_name not in already_printed: # We want this line
            print(line.strip())
            already_printed.append(gene_name)
