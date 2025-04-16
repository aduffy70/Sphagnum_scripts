#! /usr/bin/python3

# find_diagnostic_snps_from_vcf.py
# Takes a vcf or uvcf file and a csv file with samplenames and a column indicating which group each sample belongs to (samplename in 1st column, groupname in 2nd column, other columns ignored), and the names of two groups. Outputs a count of how many loci are diagnostic of the two groups and a table of the locus names and positions in the genome. We want to know how many snps are fixed between groups and have a list we can use to see what genes those snps are located within.
# To be diagnostic a snp needs to be:
#    present in >=50% of the samples in each group
#    not share any alleles between groups (it doesn't necessarily need to be fixed in both groups. If one group is always A or T and the other group is always C or G that is still diagnostic)
# I wrote this for haploids. You can use it on diploids but it is looking for diagnostic snps, not diagnostic genotypes (if one group is always AA and the other group is always Aa that is a diagnostic genotype but not a diagnostic snp).

# usage: ./find_diagnostic_snps_from_vcf.py vcf_file.vcf groups_csv_file.csv group0_name group1_name

import sys

group0_name = sys.argv[3]
group1_name = sys.argv[4]
minimum_coverage = 0.5 # we must have data for at least 50% of the samples in each group. If you want a different cutoff, set it here.

# Get group assignments for samples
group0_samplenames = []
group1_samplenames = []
with open(sys.argv[2]) as groups_file:
    is_headerline = True
    for line in groups_file:
        if is_headerline: # skip the header line
            is_headerline = False
        else:
            elements = line.strip().split(",")
            samplename = elements[0]
            #print(elements[0])
            groupname = elements[1]
            if groupname == group0_name:
                group0_samplenames.append(samplename)
            if groupname == group1_name:
                group1_samplenames.append(samplename)
    group0_size = len(group0_samplenames)
    group1_size = len(group1_samplenames)
#print(str(group0_size))
#print(str(group1_size))

total_loci_count = 0
below_mincov_count = 0
not_diagnostic_count = 0
diagnostic_count = 0

# Read the vcf file, calculate coverage, and find diagnostic snps
vcf_samplenames = [] # List of samplenames in the vcf file, in the same order as the genotype data
with open(sys.argv[1]) as vcf_file:
    for line in vcf_file:
        #print(line[0:2])
        if line[0:2] != "##": # skip the header lines
            elements = line.strip().split()
            #print(elements)
            if elements[0] == "#CHROM": # Line with the sample names
                vcf_samplenames = elements[9:]
                vcf_samplecount = len(vcf_samplenames)
            else: # Data line with sample_genotypes
                total_loci_count += 1
                chromosome = elements[0]
                position = elements[1]
                id = elements[2]
                #print()
                #print(chromosome, position)
                genotype_strings = elements[9:]
                group0_alleles = [] # list of alleles present in group0 samples
                group1_alleles = [] # list of alleles present in group1 samples
                group0_coverage = 0 # track the number of group0 samples with data
                group1_coverage = 0 # track the number of group0 samples with data
                for x in range(0, vcf_samplecount):
                    if vcf_samplenames[x] in group0_samplenames:
                        #print(vcf_samplenames[x],group0_name, end=" ")
                        allele0 = genotype_strings[x][0] # first allele of the genotype
                        allele1 = genotype_strings[x][2] # second allele of the genotype
                        if allele0 != "." or allele1 != ".": # we have data
                            group0_coverage += 1
                            #print(allele0, allele1)
                            if allele0 != "." and allele0 not in group0_alleles:
                                group0_alleles.append(allele0)
                            if allele1 != "." and allele1 not in group0_alleles:
                                group0_alleles.append(allele1)
                        #else:
                            #print("-")
                    elif vcf_samplenames[x] in group1_samplenames:
                        #print(vcf_samplenames[x],group1_name, end=" ")
                        allele0 = genotype_strings[x][0] # first allele of the genotype
                        allele1 = genotype_strings[x][2] # second allele of the genotype
                        if allele0 != "." or allele1 != ".": # we have data
                            group1_coverage += 1
                            #print(allele0, allele1)
                            if allele0 != "." and allele0 not in group1_alleles:
                                group1_alleles.append(allele0)
                            if allele1 != "." and allele1 not in group1_alleles:
                                group1_alleles.append(allele1)
                        #else:
                            #print("-")
                if group0_coverage / float(group0_size) >= minimum_coverage and group1_coverage / float(group1_size) >= minimum_coverage: # It meets the minimum coverage level for both groups
                    is_diagnostic = True
                    for allele in group0_alleles:
                        if allele in group1_alleles: # the allele isn't diagnostic
                            is_diagnostic = False
                    if is_diagnostic:
                        #print(group0_coverage, group1_coverage, chromosome, position, id)
                        print(chromosome, position, id)
                        diagnostic_count += 1
                    else:
                        #print(group0_coverage, group1_coverage, "Not diagnostic")
                        not_diagnostic_count += 1
                else:
                    #print(group0_coverage, group1_coverage, "Under_depth")
                    below_mincov_count += 1
print(group0_name, group0_size, file=sys.stderr)
print(group1_name, group1_size, file=sys.stderr)
print("loci_total:", str(total_loci_count), file=sys.stderr)
print("loci_below_min_coverage:", str(below_mincov_count), file=sys.stderr)
print("loci_not_diagnostic:", str(not_diagnostic_count), file=sys.stderr)
print("loci_diagnostic:", str(diagnostic_count), file=sys.stderr)
