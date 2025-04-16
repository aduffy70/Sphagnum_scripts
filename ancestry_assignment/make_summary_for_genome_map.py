#! /usr/bin/python3

# make_summary_for_genome_map.py
# Takes a table of RASPberry sample numbers and species name, along with my 19 combined RASPberry
# AllInd files (the path and names are hardcoded, not command-line parameters) and makes a summary
# table I can use to make a single genome map in R (rather than the 19 separate chromosome maps
# I currently have). Output is csv, one line per SNP with:
#     chromosome number, snp name, snp position in bp, count of diabolicum samples introgressed with magniae alleles, count of magniae samples introgressed with diabolicum alleles
# usage: ./make_summary_for_genome_map.py sample_species_table.csv > summary_for_genome_map.csv

import sys

# Read the sample species table
sample_spp = {} # key = RASPberry sample number, value = species of the sample
with open(sys.argv[1]) as spp_file:
    for line in spp_file:
        elements = line.strip().split(",")
        if elements[0] != "raspberry_number": # skipping the header row
            if len(elements) > 0:
                sample_spp[elements[0]] = elements[1]

print("chrom,snp,position,count_of_introgressed_diabolicum,count_of_introgressed_magniae") # the header row

chromosomes = {} # key = snp_name, value = chromosome_number of the snp
positions = {} # key = snp_name, value = position in bp of the snp
diab_intr_counts = {} # key = snp_name, value = count of diabolicum samples introgressed with magniae alleles at that snp
magn_intr_counts = {} # key = snp_name, value = count of magniae samples introgressed with diabolicum alleles at that snp
for chromosome_number in range(1,20):# The current chromosome
    filename = "../chr" + str(chromosome_number) + "_paramId_1_AllInd.txt"
    with open(filename) as allind_file:
        for line in allind_file:
            elements = line.strip().split()
            if len(elements) > 0 and elements[1] != "snp": # skipping the header row
                sample_number = elements[0]
                snp_name = elements[1]
                snp_position = int(elements[2])
                prob_diab = float(elements[9])
                prob_magn = float(elements[11])
                spp = sample_spp[sample_number]
                if snp_name not in chromosomes.keys(): # this is a snp we haven't seen before
                    chromosomes[snp_name] = chromosome_number
                    positions[snp_name] = snp_position
                    diab_intr_counts[snp_name] = 0
                    magn_intr_counts[snp_name] = 0
                if prob_diab > 0.5: # it is a diabolicum allele
                    if spp == "magniae": # magniae sample with an introgressed diabolicum allele
                        magn_intr_counts[snp_name] += 1
                elif prob_magn > 0.5:
                    if spp == "diabolicum": # diabolicum sample with an introgressed magniae allele
                        diab_intr_counts[snp_name] += 1

for snp_name in chromosomes.keys():
    print("%s,%s,%s,%s,%s" % (chromosomes[snp_name], snp_name, str(positions[snp_name]), str(diab_intr_counts[snp_name]), str(magn_intr_counts[snp_name])))
    
            
