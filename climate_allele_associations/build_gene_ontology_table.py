#! /usr/bin/python2

# build_gene_ontology_table.py
# I want a table with climate variable, a comma separated list of genes associated with that variable, and a comma separated list of gene ontology terms for those genes. Some of the input files include commas in the data so I need to use tsv versions of those spreadsheets.
# usage: ./build_gene_ontology_table.py genes_at_interesting_loci-clean.csv annotation_info_for_genes_at_interesting_loci.csv GO_Terms_with_descriptions.tsv > gene_ontology_table.csv

import sys

#Read the file with the gene names and climate variables
genes_by_climate_variable = {} # key = climate_variable, value = list of genes
with open(sys.argv[1]) as gene_climate_file:
    for line in gene_climate_file:
        if line[0] != "#": # It is not a header line
            elements = line.strip().split(",")
            gene = elements[1]
            climate_variables = elements[8].split(";")
            for climate_variable in climate_variables:
                if climate_variable not in genes_by_climate_variable.keys():
                    genes_by_climate_variable[climate_variable] = [gene]
                else:
                    genes_by_climate_variable[climate_variable].append(gene)
#for climate_variable in genes_by_climate_variable.keys():
#    print("%s %s" % (climate_variable, ";".join(genes_by_climate_variable[climate_variable])))

# Read the file with the gene names, descriptions, and GO terms
go_terms_by_gene = {} # key = gene, value = list of go terms
gene_descriptions_by_gene = {} # key = gene, value = gene description
with open(sys.argv[2]) as annotation_info_file:
    for line in annotation_info_file:
        elements = line.strip().split("\t")
        #print(str(len(elements)), elements)
        gene = elements[0]
        gene_description = elements[2]
        go_terms = elements[1].split(",")
        go_terms_by_gene[gene] = go_terms
        gene_descriptions_by_gene[gene] = gene_description
#for gene in go_terms_by_gene.keys():
#    print("%s %s %s" % (gene, gene_descriptions_by_gene[gene], ";".join(go_terms_by_gene[gene])))

# Read the file with the GO terms and gene_descriptions
go_descriptions_by_go_term = {} # key = go_term, # value = go_description
with open(sys.argv[3]) as go_term_description_file:
    for line in go_term_description_file:
        elements = line.strip().split("\t")
        go_term = elements[0]
        go_description = elements[1]
        go_descriptions_by_go_term[go_term] = go_description

# Build the table
for climate_variable in genes_by_climate_variable.keys():
    gene_descriptions = []
    go_descriptions = []
    for gene in genes_by_climate_variable[climate_variable]:
        if gene in gene_descriptions_by_gene.keys():
            if gene_descriptions_by_gene[gene] not in gene_descriptions:
                gene_descriptions.append(gene_descriptions_by_gene[gene])
            if gene in go_terms_by_gene.keys():
                for go_term in go_terms_by_gene[gene]:
                    if go_term in go_descriptions_by_go_term.keys():
                        if go_descriptions_by_go_term[go_term] not in go_descriptions:
                            go_descriptions.append(go_descriptions_by_go_term[go_term])
    go_descriptions.sort()
    gene_descriptions.sort()
    print("%s\t%s\t%s" % (climate_variable, "; ".join(gene_descriptions), "; ".join(go_descriptions)))
