#! /usr/bin/python2

# filter_vcf_for_exactly_2_allele_loci.py
# Takes a vcf file and removes snps that don't have exactly 2 alleles (missing data doesn't count as another allele).

# usage: ./filter_vcf_for_exactly_2_allele_loci.py vcf_file.vcf > filtered_vcf.vcf

import sys

# Read the vcf file and only keep loci with exactly 2 alleles.
with open(sys.argv[1]) as vcf_file:
    for line in vcf_file:
        if line[0] == "#": # Header line. Print as-is
            print line.strip()
        else: # Data line to process
            elements = line.strip().split()
            genotypes = elements[9:] # Just the genotype strings
            alleles = [] # Keep track of the different alleles for this snp
            for genotype in genotypes:
                allele = genotype[0] # first allele of the genotype
                if allele != "." and allele not in alleles:
                    alleles.append(allele)
                allele = genotype[2] # second allele of the genotype
                if allele != "." and allele not in alleles:
                    alleles.append(allele)
            if len(alleles) == 2:
                print(line.strip())
          
           
