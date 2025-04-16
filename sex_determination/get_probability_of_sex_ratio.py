#! /usr/bin/python3

# get_probability_of_sex_ratio.py
# Takes a count of males and females and a desired number of simulations and runs simulations to
# determine how often we get a sampled sex ratio as extreme or more extreme that the one observed
# when the true sex ratio is 1:1.
# Basically, I have 7 males and 1 females or 8 males and zero females and I want to know how likely
# it would be to get this result if the actual sex ratio is 1:1. How large a sample size to I need
# to be confident the sex ratio differs from 1:1?
# usage: ./get_probability_of_sex_ratio.py male_count female_count simulation_count

import sys
import random

# Read in the pairwise distances table
observed_males = int(sys.argv[1])
observed_females = int(sys.argv[2])
population_male_proportion = 0.5
simulations_count = int(sys.argv[3])
samples = observed_males + observed_females
simulated_ratios = []

for simulation in range(0, simulations_count):
    simulated_males = 0
    simulated_females = 0
    for sample in range(0, samples):
         if random.random() < population_male_proportion:
             simulated_males += 1
         else:
            simulated_females += 1
    simulated_ratios.append(simulated_males / float(samples))
#print(simulated_ratios)

extreme_count = 0
for ratio in simulated_ratios:
    if observed_males < observed_females: # use the left tail
        if ratio <= observed_males / float(samples):
            extreme_count += 1
    else: # use the right tail
        if ratio >= observed_males / float(samples):
            extreme_count += 1
print("P-value: " + str(extreme_count / float(simulations_count)))
