#! /usr/bin/python2

# extract_locus_positions_from_vcf.py
# Takes a vcf file from ipyrad and extracts the positions of each locus in csv format. I have str files generated from my vcfs that I am using for other analyses. Those str files don't contain locus position info but the loci in those files are in the same order as the original vcf file so I can extract the locus positions from the vcf and re-associate it with the str loci. Ouput is number of the locus in the vcf file (starting with 1), chromosome, base position within chromosome, snp_name, reference base, and alternate base
# usage: ./extract_locus_positions_from_vcf.py vcf_file.vcf > locus_positions_file.csv

import sys

# Read the vcf file and filter it.
with open(sys.argv[1]) as vcf_file:
    locus_count = 1
    print("order_in_vcf,chromosome,position,snp_name,ref_base,alt_base")
    for line in vcf_file:
        if line[0] != "#": # This is a data line
            elements = line.split()
            print(str(locus_count) + "," + elements[0] + "," + elements[1] + "," + elements[2] + "," + elements[3] + "," + elements[4])
            locus_count += 1
