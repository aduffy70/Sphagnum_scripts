#! /usr/bin/python2

# find_nonidentical_clone_genotyes_in_vcf.py
# Takes a vcf file and a file with a list of clonesets. For each cloneset, it checks each snp to make sure everything in the cloneset has the same allele (or is unknown) and reports the chromosome, position, and genotypes for the cloneset.
# The format of the clonesets file is one line per cloneset with a csv separated list of sample names on each line.
# Basically, clones should have identical multilocus genotypes but they do not in RADseq data (even after cleaning the data). I want to find them. Next step will be fixing them.
# usage: ./find_nonidentical_clone_genotyes_in_vcf.py cloneset_file.csv vcf_file.vcf

import sys

clonesets = [] # List of clonesets. List of lists of strings (samplenames)
sample_indices = {} # Key = sample name, value = index within the vcf data

# Read the clonesets file
with open(sys.argv[1]) as clonesets_file:
    for line in clonesets_file:
        cloneset = line.strip().split(",")
        clonesets.append(cloneset)
        for sample in cloneset:
            sample_indices[sample] = 0 # Placeholder. We won't know the index til we get to the vcf file.

# Read the vcf file and check each locus
str_strings = [] # list of genotype strings for each sample--one element for each sample, in the same order that they are in the vcf.
with open(sys.argv[2]) as vcf_file:
    for line in vcf_file:
        if line[0:2] != "##": # skip the header lines
            elements = line.strip().split("\t")
            if elements[0] == "#CHROM": # Line with the sample names
                x = 0 #counter to step through the samples
                for sample_name in elements[9:]:
                    if sample_name in sample_indices.keys():
                        sample_indices[sample_name] = x
                    x += 1
            else: # Data line with sample_genotypes
                genotypes = elements[9:]
                for cloneset in clonesets:
                    cloneset_genotypes = []
                    sample_genotypes_string = ""
                    for sample in cloneset:
                        sample_genotype = genotypes[sample_indices[sample]][0:3]
                        sample_genotypes_string += sample_genotype + ","
                        if sample_genotype != "./." and sample_genotype not in cloneset_genotypes:
                            cloneset_genotypes.append(sample_genotype)
                    if len(cloneset_genotypes) > 1:
                        output_string = elements[0] + "," + elements[1]
                        for clone in cloneset:
                            output_string += "," + clone
                        output_string += "," + sample_genotypes_string
                        print(output_string)
