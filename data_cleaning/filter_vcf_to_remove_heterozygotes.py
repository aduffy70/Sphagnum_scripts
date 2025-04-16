#! /usr/bin/python2

# filter_vcf_to_remove_heterozygotes.py
# Takes a vcf file from ipyrad and only keeps genotypes that were called as homozygous. If filtering makes a snp non-variable the snp position is removed entirely.
# I don't like how ipyrad is calling genotypes for haploids. It uses a strict majority rule to call the genotype and only calls unknown if there are exactly the same number of major/minor allele reads. If there are large numbers of minor allele reads it either means there is a very high error level or that we have combined more than one locus into a single locus. Either way, I don't want that in my data. So I am calling genotypes as if samples are diploid and only keeping genotypes that ipyrad called as homozygous. This way we get the benefit of ipyrad's statistical genotype calling to eliminate samples that likely don't really represent haploids. We are losing some data in the process, but I'd rather have less data that contains less noise.
# This script is only for haploid data, obviously.
# usage: ./filter_vcf_to_remove_heterozygotes.py vcf_file.vcf > filtered_vcf.vcf

import sys

# Read the vcf file and filter it
with open(sys.argv[1]) as vcf_file:
    for line in vcf_file:
        if line[0] == "#": # Print the header lines as is
            print(line.strip())
        else: # it is a locus dataline with genotypes we need to process
            elements = line.strip().split()
            #print elements
            output_string = "\t".join(elements[0:7]) + "\t.\t" + elements[8]
            genotypes_kept = [] # Keep track of how what genotypes we keep so we can drop non-variable loci or loci with no remaining genotypes
            for genotype_string in elements[9:]:
                genotype_string_elements = genotype_string.split(":")
                genotype = genotype_string_elements[0]
                if genotype == "./.": #It is already an unknown genotype. Keep as is.
                    output_string += "\t" + genotype_string
                else: # It is a known genotype. Let's see if we want to keep it
                    alleles = genotype.split("/")
                    if alleles[0] == alleles[1]: # It is homozygous. Keep it.
                        output_string += "\t" + genotype_string
                        if genotype not in genotypes_kept:
                            genotypes_kept.append(genotype)
                    else: # It doesn't meet the cutoff. Replace the genotype with ./.
                        output_string += "\t./.:" + ":".join(genotype_string_elements[1:])
            if len(genotypes_kept) > 1: # We still have a variable locus
                print(output_string)
