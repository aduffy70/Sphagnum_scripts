#! /usr/bin/python3

# classifycomparisons.py
# Given a sample attributes table, make a list of pairwise comparisons between every two samples of a given species and determine whether each comparison is between 2 of the same genotype, 2 of the same collection but different genotypes, or two of the same site but different collections.
# It is important that the sample names in the table are sorted alphabetically because that will put the comparisons in the same order as the distances in the R distobj that we are going to compare these to.
# usage: ./classifycomparisons.py sample_attributes_table.csv species_name

import sys
import csv

species = sys.argv[2]

samplenames = []
samples = []
collections = []
sites = []
genotypes = []


with open(sys.argv[1]) as attributes_file:
    sample_counter = 0
    is_firstline = True
    csv_data = csv.reader(attributes_file)
    for line in csv_data:
        if is_firstline: # skip the header
            is_firstline = False
        else:
            if line[3] == species:
                samplenames.append(line[1])
                samples.append(line[15]) #The unique sample identier (must be exactly the same for duplicates)
                collections.append(line[9]) # The collection name/number
                sites.append(line[8]) # The site identifier
                genotypes.append(line[2]) # The genotype identifier.
                sample_counter += 1

for x in range(0, sample_counter):
    for y in range(x+1,sample_counter):
        if samples[x] == samples[y]:
            print(",".join((samplenames[x], samplenames[y], "Replicates")))
        elif genotypes[x] == genotypes[y]:
            print(",".join((samplenames[x], samplenames[y], "Within genotype")))
        elif collections[x] == collections[y]:
            print(",".join((samplenames[x], samplenames[y], "Within collection")))
        elif sites[x] == sites[y]:
            print(",".join((samplenames[x], samplenames[y], "Within site")))
        else:
            print(",".join((samplenames[x], samplenames[y], "Between sites")))
