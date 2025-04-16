#! /usr/bin/python3

# make_fake_clumpp_outfile_from_structure_output.py
# Takes a folder of structure output files (_f) (where the population numbers are the same 
# across replicate runs because we used a training sample set with preset group assignments),
# and makes a file in the same format as a clump outfile.
# Expects preset populations to be 1 through n (number of preset populations) for the
# training samples with fixed population assignments and to be 0 for the samples with 
# inferred ancestry. 
# Basically, I ran structure using a training set on a single value of K and I want to combine
# the 10 replicate runs. I don't need clumpp because the group numbers are already assigned
# and are the same across runs. And I can't run clumpp anyway because it expects the ind file
# output from structureharvester, and structureharvester chokes on structure output with preset
# population info. So I am manually averaging the population assignments across replicate runs
# and generating a file to match the format of clumpp outfiles. Then I can make plots using my 
# usual R code.

# usage: ./make_clumpp_outfile_from_structure_output.py path_to_stucture_output_folder > faked_clumpp_outfile.outfile

import sys
import os

probability_sums = {} # key = samplenumber from structure, value = lists of sums of group probabilities
missing_data_strings = {} # Key = sample number from structure, value = the missing data percentages. We will get them from the first file so we can include them in the output. 
file_count = 0 # Track how many files we process so we have the denominator for the averages

filepath = sys.argv[1]
is_firstfile = True
for filename in os.listdir(filepath):
    if filename.endswith('_f'):
        file_count += 1
        full_filename = filepath + "/" + filename
        with open(full_filename) as f_file:
            is_probability_block = False # we need to find the block of probability data
            population_count = 0 
            for line in f_file:
                elements = line.strip().split()
                if len(elements) > 0:
                    if elements[0] == "Label":
                        is_probability_block = True # We found the start of the probability block
                    elif len(elements) == 3 and elements[1] == "populations" and elements[2] == "assumed": # This is the line with the population count
                        population_count = int(elements[0])
                    elif is_probability_block: # This is a probability line we need to process
                        #print(elements)
                        population = int(elements[3])
                        samplenumber = int(elements[0])
                        missing_data = elements[2]
                        if population == 0:
                            probabilities = []
                            for x in range(5,5+population_count):
                                probabilities.append(float(elements[x]))
                        else:
                            probabilities = [0.0] * population_count
                            probabilities[population - 1] = 1.0
                        if is_firstfile:
                            probability_sums[samplenumber] = probabilities
                            missing_data_strings[samplenumber] = missing_data
                        else:
                            for x in range(0, population_count):
                                probability_sums[samplenumber][x] += probabilities[x]
                elif is_probability_block: # This is the blank line at the end of the block
                    is_probability_block = False
            is_firstfile = False
for sample in probability_sums.keys():
    means = []
    for prob_sum in probability_sums[sample]:
        means.append(str(round(prob_sum / float(file_count), 3)))
    means_string = "\t".join(means)
    print("%s\t%s\t%s\t1\t:\t%s" % (str(sample), str(sample), missing_data_strings[sample], means_string))
            
            
            
            
