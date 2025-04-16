#! /usr/bin/python2

# get_sample_coverage_from_vcf.py
# Takes a vcf file from ipyrad returns a csv table of how many snps are present in X samples and a csv table of how many loci each sample has.
# I am filtering genotypes and want to see how this is affecting missing data.
# usage: ./filter_vcf_for_cleaner_haploids.py vcf_file.vcf proportion_float > filtered_vcf.vcf

import sys

# Read the vcf file and generate counts for the tables
total_locus_count = 0
with open(sys.argv[1]) as vcf_file:
    for line in vcf_file:
        if line[0:2] != "##": # Ignore the header lines
            elements = line.strip().split()
            if elements[0] == "#CHROM": # It is the line with sample names
                sample_names = elements[9:] # list of sample names
                sample_count = len(sample_names)
                locus_counts_by_sample = [0] * sample_count # list of locus counts by sample
                locus_counts_with_X_samples = [0] * (sample_count + 1) # list of how many loci are present in 0, 1, 2, 3, etc samples.
            else: # it is a locus dataline with genotypes we need to process
                sample_count_for_this_locus = 0
                for x in range(0, sample_count):
                    current_genotype_string = elements[9 + x]
                    if current_genotype_string[0] != ".": # We have data for this sample
                        sample_count_for_this_locus += 1
                        locus_counts_by_sample[x] += 1
                total_locus_count += 1
                locus_counts_with_X_samples[sample_count_for_this_locus] += 1

# Output the tables

print("Locus(snp) counts by sample")
print("sample,loci")
for x in range(0, sample_count):
    print(sample_names[x] + "," + str(locus_counts_by_sample[x]))
print("Total," + str(total_locus_count))

print("\nLoci(snps) present in X samples")
print("X_samples,loci,loci_X_or_better,percent_sample_coverage")
for x in range(0, sample_count +1):
    print(str(x) + "," + str(locus_counts_with_X_samples[x]) + "," + str(sum(locus_counts_with_X_samples[x:])) + "," + str(round(x / float(sample_count) * 100,1)))
