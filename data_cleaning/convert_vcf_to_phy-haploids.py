#! /usr/bin/python2

# convert_vcf_to_phy.py
# Takes a vcf file from ipyrad and writes the data in phylip format. Haploid data only!
# Basically, I have a vcf from ipyrad that I have filtered and manipulated and now I want
# a phy format file of this exact dataset.
# usage: ./convert_vcf_to_phy.py vcf_file.vcf > phylip_file.phy

import sys

# Read the vcf file and convert it
phy_strings = [] # list of genotype strings for each sample--one element for each sample, in the same order that they are in the vcf.
sample_names = [] # list of sample names in the same order they are in the vcf
locus_count = 0
with open(sys.argv[1]) as vcf_file:
    for line in vcf_file:
        if line[0:2] != "##": # skip the header lines
            elements = line.strip().split()
            if elements[0] == "#CHROM": # Line with the sample names
                for sample_name in elements[9:]:
                    sample_names.append(sample_name)
                    phy_strings.append("")
            else: # Data line with sample_genotypes
                alleles = [] # We need a list of the reference and alternative nucleotides for this snp
                alleles.append(elements[3]) # puts the reference allele as element 0 of the alleles list
                for alt_allele in elements[4].split(","):
                    alleles.append(alt_allele) # Puts the alternative alleles in order as elements 1, 2...
                x = 0 #counter to step through samples as we append the genotypes
                for genotype_string in elements[9:]:
                    allele = genotype_string[0]
                    if allele == ".":
                        allele_character = "N" #Use N's for missing data
                    else:
                        allele_character = alleles[int(allele)]
                    phy_strings[x] += allele_character
                    x += 1
                locus_count += 1
print(str(len(sample_names)) + " " + str(locus_count)) # Header line
name_field_size = len(max(sample_names, key=len)) + 2 # We need to pad the sample names with spaces to make them all the same length
for x in range(0, len(sample_names)):
    sample_name = sample_names[x]
    padding_needed = name_field_size - len(sample_name)
    padding = " " * padding_needed
    print(sample_name + padding + phy_strings[x])
