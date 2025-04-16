#! /usr/bin/python

# extract_LSC-IRA-SSC_from_SSC-IRB-LSC-IRA-SSC-IRB-LSC.py
# Takes a folder of consensus fastas and a table of inverted repeat and single copy regions within
# each sequence (along with columns showing whether single copies are in the plus or minus
# direction, and columns showing whether single copies are in the correct order and whether the
# sample should be included or excluded) and returns a single fasta file with the LSC-IRA-SSC
# sequence from each of the fastas so we can then use it as input for alignment software.

# usage: ./extract_LSC-IRA-SSC_from_SSC-IRB-LSC-IRA-SSC-IRB-LSC.py ir_sc_section_lengths.csv path_to_folder_of_consensus_fastas > LSC-IRA-SSC_file_to_be_aligned.fasta

import sys
import os
import HTSeq
from Bio.Seq import Seq

section_lengths_filename = sys.argv[1]
consensus_folder_path = sys.argv[2]

# Read the section lengths info into a dictionary
section_info = {} # key = samplename, values = list of [SSC1_length, IRB1_length, LSC1_length, IRA_length, SSC2_length, LSC_direction, SSC_direction, is_included, is_correct_order]
with open(section_lengths_filename, "r") as section_lengthsfile:
    for line in section_lengthsfile:
        elements = line.strip().split(",")
        samplename = elements[0]
        SSC1_length = int(elements[2])
        IRB1_length = int(elements[3])
        LSC1_length = int(elements[4])
        IRA_length = int(elements[5])
        SSC2_length = int(elements[6])
        LSC_direction = elements[11]
        SSC_direction = elements[13]
        is_included = int(elements[14])
        is_correct_order = int(elements[15])
        section_info[samplename] = [SSC1_length, IRB1_length, LSC1_length, IRA_length, SSC2_length, LSC_direction, SSC_direction, is_included, is_correct_order]

# Process each consensus fasta file in the specified folder
for filename in os.listdir(consensus_folder_path):
    if filename.endswith(".fasta"):
        fastafile = HTSeq.FastaReader(os.path.join(consensus_folder_path, filename))
        for read in fastafile:
            trimmed_sequence = ""
            samplename = read.name
            long_sequence = read.seq
            if samplename not in section_info.keys(): #We have a consensus sequence that wasn't expected
                print >> sys.stderr, samplename + " was not expected!"
            else:
                if section_info[samplename][7]: #sample is meant to be included in the output
                    IR = long_sequence[section_info[samplename][0] + section_info[samplename][1] + section_info[samplename][2] : section_info[samplename][0] + section_info[samplename][1] + section_info[samplename][2] + section_info[samplename][3]]
                    if section_info[samplename][8]: # Correct order
                        LSC = long_sequence[section_info[samplename][0] + section_info[samplename][1] : section_info[samplename][0] + section_info[samplename][1] + section_info[samplename][2]]
                        SSC = long_sequence[section_info[samplename][0] + section_info[samplename][1] + section_info[samplename][2] + section_info[samplename][3] : section_info[samplename][0] + section_info[samplename][1] + section_info[samplename][2] + section_info[samplename][3] + section_info[samplename][4]]
                    else:
                        SSC = long_sequence[section_info[samplename][0] + section_info[samplename][1] : section_info[samplename][0] + section_info[samplename][1] + section_info[samplename][2]]
                        LSC = long_sequence[section_info[samplename][0] + section_info[samplename][1] + section_info[samplename][2] + section_info[samplename][3] : section_info[samplename][0] + section_info[samplename][1] + section_info[samplename][2] + section_info[samplename][3] + section_info[samplename][4]]
                    if section_info[samplename][5] == "minus": #LSC is the wrong direction and needs  revcomp
                        LSC = Seq(LSC).reverse_complement()
                    if section_info[samplename][6] == "minus": # SSC is the wrong direction and needs revcomp
                        SSC = Seq(SSC).reverse_complement()
                    print ">" + samplename
                    print LSC + IR + SSC
                else: # sample in not meant to be included in the output
                    print >> sys.stderr, samplename + " was intentionally omitted."
