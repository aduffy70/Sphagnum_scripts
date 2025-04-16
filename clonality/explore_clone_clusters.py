#! /usr/bin/python3

# explore_clone_clusters.py
# Takes a csv table of pairwise distances and outputs clusters of samples that are connected by
# pairwise distances less than some specified cutoff. Not all distances among them need to be below
# the cutoff--that is what I want to explore.
# For each cluster identified, outputs a csv table of the pairwise distances.
# usage: ./explore_clone_clusters.py distmatrix.csv cutoff_float

import sys

# Read in the pairwise distances table
cutoff = float(sys.argv[2])
samplenames = []
distmatrix = [] # matrix (list of lists) of the distances
is_headerline = True
with open(sys.argv[1]) as distmatrix_file:
    for line in distmatrix_file:
        elements = line.strip().split(",")
        if is_headerline:
            if elements[0]=="": #first element of the header might be blank or might be the first sample name, depending on how the matrix was created
                samplenames = elements[1:] # Grab the samplenames from the header, but drop that first empty element
            else:
                samplenames = elements
            samplecount = len(samplenames)
            is_headerline = False
        else:
            distmatrix.append(elements[1:]) # first element is the sample name

# Make clusters
clusters = [] # List of lists of clusters of clones
is_firstcluster = True
for x in range(0, samplecount):
    for y in range(0, samplecount):
        if float(distmatrix[x][y]) <= cutoff and x!=y:
#            print("\n", samplenames[x], samplenames[y])
            if is_firstcluster:
                clusters.append([samplenames[x], samplenames[y]])
                is_firstcluster = False
            else:
                in_cluster = False # Track whether this sample is already in a cluster
                for cluster in clusters:
                    if samplenames[x] in cluster or samplenames[y] in cluster:
                        if samplenames[x] not in cluster:
                            cluster.append(samplenames[x])
                        if samplenames[y] not in cluster:
                            cluster.append(samplenames[y])
                        in_cluster = True
                if not in_cluster:
                    clusters.append([samplenames[x], samplenames[y]])
#            for cluster in clusters:
#                print(cluster)

# Updated 2024-05 There are edge cases where samples appear in more than one cluster and so those clusters should be combined. The older version of the script caught the problem and warned about it. This update resolves the problem and still checks afterward to make sure it is corrected and warn if not. So if I've still missed some edge case, we are covered.

if len(clusters) > 1: # None of this makes sense if there isn't more than one cluster
    is_updated = False
    while not is_updated:
        combined = [] # List of indices of clusters that were combined
        updated_clusters = [] # The new list of lists of clusters of clones
        is_updated = False # Keep track of whether we made any changes this round
        for x in range(0, len(clusters) - 1):
            if x not in combined:
                new_cluster = clusters[x]
                for y in range(x, len(clusters)):
                    if y not in combined:
                        if (set(new_cluster) & set(clusters[y])):
                            new_cluster = list(set(new_cluster) | set(clusters[y]))
                            is_updated = True
                            combined.append(y)
                updated_clusters.append(new_cluster)
        if y not in combined:
            updated_clusters.append(clusters[y])
        clusters = updated_clusters

#for cluster in clusters:
#    print(" ".join(sorted(cluster)))

# Make sure there are no overlapping clusters
all_samples_in_a_cluster = []
for cluster in clusters:
    for sample in cluster:
        if sample in all_samples_in_a_cluster:
            print("Error: ", sample, "is in more than one cluster")
        else:
            all_samples_in_a_cluster.append(sample)

# Print distance tables for each cluster of clones
for cluster in clusters:
    headerline = "," + ",".join(sorted(cluster))
    print(headerline)
    for sample_x in sorted(cluster):
        dataline = sample_x
        for sample_y in sorted(cluster):
            dataline += "," + distmatrix[samplenames.index(sample_x)][samplenames.index(sample_y)]
        print(dataline)
    print()
