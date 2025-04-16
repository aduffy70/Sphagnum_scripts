#! /usr/bin/python3

# compare_pairwise_str_samples.py
# Takes a str file (one line per sample) and two sample names and outputs the number total number of bases in the str alignment, the number of bases where both samples have data (not missing) and the number of bases where both samples do not share the same base. Note- if used on diploid data (or haploids coded as diploids) all counts will be doubled.
# Basically, I want to know how many bases are actually different between two samples.
# usage: ./compare_pairwise_str_samples.p sample1 sample2

import sys

sample1_name = sys.argv[2]
sample2_name = sys.argv[3]
sample1_data = [] # List of the alleles in sample1
sample2_data = [] # list of the alleles in sample2
nonmissing_bases = 0 # Count of bases with data for both samples
mismatched_bases = 0 # Count of bases where both samples have data and the bases match

# Read the str file and grab the two lines for the two samples
with open(sys.argv[1]) as str_file:
    for line in str_file:
        elements = line.strip().split()
        if elements[0] == sample1_name:
            sample1_data = elements[1:]
        elif elements[0] == sample2_name:
            sample2_data = elements[1:]

total_bases = len(sample1_data)
print(str(total_bases))
print(str(len(sample1_data))) # both should have the same length
for x in range(0,total_bases):
    #print(sample1_data[x] + " " + sample2_data[x])
    if sample1_data[x] != "-9" and sample2_data[x] != "-9":
        nonmissing_bases += 1
        #print("nonmissing")
        if sample1_data[x] != sample2_data[x]:
            mismatched_bases += 1
            #print("mismatch")
        

print("Total: " + str(total_bases))
print("Non-missing: " + str(nonmissing_bases))
print("Mismatched: " + str(mismatched_bases))

