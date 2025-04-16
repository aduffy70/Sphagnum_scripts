#! /usr/bin/python3

# make_summary_for_block_sizes-max.py
# Takes a table of RASPberry sample numbers and species name, along with my 19 combined RASPberry
# AllInd files (the path and names are hardcoded, not command-line parameters) and makes a summary
# table of the counts and sizes of contiguous blocks of introgressed SNPs from each species. Output is csv, one line per sample with:
#     sample name, number of undetermined SNPs, number of introgressed SNPs, total SNPs, number of blocks, minimum block size, maximum block size, mean block size, standard deviation of block sizes
# This version is based on maximum supported block sizes (the distance from the last non-introgressed allele before a block to the first non-introgressed allele after a block, counting undetermined alleles amongst introgressed blocks as introgressed). This means the estimates of minimum block size are conservative estimates (i.e., the true minimum block size is probably not larger than the estimate).

# usage: ./make_summary_for_block_sizes-max.py sample_species_table.csv > block_counts_and_sizes-max.csv

import sys
import statistics

# Read the sample species table
sample_spp = {} # key = RASPberry sample number, value = species of the sample
sample_names = {} # key = RASPberry sample number, value = name of the sample
with open(sys.argv[1]) as spp_file:
    for line in spp_file:
        elements = line.strip().split(",")
        if elements[0] != "raspberry_number": # skipping the header row
            if len(elements) > 0:
                sample_spp[elements[0]] = elements[1]
                sample_names[elements[0]] = elements[2]
print("sample,undetermined,introgressed,total,block_count,min_block,max_block,mean_block,stdev")

sample_blocks = {} # key = sample_name, value = list of introgressed block_sizes
sample_undetermined = {} # key = sample_name, value = undetermined_snps_count
sample_introgressed = {} # key = sample_name, value = introgressed_snps_count
sample_total_snps = {} # key = sample_name, value = total_snps_count
current_sample_name = "" # Keep track of which sample we are processing
current_chromosome = 0 # Keep track of which sample we are processing
is_a_block = False # Keep track of whether we are in a block of contiguous introgressed snps
current_block_start = 0 # keep track of where the current block started
current_block_end = 0 # keep track of where the current block ends

for chromosome_number in range(1,20):# The current chromosome
    filename = "../chr" + str(chromosome_number) + "_paramId_1_AllInd.txt"
    with open(filename) as allind_file:
        for line in allind_file:
            elements = line.strip().split()
            if len(elements) > 0 and elements[1] != "snp": # skipping the header row
                sample_name = sample_names[elements[0]]
                spp = sample_spp[elements[0]]
                snp_position = int(elements[2])
                prob_diab = float(elements[9])
                prob_magn = float(elements[11])
                if prob_diab > 0.5: # it is a diabolicum allele
                    if spp == "magniae": # magniae sample with an introgressed diabolicum allele
                        snp_type = "introgressed"
                    else: # diabolicum sample with a diabolicum allele
                        snp_type = "not introgressed"
                elif prob_magn > 0.5: # It is a magniae allele
                    if spp == "diabolicum": # diabolicum sample with an introgressed magniae allele
                        snp_type = "introgressed"
                    else: # magniae sample with a magniae allele
                        snp_type = "not introgressed"
                else: # undetermined allele
                    snp_type = "undetermined"
                if sample_name != current_sample_name: # starting into a new sample
                    if is_a_block: # We ended the sample in a block
                        block_size = current_block_end - current_block_start - 1
                        if current_sample_name in sample_blocks.keys():
                            sample_blocks[current_sample_name].append(block_size)
                        else:
                            sample_blocks[current_sample_name] = [block_size]
                        is_a_block = False
                    current_block_start = 0
                    current_block_end = 0
                    current_sample_name = sample_name
                if snp_type == "introgressed":
                    if sample_name in sample_introgressed.keys():
                        sample_introgressed[sample_name] += 1
                    else:
                        sample_introgressed[sample_name] = 1
                    if not is_a_block: 
                        is_a_block = True
                    current_block_end = snp_position
                elif snp_type == "undetermined":
                    if sample_name in sample_undetermined.keys():
                        sample_undetermined[sample_name] += 1
                    else:
                        sample_undetermined[sample_name] = 1
                    if is_a_block:
                        current_block_end = snp_position
                elif snp_type == "not introgressed":
                    if is_a_block: # We finished a block
                        current_block_end = snp_position
                        block_size = current_block_end - current_block_start - 1
                        if sample_name in sample_blocks.keys():
                            sample_blocks[sample_name].append(block_size)
                        else:
                            sample_blocks[sample_name] = [block_size]
                        is_a_block = False
                        current_block_start = snp_position
                        current_block_end = snp_position
                    else:
                        current_block_start = snp_position
                        current_block_end = snp_position
                else: # Something unexpected has happened
                    print("WTF")
                if sample_name in sample_total_snps.keys():
                        sample_total_snps[sample_name] += 1
                else:
                    sample_total_snps[sample_name] = 1
        if is_a_block: # We ended the file in a block
            block_size = current_block_end - current_block_start - 1
            if sample_name in sample_blocks.keys():
                sample_blocks[sample_name].append(block_size)
            else:
                sample_blocks[sample_name] = [block_size]
            is_a_block = False
            current_block_start = 0
            current_block_end = 0
        current_block_start = 0
        current_block_end = 0

for sample_name in sample_total_snps.keys():
    if sample_name in sample_undetermined.keys():
        undetermined_count = sample_undetermined[sample_name]
    else:
        undetermined_count = 0
    if sample_name in sample_introgressed.keys():
        introgressed_count = sample_introgressed[sample_name]
    else:
        introgressed_count = 0
    if sample_name in sample_total_snps.keys():
        total_snp_count = sample_total_snps[sample_name]
    else:
        total_snp_count = 0
    if sample_name in sample_blocks.keys():
        block_count = len(sample_blocks[sample_name])
        min_block = min(sample_blocks[sample_name])
        max_block = max(sample_blocks[sample_name])
        mean_block = statistics.mean(sample_blocks[sample_name])
        if len(sample_blocks[sample_name]) > 1:
            stdev_block = statistics.stdev(sample_blocks[sample_name])
        else:
            stdev_block = 0
    else:
        block_count = 0
        min_block = "NA"
        max_block = "NA"
        mean_block = "NA"
        stdev_block = "NA"
    print("%s,%s,%s,%s,%s,%s,%s,%s,%s" % (sample_name, str(undetermined_count), str(introgressed_count), str(total_snp_count), str(block_count), str(min_block), str(max_block), str(mean_block), str(stdev_block)))
    
            
