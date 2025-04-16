#! /usr/bin/python

# find_identical_or_indistinguishable_genotypes.py
# Takes a csv with haploid microsat data (one row per sample) & identifies any samples that are:
#    identical: all alleles are the same
#    indistinguishable: all alleles that are present are the same but some alleles are missing in
#                       one sample and present in the other (missing = -9)
# Uses the first (0) column as the sample name and starts reading genotype data at the specified
# (0-base) column so I can ignore other info in the table.
# Outputs a table of all pairwise comparisons. I'm making ALL of the pairwise comparisons to
# make generating the table simpler and making it easier to read, even though that means I'm
# making every comparison twice (A vs B and B vs A). I know. So wasteful of computing time.
# If you have a header line (or other lines you want ignored), start it with a "#""

# usage: ./find_identical_or_indistinguishable_genotypes.py csv_file.csv column_number_where_genoptypes_start > table_of_identical_or_indistinguishable_sample_pairs.csv

import sys

# Read in the csv file
with open(sys.argv[1]) as csv_file:
    start_column = int(sys.argv[2])
    names = [] # list of sample names
    genotypes = [] # list of lists of alleles
    for line in csv_file:
        elements = line.strip().split(",")
        if elements[0][0] != "#": # Ingnore header or comment lines
            names.append(elements[0])
            genotypes.append(elements[start_column:])
    # pairwise comparisons between genotypes
    header_string = ""
    for name in names:
        header_string = header_string + "," + name
    print header_string
    for x in range(0, len(names)):
        table_string = names[x]
        for y in range(0, len(names)):
            if genotypes[x] == genotypes[y]: #identical
                if names[x] == names[y]: #comparing a sample to itself, so yes it is identical but no it is not interesting
                    table_string += ","
                else: #Two different samples that are identical
                    table_string += ",ident"
            else:
                is_indistinguishable = True
                for z in range(0,len(genotypes[x])):
                    if genotypes[x][z] != genotypes[y][z] and genotypes[x][z] != "-9" and genotypes[y][z] != "-9":
                        is_indistinguishable = False
                if is_indistinguishable:
                    table_string += ",indis"
                else:
                    table_string += ","
        print table_string
