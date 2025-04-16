#! /usr/bin/python3

# insilico_admix_str_samples.py
# Takes a haploid str file and admixes two of the samples at a specified level (1-99%)
# and with a specified level of missing data (0-99%). Outputs a str format line that
# can be concatenated to an existing str file. The admix % is the percent from sample1.
# Values will be approximate because we are specifying a probability, not an
# absolute percentage. Also missing data is an upper bound because the samples being
# admixed may already have missing data, which can be included if their allele for
# a locus is selected. We will include the actual percentages in the new samplename.
# Basically, I want to create some fake samples with known levels of admixture and
# missing data so I can see how ADMIXTURE and STRUCTURE deal with them.
# usage: ./insilico_admix_str_samples str_file.str admixture_percent_integer missing_data_percent_integer new_sample_name > new_insilico_admixed_sample.str

import sys
from random import randint

sample1 = "SB5525"
sample2 = "SB4940"

admix_percent = int(sys.argv[2])
missing_percent = int(sys.argv[3])

sample1_alleles = []
sample2_alleles = []
admixed_alleles = []
sample1_allele_count = 0 # Keep track of how many alleles we got from sample1
sample2_allele_count = 0 # How many alleles we got from sample 2
total_allele_count = 0 # How many total alleles there are
missing_allele_count = 0 # How many alleles are missing data (-9)

# Read the str file
with open(sys.argv[1]) as str_file:
    for line in str_file:
        elements = line.strip().split()
        if elements[0] == sample1:
            sample1_alleles = elements[1:]
        if elements[0] == sample2:
            sample2_alleles = elements[1:]
for allele in range(0,len(sample1_alleles)):
    if randint(0,99) < admix_percent: # make it sample1's allele
        chosen_genome = "sample1"
    else:
        chosen_genome = "sample2"
    if randint(0,99) < missing_percent: # make it missing missing_data
        admixed_alleles.append("-9")
        missing_allele_count += 1
    elif chosen_genome == "sample1":
        admixed_alleles.append(sample1_alleles[allele])
        if sample1_alleles[allele] != "-9":
            sample1_allele_count += 1
        else:
            missing_allele_count += 1
    else:
        admixed_alleles.append(sample2_alleles[allele])
        if sample2_alleles[allele] != "-9":
            sample2_allele_count += 1
        else:
            missing_allele_count += 1
    total_allele_count += 1

true_missing_percent = round(100 * (missing_allele_count / float(total_allele_count)), 1)
true_admix_percent = round(100 * (sample1_allele_count / float(sample1_allele_count + sample2_allele_count)),1)

new_str_line = "admixed_" + str(true_admix_percent) + "_missing_" + str(true_missing_percent) + "\t" + "\t".join(admixed_alleles)
print(new_str_line)
