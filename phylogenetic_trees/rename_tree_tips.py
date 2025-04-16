#! /usr/bin/python2

# rename_tree_tips.py
# Takes a raxml bipartitions tree and replaces the tip names with new names from a
# csv format conversion table with no header row (oldname,newname,ignoredadditionalcolumns).
# Outputs the new table string and a list of any old labels that were not found.
# usage: ./rename_tree_tips.py bipartitions_file conversion_table.csv

import sys

# Read in the conversion table
old_to_new = {} # A dictionary to hold conversions key=oldname, value=newname
with open(sys.argv[2]) as conversion_file:
    for line in conversion_file:
        elements = line.strip().split(",")
        old_to_new[elements[0] + ":"] = elements[1] + ":"

# Read in the tree string
with open(sys.argv[1]) as tree_file:
    tree = tree_file.readline().strip()
    #print tree

# For each item in the conversion table, see if it is in the tree and if so, replace it.
not_in_tree = [] # Keep track of the ones that aren't needed
for oldname in old_to_new.keys():
    index = tree.find(oldname)
    if index != -1:
        tree = tree[0:index] + old_to_new[oldname] + tree[index + len(oldname):]
    else:
        not_in_tree.append(oldname)
        print oldname, old_to_new[oldname]

print tree

if len(not_in_tree) > 0:
    print "Names in the conversion file but not in the tree:"
    for name in not_in_tree:
        print name
