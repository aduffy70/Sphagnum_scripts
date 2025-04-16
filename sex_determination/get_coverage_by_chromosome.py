#! /usr/bin/python2

# get_coverage_by_chromosome.py
# Takes an ipyrad loci file and for each sample outputs the % locus coverage in
# each chromosome. For example, if there are 10 total loci in Chromosome 1 and
# 5 of them are present in a sample, that sample has 50% coverage of LG01 loci.
# I want to see if % coverages for LG20 are drastically different from other
# chromosomes in some samples suggesting they don't actually have that chromosome
# because of their sex.
# This is best done on a dataset before loci have been filtered for sample coverage
# since most LG20 loci will get filtered if we have too many samples of the sex
# that does not have that chromosome.
# usage: ./get_coverage_by_chromosome.py loci_file.loci > chromosome_locus_coverages.csv

import sys

chromosomes = ["LG01", "LG02", "LG03", "LG04", "LG05", "LG06", "LG07", "LG08", "LG09", "LG10", "LG11", "LG12", "LG13", "LG14", "LG15", "LG16", "LG17", "LG18", "LG19", "LG20"] # These are the chromosome names I care about. Anything else (scaffolds etc) will be classified as "Other"
locus_counts_by_chromosome = {} # key = chromosome name, value = count of loci in that chromosome
locus_counts_by_sample = {} # key = sample_name, value = {} key = chromosome name, value = count of loci in that chromosome for that sample

# Read the loci file
with open(sys.argv[1]) as vcf_file:
    samples_with_locus = [] # Keep track of which samples have the current locus
    for line in vcf_file:
        elements = line.strip().split()
        if elements[0] == "//": # It is the end of a locus
            is_in_a_chromosome = False
            for chromosome in chromosomes:
                if chromosome in line:
                    current_chromosome = chromosome
                    is_in_a_chromosome = True
            if not is_in_a_chromosome:
                current_chromosome = "Other"
            if current_chromosome in locus_counts_by_chromosome.keys():
                locus_counts_by_chromosome[current_chromosome] += 1
            else:
                locus_counts_by_chromosome[current_chromosome] = 1
            for sample in samples_with_locus:
                if sample in locus_counts_by_sample.keys():
                    if current_chromosome in locus_counts_by_sample[sample].keys():
                        locus_counts_by_sample[sample][current_chromosome] += 1
                    else:
                        locus_counts_by_sample[sample][current_chromosome] = 1
                else:
                    locus_counts_by_sample[sample] = {current_chromosome: 1}
            samples_with_locus  = []
        else: #Add the sample to the list of samples with this locus
            samples_with_locus.append(elements[0])


# Output the table of chromosome coverage by sample
header_string = "sample," + ",".join(chromosomes) + ",Other"
print(header_string)
for sample in locus_counts_by_sample.keys():
    output_string = sample
    for chromosome in chromosomes:
        if chromosome in locus_counts_by_sample[sample].keys():
            percent_coverage = locus_counts_by_sample[sample][chromosome] / float(locus_counts_by_chromosome[chromosome]) * 100
            output_string += "," + str(percent_coverage)
        else:
            output_string += ",0.0"
    if "Other" in locus_counts_by_sample[sample].keys():
        percent_coverage = locus_counts_by_sample[sample]["Other"] / float(locus_counts_by_chromosome["Other"]) * 100
        output_string += "," + str(percent_coverage)
    else:
        output_string += ",0.0"
    print(output_string)
