#! /usr/bin/python2

# filter_vcf_for_bad_insilico_loci.py
# Takes a vcf file from ipyrad and only keeps snps where none of a specified list of in silico digested samples have more than 10 reads (evidence of combined loci).

#When I use the Smag reference genome to assemble loci and also include in silico samples, I can spot loci where we are pulling multiple loci into a single locus. Because of the way I generated the in silico samples every locus should have exactly 10 reads. If it has more, we have combined loci and that position should be dropped for all samples.
# Include a flag for whether we want to output the filtered vcf or just a list of the loci we want to drop. Use "vcf" if we want the vcf output or "list" if we want the list of loci. The list of loci is tab separated Chromosome, position so we can feed it into vcftools (with the --exclude-positions tag) if we like.
#The list of insilico samples is one name per line, no other info in the file.
# usage: ./filter_vcf_for_bad_insilico_loci.py vcf_file.vcf vcf reference_sample_name_list.txt > filtered_vcf.vcf
# usage: ./filter_vcf_for_bad_insilico_loci.py vcf_file.vcf list reference_sample_name_list.txt > list_of_loci.csv

import sys

# Read the list of sample names
reference_samples = []
with open(sys.argv[3]) as ref_sample_file:
    for line in ref_sample_file:
        reference_samples.append(line.strip())

# Read the vcf file and filter it
output_type = sys.argv[2] # "vcf" for filtered vcf output or "list" for a list of the loci to be removed
dropped_loci = [] # A list of loci to drop (Chromosome,position,locus_name)
reference_sample_indices = [] # A list of indices of the reference samples we need to inspect
with open(sys.argv[1]) as vcf_file:
    if output_type == "list":
        print("#chromosome\tposition")
    for line in vcf_file:
        elements = line.strip().split()
        if line[0:2] == "##": # Print the header lines as is
            if output_type == "vcf":
                print(line.strip())
        elif elements[0] == "#CHROM": # It is the header line with the sample names. Find where the reference sample is in the list of names
                for sample in reference_samples:
                    if sample in elements:
                        reference_sample_indices.append(elements.index(sample))
                if output_type == "vcf":
                    print(line.strip())
        else: # It is a dataline we need to process
            is_good_locus = True
            for sample_index in reference_sample_indices:
                sample_readcount = int(elements[sample_index].split(":")[1])
                if sample_readcount > 10: # Too many reads--it is a bad locus
                    is_good_locus = False
            if is_good_locus: # The expected number of reads, keep the locus
                if output_type == "vcf":
                    print(line.strip())
            else: # Wrong number of reads, drop it
                if output_type == "list":
                    print(elements[0] + "\t" + elements[1])
