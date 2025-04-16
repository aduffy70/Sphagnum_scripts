#! /usr/bin/python2

# get_percent_polymorphic_loci_from_vcf.py
# Takes a vcf file, a sample attributes table, and a column number from the table (counting from column 1) that contains the groupings we want to compare. For each group, calculates the percent of loci that are polymorphic (there is more than one genotype other than missing data)
# Basically, I want to know the number of polymorphic loci in each site or sex.
# usage: ./get_percent_polymorphic_loci_from_vcf.py vcf_file.vcf Sample_attributes_table.csv grouping_column_integer

import sys

grouping_column = int(sys.argv[3])
grouping_attributes = {} # Key = sample, value = group
group_indices = {} # Key = groupnames (of groups that have samples in the vcf file (the sample attributes table likely contains samples not in the vcf since the vcf is by species and the attributes table is for all samples) , value = list of vcf indices of the samples in the group
polymorphic_loci = {} # key = groupnames, value = count of polymorphic loci

# Read the Sample_attributes_table
with open(sys.argv[2]) as attributes_file:
    for line in attributes_file:
        elements = line.strip().split(",")
        sample_name = elements[0]
        group = elements[grouping_column - 1]
        grouping_attributes[sample_name] = group
#print(grouping_attributes)

# Read the vcf file and check each locus
locus_count = 0 # We will need to know the total number of loci
with open(sys.argv[1]) as vcf_file:
    for line in vcf_file:
        if line[0:2] != "##": # skip the header lines
            elements = line.strip().split("\t")
            if elements[0] == "#CHROM": # Line with the sample names
                x = 0 #counter to step through the samples
                for sample_name in elements[9:]:
                    group = grouping_attributes[sample_name]
                    if group in group_indices.keys():
                        group_indices[group].append(x)
                    else:
                        group_indices[group] = [x]
                        polymorphic_loci[group] = 0
                    x += 1
            else: # Data line with sample_genotypes
                genotypes = elements[9:]
                for group in group_indices.keys():
                    #print(group)
                    group_genotypes = [] # List of the non-missing data genotypes for this group
                    for index in group_indices[group]:
                        sample_genotype = genotypes[index][0:3]
                        if sample_genotype != "./." and sample_genotype not in group_genotypes:
                            group_genotypes.append(sample_genotype)
                    #print(group_genotypes)
                    if len(group_genotypes) > 1: #locus is polymorphic for this group
                        polymorphic_loci[group] += 1
                        #print("polymorphic ")
                    #else:
                        #print("not")
                locus_count += 1
                #print(polymorphic_loci)

for group in polymorphic_loci:
    print(group + " " + str(polymorphic_loci[group] / float(locus_count) * 100))
