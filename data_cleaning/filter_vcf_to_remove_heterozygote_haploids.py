#! /usr/bin/python2

# filter_vcf_to_remove_heterozygote_haploids.py
# This version is for datasets with mixed haploid and diploid samples.
# Takes a vcf file from ipyrad and a file with a one-per-row list of the haploid sample names. For haploids, it only keeps genotypes that were called as homozygous. For diploids it keeps all genotypes. If filtering makes a snp non-variable the snp position is removed entirely. It replaces the genotype calls in the vcf with "./." but keeps the original read count info in case we want them later.
# I don't like how ipyrad is calling genotypes for haploids. It uses a strict majority rule to call the genotype and only calls unknown if there are exactly the same number of major/minor allele reads. If there are large numbers of minor allele reads it either means there is a very high error level or that we have combined more than one locus into a single locus. Either way, I don't want that in my data. So I am calling genotypes as if samples are diploid and for the haploid samples, only keeping genotypes that ipyrad called as homozygous. This way we get the benefit of ipyrad's statistical genotype calling to eliminate samples that likely don't really represent haploids. We are losing some data in the process, but I'd rather have less data that contains less noise.
# usage: ./filter_vcf_to_remove_heterozygotes.py vcf_file.vcf haploid_list.txt > filtered_vcf.vcf

import sys

# Read the ploidy table into a dictionary
haploid_samples = []
with open(sys.argv[2]) as haploid_file:
    for line in haploid_file:
        haploid_samples.append(line.strip())

# Read the vcf file and filter it
with open(sys.argv[1]) as vcf_file:
    for line in vcf_file:
        if line[0:2] == "##": # Print the header lines as is
            print(line.strip())
        elif line[0] == "#": # Sample name line. We need to keep track of which indices are the haploids so we only fix those elements of the data
            elements = line.strip().split()
            samplenames = elements[9:]
            haploid_indices = []
            index = 0
            for samplename in samplenames:
                if samplename in haploid_samples:
                    haploid_indices.append(index)
                index += 1
            print(line.strip())
        else: # it is a locus dataline with genotypes we need to process
            elements = line.strip().split()
            #print elements
            output_string = "\t".join(elements[0:7]) + "\t.\t" + elements[8]
            genotypes_kept = [] # Keep track of how what genotypes we keep so we can drop non-variable loci or loci with no remaining genotypes but only in haploids
            index = 0
            for genotype_string in elements[9:]:
                genotype_string_elements = genotype_string.split(":")
                genotype = genotype_string_elements[0]
                if genotype == "./.": #It is already an unknown genotype. Keep as is.
                    output_string += "\t" + genotype_string
                else: # It is a known genotype. Let's see if we want to keep it
                    alleles = genotype.split("/")
                    if alleles[0] == alleles[1] or index not in haploid_indices: # Keep it. It is a diploid or it is a haploid called as homozygous.
                        output_string += "\t" + genotype_string
                        if genotype not in genotypes_kept:
                            genotypes_kept.append(genotype)
                    else: # It is a haploid called as heterozygous. Replace the genotype with ./.
                        output_string += "\t./.:" + ":".join(genotype_string_elements[1:])
                index += 1
            if len(genotypes_kept) > 1: # We still have a variable locus
                print(output_string)
