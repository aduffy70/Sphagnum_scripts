#! /usr/bin/python2

# fix_nonidentical_clone_genotyes_in_vcf.py
# Takes a vcf file and a file with a list of clonesets. For each cloneset, it checks each snp to make sure everything in the cloneset has the same allele (or is unknown) and if not, replaces all the genotypes with missing data. If everything has the same allele (or is unknown) it replaces all the unknowns with that allele so all of them truly have the same multilocus genotype with the same missing data.
# The format of the clonesets file is one line per cloneset with a csv separated list of sample names on each line.
# Basically, clones should have identical multilocus genotypes but they do not in RADseq data (even after cleaning the data). I want to fix them and rather than trying to chose which is the genotype I am throwing them all away.
# usage: ./fix_nonidentical_clone_genotyes_in_vcf.py cloneset_file.csv vcf_file.vcf > fixed_vcf_file.vcf

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
        elements = line.strip().split("\t")
        if line[0:2] == "##": # the header lines
            print(line.strip()) # Print the header lines as-is.
        elif elements[0] == "#CHROM": # Line with the sample names. Get the sample names and print the line as-is.
            x = 0 #counter to step through the samples
            for sample_name in elements[9:]:
                if sample_name in sample_indices.keys():
                    sample_indices[sample_name] = x
                x += 1
            print(line.strip())
        else: # Data line with sample_genotypes. Find and fix any non-identical clonesets and print the line.
            genotypes = elements[9:]
            for cloneset in clonesets:
                cloneset_genotypes = []
                sample_genotypes_string = ""
                for sample in cloneset:
                    sample_genotype = genotypes[sample_indices[sample]][0:3]
                    sample_genotypes_string += sample_genotype + ","
                    if sample_genotype != "./." and sample_genotype not in cloneset_genotypes:
                        cloneset_genotypes.append(sample_genotype)
                if len(cloneset_genotypes) > 1: #There are mismatched genotypes. Make them all unknown
                    for sample in cloneset:
                        genotypes[sample_indices[sample]] = "./." + genotypes[sample_indices[sample]][3:]
                elif len(cloneset_genotypes) == 1: # There is only one genotype. Let's make ALL of them have that genotype (change the unknowns)
                    for sample in cloneset:
                        genotypes[sample_indices[sample]] = cloneset_genotypes[0] + genotypes[sample_indices[sample]][3:]
            print("\t".join(elements[0:9]) + "\t" + "\t".join(genotypes))
