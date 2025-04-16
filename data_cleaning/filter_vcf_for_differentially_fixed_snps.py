#! /usr/bin/python2

# identify_differentially_fixed_snps_in_vcf.py
# Takes a vcf file, two lists of pure samples, a list of potentially admixed samples, and a minimum number of samples in each pure sample group that must have data and finds snps that are differentially fixed between two sets of samples.

# Output is a table of the differentially fixed snps, which snp each pure group has, and which 
# group's snp each admixed sample has (or "unknown" if the snp is missing or is different from both groups).

# To be considered differentially fixed, a snp needs to have only one allele (or missing data) in 
# every sample of one group and only one different allele (or missing data) in every sample of 
# the other group. This script was written with haploid samples in mind. It also needs to be
# present in at least the specified number of samples of each pure group.

# Examples:
# Sampleset1 alleles    Sampleset2 alleles   Differentially fixed?
#   A                       G                       Y
#   A,-                     G,-                     Y
#   A,G                     A                       N
#   A,G                     C                       N
#   A                       -                       N

# usage: 
# ./filter_vcf_for_differentially_fixed_snps.py vcf_file.vcf pure_sample_list1.txt pure_sample_list2.txt admixed_sample_list.txt minimum_data_integer > table_of_snps_and_diagnostic_alleles.csv


import sys

minimum_data = int(sys.argv[5])

# Read the lists of samples in each group
group1_samples = [] # List of samples in group1
group2_samples = [] # List of samples in group2
admix_samples = [] # List of potentially admixed samples
with open(sys.argv[2]) as group1_file:
    for line in group1_file:
        if line.strip():
            group1_samples.append(line.strip())
with open(sys.argv[3]) as group2_file:
    for line in group2_file:
        if line.strip():
            group2_samples.append(line.strip())      
with open(sys.argv[4]) as admix_group_file:
    for line in admix_group_file:
        if line.strip():
            admix_samples.append(line.strip())  

group1_indices = [] # A list of the indices of the group1 samples in the vcf file...so we know which indices of the genotypes to check
group2_indices = [] # A list of the indices of the group2 samples in the vcf file
admix_indices = [] # A list of the indices of the admix samples in the vcf file

# Read the vcf file and decide if each snp is differentially fixed
with open(sys.argv[1]) as vcf_file:
    for line in vcf_file:
        if line[0] == "#": # Header line.
            if line[1:6] == "CHROM": # this is the line with samplenames
                headerline = "chromosome,position,id,group1_allele,group2_allele"
                elements = line.strip().split()[9:] # just the sample names
                for index in range(0,len(elements)):
                    if elements[index] in group1_samples:
                        group1_indices.append(index)
                    if elements[index] in group2_samples:
                        group2_indices.append(index)
                    if elements[index] in admix_samples:
                        admix_indices.append(index)
                        headerline = headerline + "," + elements[index]
                print(headerline)
        else: # Data line to process
            elements = line.strip().split()
            genotypes = elements[9:] # Just the genotype strings
            group1_alleles = [] # Track the different group1 alleles at this snp
            group2_alleles = [] # Track the different group2 alleles at this snp
            base_order = [] # Keep track of which base is represented by 0, 1, 2, and 3 in the vcf format
            ref_base = elements[3]
            alt_bases = elements[4]
            base_order.append(ref_base)
            for base in alt_bases.split(","):
                base_order.append(base)
            group1_count = 0 # Keep track of how many samples in group1 have data for this snp 
            for index in group1_indices:
                allele = genotypes[index][0] # first allele in the genotype (assuming haploids here)
                if allele != ".":
                    group1_count += 1
                    if allele not in group1_alleles: # It is an allele we haven't seen in group1 yet
                        group1_alleles.append(allele)
            group2_count = 0
            for index in group2_indices:
                allele = genotypes[index][0] # first allele in the genotype (assuming haploids here)
                if allele != "." :
                    group2_count += 1
                    if allele not in group2_alleles: # It is an allele we haven't seen in group1 yet
                        group2_alleles.append(allele)
            if len(group1_alleles) == 1 and len(group2_alleles) == 1 and group1_alleles[0] != group2_alleles[0] and group1_count >= minimum_data and group2_count >= minimum_data: # The snp is differentially fixed
                chromosome = int(elements[0][2:])
                pos = elements[1]
                snpid = elements[2]
                group1_base = base_order[int(group1_alleles[0])]
                group2_base = base_order[int(group2_alleles[0])]
                outputline = str(chromosome) + "," + pos + "," + snpid + "," + group1_base + "," + group2_base
                for index in admix_indices:
                    allele = genotypes[index][0] # first allele in the genotype (assuming haploids here)
                    if allele == ".":
                        outputline = outputline + ",-" # Missing data
                    else:
                        admix_base = base_order[int(allele)]
                        if admix_base == group1_base:
                            outputline = outputline + ",1"
                        elif admix_base == group2_base:
                            outputline = outputline + ",2"
                        else:
                            outputline = outputline + ",?" # Allele doesn't match either group
                print(outputline)
                
                
                
          
           
