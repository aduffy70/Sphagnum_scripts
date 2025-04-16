#! /usr/bin/python2

# fix_reads_with_large_gaps.py
# Takes the output of my parse_and_filter_restrict_output.py script and fixes any reads with large gaps. Long runs of Ns (50bp) in my cp genomes represent a gap of hundreds to 10s of thousands of bases. If a fragment includes one of those we don't want to keep the Ns or anything after them. If that makes the read shorter than the specified length, drop it.

# usage: ./fix_reads_with_large_gaps.py file_of_sequence_fragments.txt minimum_read_length_integer > file_of_fixed_sequence_fragments.txt

import sys
import random

minimum_read_length = int(sys.argv[2])

with open(sys.argv[1]) as fragment_file:
    for line in fragment_file:
        line = line.strip()
        fragment_length = len(line)
        if fragment_length > 0: # Not a blank line
            gap_start = line.find("NNNNNNNNNNNNNNNNNNNN")
            if gap_start != -1: # There is a gap, let's fix the fragment
                line = line[0:gap_start]
                if len(line) >= minimum_read_length: # It is still long enough after fixing.
                    print line
            else: # No gap, just print the fragment
                print line
