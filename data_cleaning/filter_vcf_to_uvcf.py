#! /usr/bin/python2

# filter_vcf_to_uvcf.py
# Takes a vcf file from ipyrad and keeps one position per radseq locus. Before picking
# a position to represent the locus, it drops positions with all missing data or no
# variation. It keeps the position with the least missing data (or if there is a tie,
# it keeps the first position tied for least missing data).
# Also filters for a specified minumum sample coverage level (integer number).
# This should work on haploids or diploids but I'm only testing on haploids now.
# Basically, I want to be able to run STRUCTURE and ADMIXTURE on the exact same loci
# but I can't find a way to get from the ipyrad ustr output to the bed format needed by
# ADMIXTURE. I can get from vcf to bed and vcf to str but I need this script to get from
# vcf to a vcf with one snp per locus.
# usage: ./filter_vcf_to_uvcf.py vcf_file.vcf min_coverage > filtered_vcf_file.u.vcf

import sys

# Read the vcf file and filter it.
min_coverage = int(sys.argv[2])
is_first_locus = True
previous_locus = ""
best_position_data = "" # Data line for the position with the least missing data
best_position_quality = 0 # Number of samples with data at the best position
with open(sys.argv[1]) as vcf_file:
    for line in vcf_file:
        if line[0] == "#": # header line. Output as is.
            print line.strip()
        else: # Data line for a position. Let's evaluate it.
            current_position_data = line.strip()
            elements = line.split()
            current_locus = elements[2].split("_")[0] # The "locus" part of "locus_position"
            if current_locus != previous_locus: # starting a new locus
                if is_first_locus:
                    is_first_locus = False
                else: # Process the previous locus
                    if best_position_data != "" and best_position_quality >= min_coverage:
                        print best_position_data
                    previous_locus = current_locus
                    best_position_data = ""
                    best_position_quality = 0
            position_quality = 0 # count of samples with data for this position
            genotypes = [] # list of genotypes present for this position
            sample_genotypes = elements[9:]
            for sample in sample_genotypes:
                genotype = sample.split(":")[0]
                if genotype != "./.": # not missing data
                    position_quality += 1
                    if genotype not in genotypes:
                        genotypes.append(genotype)
            #print elements[2], str(position_quality), genotypes #TESTING
            alt_alleles_length = len(elements[4]) #Check how long the alternative alleles string is. If there is more than one alternative allele we are going to drop the snp since plink is going to drop it from the admixture dataset later and this will let us keep out structure and admixture datasets identical
            if position_quality > best_position_quality and len(genotypes) > 1 and alt_alleles_length == 1: #This position is variable, has only 2 alleles, and has better sample coverage than any previous snps from this locus. Best yet!
                best_position_quality = position_quality
                best_position_data = current_position_data
                #print "best" # TESTING
