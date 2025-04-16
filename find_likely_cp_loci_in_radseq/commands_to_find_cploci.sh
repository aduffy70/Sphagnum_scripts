# Steps I used to find likely chloroplast loci in the majus ipyrad data.

# Get the sequence from a random sample to represent each locus
./get_example_sequence_from_ipyrad_loci.py postmergeAll110_90.loci > example_sequences.fa

# Index the S. fallax chloroplast genome for bwa
bwa index S_fallax_cpgenome/Sphagnum_fallax_cpgenome.fasta

# Map these example sequences to the S_fallax chloroplast genome (allow 9 mismatches--to approximate 0.9 clustering in ipyrad)
bwa aln -t 5 -n 9 -N S_fallax_cpgenome/Sphagnum_fallax_cpgenome.fasta example_sequences.fa > mapping.sai

# Convert to sam then bam format
bwa samse S_fallax_cpgenome/Sphagnum_fallax_cpgenome.fasta mapping.sai example_sequences.fa > mapping.sam
samtools view -Sb mapping.sam > mapping.bam

# Count mapped loci, then write them to a file. Manually inspect and look for weirdness (no weirdness found).
samtools view -F 4 mapping.bam | wc -l
samtools view -F 4 mapping.bam > mapping_loci.tsv

# Get the sequences for these loci in fasta format (which can then be opened in Aliview and saved to other formats as needed)
./filter_loci_file_into_fasta.py postmergeAll110_90.loci mapping_loci.tsv > majus_cp_loci.fasta
