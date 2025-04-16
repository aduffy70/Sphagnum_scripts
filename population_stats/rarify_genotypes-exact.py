#! /usr/bin/python3

# rarify_genotypes.py
# Given a list of genotypes, get all combinations of a specified number of them, calculate
# the number of unique genotypes in each combination, calculate a mean number of genotypes and
# the standard error.
# Basically, poppr in R rarifies genotypes down to 10 samples but I want to rarify down to 4 since
# my smallest populations have 4 samples.
# usage: ./rarify_genotypes.py integer_of_samples_to_rarify_down_to csv,genotypes,with,no,spaces

import sys
from itertools import combinations
from statistics import mean, stdev

rarified_count = int(sys.argv[1])
genotypes = sys.argv[2].strip().split(",")
genotype_counts = [] # list of genotype counts for each rarified subset

#print(genotypes)

for subset in combinations(genotypes, rarified_count):
    genotype_count = len(set(subset))
    genotype_counts.append(genotype_count)
#print(genotype_counts)
print("Mean " + str(mean(genotype_counts)))
print("Stdev " + str(stdev(genotype_counts)))
