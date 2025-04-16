#! /usr/bin/python3

# rarify_genotypes.py
# Given a list of genotypes, sample as specified number of all combinations of a specified number
# of them, calculate the number of unique genotypes in each combination, calculate a mean number
# of genotypes and the standard deviation.
# Basically, poppr in R rarifies genotypes down to 10 samples but I want to rarify down to 4 since
# my smallest populations have 4 samples. And I can't do the exact calculations when there are 30+ genotypes involved, so I need to estimate by sampling.
# usage: ./rarify_genotypes.py integer_number_of_simulations integer_of_samples_to_rarify_down_to csv,genotypes,with,no,spaces

import sys
import random
from statistics import mean, stdev

simulations_count = int(sys.argv[1])
rarified_count = int(sys.argv[2])
genotypes = sys.argv[3].strip().split(",")
genotype_counts = [] # list of genotype counts for each rarified subset

#print(genotypes)

for x in range(0, simulations_count):
    this_sample = random.sample(genotypes, rarified_count)
#    print(this_sample)
    genotype_count = len(set(this_sample))
    genotype_counts.append(genotype_count)
#print(genotype_counts)
print("Mean " + str(mean(genotype_counts)))
print("Stdev " + str(stdev(genotype_counts)))
