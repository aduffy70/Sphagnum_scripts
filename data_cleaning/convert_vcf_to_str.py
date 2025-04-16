#! /usr/bin/python2

# convert_vcf_to_str.py
# Takes a vcf file from ipyrad and writes the data in one-line per sample structure format
# in the chosen ploidy (specified from the command line as haploid=1 or diploid=2).
# Basically, I have a vcf from ipyrad that I have filtered and manipulated and now I want
# a str format file of this exact dataset. (I'm trying to compare STRUCTURE to ADMIXTURE
# on a set of different datasets)
# usage: ./convert_vcf_to_str.py vcf_file.vcf ploidy_integer > structure_file.str

import sys

# Read the vcf file and convert it
str_strings = [] # list of genotype strings for each sample--one element for each sample, in the same order that they are in the vcf.
ploidy = int(sys.argv[2]) # 1 for haploids, 2 for diploids
with open(sys.argv[1]) as vcf_file:
    for line in vcf_file:
        if line[0:1] != "##": # skip the header lines
            elements = line.strip().split()
            if elements[0] == "#CHROM": # Line with the sample names
                for sample_name in elements[9:]:
                    str_strings.append(sample_name)
                    sample_count = len(str_strings)
            else: # Data line with sample_genotypes
                x = 0 #counter to step through samples as we append the genotypes
                for genotype_string in elements[9:]:
                    if ploidy == 1: # haploid- we can get the genotype from just the first character
                        genotype = genotype_string[0]
                        if genotype == ".":
                            genotype = "-9" #Use -9's for missing data
                    else: # diploid- the genotype is the 1st + 3rd characters
                        genotype = genotype_string[0] + "\t" + genotype_string[2]
                        if genotype == ".\t.":
                            genotype = "-9\t-9" #Use -9's for missing data
                    str_strings[x] += "\t" + genotype
                    x += 1
for sample in str_strings:
    print sample
