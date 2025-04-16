#! /usr/bin/python2

# identify_genes_at_interesting_loci.py
# Takes a csv list of interesting loci (including chromosome and base position), and the Smagellanicum gene.gff annotation file and returns a list of which features in the annotation each interesting locus is located within.
# Basically, I have a list of RADseq snps associated with climate factors and I want to know if any of them are within genes or regulatory regions.
# usage: ./identify_genes_at_interesting_loci.py interesting_loci.csv Smagellanicum_521_v1.1.gene.gff3 > genes_at_interesting_loci.csv

import sys

climate_column = 0 # column number (starting with 0) in the locus file containing the climate variable for which the locus is interesting
name_column = 1 # column number (starting with 0) in the locus file containing the locus name
chromosome_column = 2 # column number (starting with 0) in the locus file containing the locus chromosome id
position_column = 3 # column number (starting with 0) in the locus file containing the locus base position

climate_variables = {} # key = locus_name, value = list of climate variables
chromosomes = {} # key = locus_name, value = chromosome
positions = {} # key = locus_name, value = position
containing_features = {} # key = locus_name, value = list of containing features

# Read the information about the loci
with open(sys.argv[1]) as locus_file:
    for line in locus_file:
        if line[0] != "#": # It is not a header line
            elements = line.strip().split(",")
            locus_name = elements[name_column]
            if locus_name not in climate_variables.keys():
                climate_variables[locus_name] = [elements[climate_column]]
                chromosomes[locus_name] = elements[chromosome_column]
                positions[locus_name] = int(elements[position_column])
                containing_features[locus_name] = []
            else:
                climate_variables[locus_name].append(elements[climate_column])
#for locus_name in climate_variables.keys():
#    print("%s %s %s %s" % (locus_name, chromosomes[locus_name], str(positions[locus_name]), ";".join(climate_variables[locus_name])))

# Read the annotation info
print("#feature,type,chromosome,start_pos,end_pos,radseq_locus,chromosome,position,associated_climate_variables")
loci_in_features = [] # Keep a list of which loci are found within at least one feature
with open(sys.argv[2]) as gff_file:
    for line in gff_file:
        if line[0] != "#": # It is not a header line
            elements = line.strip().split()
            chromosome = elements[0]
            type = elements[2]
            start_pos = int(elements[3])
            end_pos = int(elements[4])
            id = elements[8].split(";")[0].split("=")[1]
            # Step through the loci and see if any are contained within this feature
            for locus_name in chromosomes.keys():
                if chromosome == chromosomes[locus_name] and start_pos <= positions[locus_name] and end_pos >= positions[locus_name]: # The locus is within the feature
                    print("%s,%s,%s,%s,%s,%s,%s,%s,%s" % (id, type, chromosome, str(start_pos), str(end_pos), locus_name, chromosome, positions[locus_name], ";".join(climate_variables[locus_name])))
                    if locus_name not in loci_in_features:
                        loci_in_features.append(locus_name)
print("Loci in features:")
print("\n".join(loci_in_features))
print(str(len(loci_in_features)), str(len(chromosomes.keys())))
