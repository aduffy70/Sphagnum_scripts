# Commands used to in silico digest chloroplast consensus sequences (fasta file format) and generate a psuedo-RADseq chloroplast sample. I want chloroplast RADseq loci for the Dimensions/Diversity samples.

# Required tools:
#    restrict from the Emboss package
#    my parse_and_filter_restrict_output.py script
#    my trim_and_get_all_sample_fragments.py script
#    gzip

# Potential problems with this process:
#    This assumes 100% digestion, which is likely not the case for the real samples, and which sites don't get cut is probably not random.
#    I have a hard cutoff of maximum fragment length, while the real fragments don't have a hard cutoff for size and we don't know what the size distribution actually is.
#    The chloroplast genome assemblies are incomplete and almost certainly contain errors.

# Path to where the consensus sequences are stored. These were an intermediate stage of creating the "whole cp genomes" that contain both copies of the IR. If I want to find loci that might span the IR boundaries I need to start with these, not the simplified LSC-IR-SSC sequences.
CPATH=/home/aduffy/Dropbox/My_Shaw_Lab/Dimensions_Diversity_Genome_Analyses/Dimensions_Diversity_cp_genome_assembly/Consensus_sequences

# For each sample, Get a list of all the EcoRI and MseI cutsites.
for FILE in $(ls $CPATH/) ;
do
    echo $FILE ;
    SAMPLE=${FILE%.consensus.fasta}
    restrict -sequence $CPATH/$FILE -sitelen 4 -enzymes EcoRI,MseI -outfile ./Cutsites/$SAMPLE.cutsites.txt
done ;

# Get an unformatted list of fragments between 35 and 2500bp with an EcoRI cutsite at one end and an MSeI cutsite at the other.
for FILE in $(ls $CPATH/) ;
do
    echo $FILE ;
    SAMPLE=${FILE%.consensus.fasta}
    ./parse_and_filter_restrict_output.py ./Cutsites/$SAMPLE.cutsites.txt $CPATH/$FILE 35 2500 > ./Pseudodigest_fragments/$SAMPLE.fragments.txt
done ;

# If a fragment ends in Ns, cut off the trailing Ns. If a fragment contains a continuous run of more than 20 Ns it represents a large gap of missing sequence (hundreds to 10s of thousands of bases) so cut off the Ns and anything after. If these modifications make the read less than 35bp, drop it.
for FILE in $(ls ./Pseudodigest_fragments) ;
do
    echo $FILE ;
    SAMPLE=${FILE%.fragments.txt}
    ./fix_reads_with_large_gaps.py ./Pseudodigest_fragments/$FILE 35 > Fixed_pseudodigest_fragments/$SAMPLE.fixedfragments.txt
done ;

# Get counts of fragments in each sample
wc -l Fixed_pseudodigest_fragments/*

# Trim each fragment to 92 bases (to match what we get from a 100bp Illumina read after removing an 8bp barcode). If that makes it end with any Ns, remove them. Put 10 copies of each of them in a fastq format (more than enough to pass ipyrad's depth filter). The quality scores are all set to a high value (all "E") that will pass ipyrad's quality filter.
for FILE in $(ls ./Fixed_pseudodigest_fragments) ;
do
    echo $FILE ;
    SAMPLE=${FILE%.fixedfragments.txt}
    ./trim_and_get_all_sample_fragments.py ./Fixed_pseudodigest_fragments/$FILE 10 92 > RADseq_fastqs/$SAMPLE.fastq
done ;

#Manually remove files for samples with zero reads: IYSA, ISSB
#Manually remove duplicates: IYRD_29 manual_bad_IR
# Manually remove the "_" from the name of the Smagellanicum and Sfallax reference genomes. It causes problems with the next renaming step.


#Rename files to just include the sample name without other numbers.
for FILE in $(ls ./RADseq_fastqs) ;
do
    SAMPLE=${FILE%.fastq} ;
    SAMPLE=${SAMPLE%%_*} ;
    echo $SAMPLE ;
    mv ./RADseq_fastqs/$FILE ./RADseq_fastqs/$SAMPLE.fastq
done ;

# Zip each file into a fastq.gz
for FILE in $(ls ./RADseq_fastqs/*.fastq) ;
do
    gzip $FILE ;
done ;
