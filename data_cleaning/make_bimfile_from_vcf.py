#! /usr/bin/python2

# make_bimfile_from_vcf.py
# Takes a vcf file and generates a bimfile format list of all snps in the vcf.
# Expects all snps in the vcf to have EXACTLY two alleles including ONLY A, C, G, or T. The vcf may list more than one alt allele but only 2 alleles can be present in the genotypes.

# Output format (tab delimited):
# chromosome_integer SNP_name genetic_map_position_cM physical_map_position_bp Allele1 Allele2
# RASPberry requires onlu the physical map positions in bp, not the genetic map positions in cM
# so the 3rd column of the bimfile will be all zeros. 

# usage: ./make_bimfile_from_vcf.py vcf_file.vcf > bimfile.vcf


import sys

# Read the vcf file and output one bim-format line per vcf snp line.
with open(sys.argv[1]) as vcf_file:
    for line in vcf_file:
        if line[0] != "#": # it is not a header line
            elements = line.strip().split()
            chromosome = int(elements[0][2:]) # Grabs the integer part of the chromosome name. Expects format: LG01 - LG19. 
            locus = elements[2]
            position = elements[1]
            alleles = [] # List of alleles in order of how they are numbered in the vcf. We have to do it this way because sometimes there are 2+ alternative alleles listed in the vcf but only one is actually used in our samples (because we filtered for loci with exactly 2 alleles present in this sampleset) and we need to be able to get the right one.
            alleles.append(elements[3]) # The reference allele
            alt_alleles = elements[4].split(",") # the alternate allele or alleles
            for allele in alt_alleles:
                alleles.append(allele)
            genotypes = elements[9:]
            genotype_alleles = []
            for genotype in genotypes:
                allele = genotype[0] # the first allele of the genotype
                if allele != "." and allele not in genotype_alleles: 
                    genotype_alleles.append(allele)
                allele = genotype[2] # the second allele of the genotype
                if allele != "." and allele not in genotype_alleles: 
                    genotype_alleles.append(allele)
            allele0 = alleles[int(genotype_alleles[0])]
            allele1 = alleles[int(genotype_alleles[1])]
            print("%s\t%s\t0\t%s\t%s\t%s" % (str(chromosome), locus, position, allele0, allele1))

