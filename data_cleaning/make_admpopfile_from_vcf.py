#! /usr/bin/python2

# make_admpopfile_from_vcf.py
# Takes a vcf file and list of admixed samples and generates a phased format admpop file.
# Expects all snps in the vcf to have EXACTLY two alleles including ONLY A, C, G, or T. Allows for missing data (-) in individual genotypes.
# RASPberry is expecting genotypes, and we have haploids so I to make the haploids look like homozygous diploids.

# Output format (tab delimited):
# SNP_name physical_map_position_bp Allele0_for_sample1 Allele1_for_sample1 Allele0_for_sample2 Allele1_for_sample2 ...
# RASPberry doesn't require the position (it can be any value) since it gets that from the bimfile, but I have it in the vcf so I included it. 

# usage: ./make_admpopfile_from_vcf.py vcf_file.vcf list_of_samples.txt > admpopfile.vcf


import sys

sample_names = []

with open(sys.argv[2]) as samples_file:
    for line in samples_file:
        if line.strip():
            sample_names.append(line.strip())

sample_indices = [] # A list of the indices of the samples of interest so we know which indices to grab genotypes from.
headerline = "ID\tposition" # Start the header row text. We will add the sample names to it.
# Read the vcf file and output one bim-format line per vcf snp line.
with open(sys.argv[1]) as vcf_file:
    for line in vcf_file:
        if line[0] == "#": # it is a header line
            if line[1:6] == "CHROM":  # this is the line with samplenames
                elements = line.strip().split()[9:] # just the sample names
                for sample in sample_names: #Add the indices of the pure samples to the sample_indices list in the same order that they are in the sample_names list
                    sample_indices.append(elements.index(sample))
                    headerline = headerline + "\t" + sample + "_0\t" + sample + "_1" 
                print(headerline)
        else: # It is a data line we need to process    
            elements = line.strip().split()
            locus = elements[2]
            position = elements[1]
            outputline = locus + "\t" + position + "\t"
            alleles = [] # List of alleles in order of how they are numbered in the vcf. We have to do it this way because sometimes there are 2+ alternative alleles listed in the vcf but only one is actually used in our samples (because we filtered for loci with exactly 2 alleles present in this sampleset) and we need to be able to get the right one.
            alleles.append(elements[3]) # The reference allele
            alt_alleles = elements[4].split(",") # the alternate allele or alleles
            for allele in alt_alleles:
                alleles.append(allele)
            genotypes = elements[9:]
            for index in sample_indices:
                if genotypes[index][0] == ".": # Missing data. Code alleles as "-"
                    allele = "-"
                else:
                    allele_digit = int(genotypes[index][0])
                    allele = alleles[allele_digit]
                outputline = outputline + "\t" + allele + "\t" + allele
            print(outputline)                

