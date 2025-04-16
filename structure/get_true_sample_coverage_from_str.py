#! /usr/bin/python2

# get_true_sample_coverage_from_str.py
# Takes a str (or ustr) file and outputs a csv table of how many loci have coverage in
# how many samples. Assumes missing data symbol = -9 and 1 line per sample, haploid data.
# Basically, I have ustr output from ipyrad for loci with some minimum level of sample
# coverage and I want to know how many of the SNPs actually had that level of coverage.
# Also useful when subsetting samples from a larger dataset to make sure we aren't
# introducing huge levels of missing data.
# usage: ./get_true_sample_coverage_from_str.py str_file.str > coverage_table.csv

import sys

sample_counts_by_locus = [] # List of samples with data for each locus
alleles_by_locus = [] # List of non-missing alleles for each locus so we can tell which loci are variable
is_first_sample = True
count_of_samples = 0 # Keep track of how many samples there are.

# Read the str data and keeps count of how many samples have non-missing data for each locus
with open(sys.argv[1]) as str_file:
    for line in str_file:
        elements = line.strip().split()
        locus_counter = 0
        #print elements[0]
        for locus in elements[1:]: #Step through the data for this sample, line by line
            if is_first_sample:
                if locus != "-9":
                    sample_counts_by_locus.append(1)
                    alleles_by_locus.append(locus)
                else:
                    sample_counts_by_locus.append(0)
                    alleles_by_locus.append("")
            else:
                if locus != "-9":
                    sample_counts_by_locus[locus_counter] += 1
                    if locus not in alleles_by_locus[locus_counter]: #An allele not seen yet at this locus
                        alleles_by_locus[locus_counter] += locus
            locus_counter += 1
        is_first_sample = False
        count_of_samples += 1

# Filter the loci to remove non-variable ones
sample_counts_by_variable_locus = []
non_variable_locus_count = 0 # Keep track of how many loci are non-variable
for x in range(0, len(sample_counts_by_locus)):
    if len(alleles_by_locus[x]) >= 2: # Locus has at least 2 alleles
        sample_counts_by_variable_locus.append(sample_counts_by_locus[x])
    else:
        non_variable_locus_count += 1

print

# Output the table
print "non-variable_loci," + str(non_variable_locus_count)
print ""
print "sample_coverage_level,number_of_loci"
for x in range(count_of_samples,-1,-1):
    loci_with_x_samples = sample_counts_by_variable_locus.count(x)
    print str(x) + "," + str(loci_with_x_samples)
