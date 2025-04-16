#! /usr/bin/python3

# convert_str_to_ped.py
# I have a str file that I have filtered just the way I want it and need a ped version so I can compare structure and admixture outputs.
# usage: ./convert_str_to_ped.py str_file.str > new_ped_file.ped

import sys

# Read the str file
with open(sys.argv[1]) as str_file:
    for line in str_file:
        elements = line.strip().split()
        sample_name = elements[0]
        ped_string = sample_name + " " + sample_name + " 0 0 0 -9" # The sample name is displayed twice and the first 4 columns are required settings.
        for element in elements[1:]:
            if element == "-9":
                allele = "0"
            elif element == "0":
                allele = "2"
            elif element == "1":
                allele = "1"
            else:
                print("*******  Error!  *******")
            ped_string += " " + allele + " " + allele # Each genotype for these haploids is coded as if it were homozygous. We tell Admixture they are haploid so it can deal with it.
        print(ped_string)
