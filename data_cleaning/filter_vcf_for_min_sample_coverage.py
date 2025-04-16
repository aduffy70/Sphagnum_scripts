#! /usr/bin/python2

# filter_vcf_for_min_sample_coverage.py
# Takes a vcf file from ipyrad and only keeps snps where the minimum sample coverage meets or exceeds a specified number of samples.

# Since I am doing filtering post-ipyrad I need a script to do this step too.
# usage: ./filter_vcf_for_min_sample_coverage.py vcf_file.vcf min_samples_coverage_integer > filtered_vcf.vcf

import sys

# Read the vcf file and filter it
min_samples = int(sys.argv[2]) # minimums number of samples required to keep a snp
reference_sample_indices = [] # A list of indices of the reference samples we need to inspect
with open(sys.argv[1]) as vcf_file:
    for line in vcf_file:
        if line[0] == "#": # Print the header lines as is
            print(line.strip())
        else: # It is a dataline we need to process
            sample_count = 0
            elements = line.strip().split()
            for genotype_string in elements[9:]:
                genotype = genotype_string.split(":")[0]
                if genotype != "./.": # It is a good genotype (not missing data)--count it
                    sample_count += 1
            if sample_count >= min_samples: # SNP exceeds minimum sample coverage. Keep it
                print(line.strip())
