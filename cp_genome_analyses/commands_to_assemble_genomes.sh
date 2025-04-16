# Make a blast db with an example sphagnum layed out as IRB-LSC-IRA-SSC-IRB in that order and the correct orientation (same orientation and order as the published Sphagnum palustre cp genomes).
cd Blast_db
makeblastdb -in IRB_LSC_IRA_SSC_IRB_continuous.fasta -out IR_flanked_cp_genome -dbtype nucl -hash_index
cd ../

# Get counts of contigs in each sample and paste into Contigs_per_sample.xlsx
cd ~/No_backup/Dimensions_cp_mt_genomes/chloro
for file in *.contigs.chloro.fasta; do
    echo -n $file ;
    echo -n "  " ;
    grep ">" $file | wc -l ;
done
cd -

# Rename contigs in assemblies so each fasta record has a unique name
for file in ~/No_backup/Dimensions_cp_mt_genomes/chloro/*.contigs.chloro.fasta; do
    NEWFILENAME=$(basename ${file%.contigs.chloro.fasta}).renamed.fasta ;
    echo $NEWFILENAME ;
    ./make_contig_names_unique.py $file > Assemblies_with_unique_contig_names/$NEWFILENAME ;
done

# Blast each contig file against a IR-flanked example genome so we can see how the contigs should be ordered and oriented..
for file in Assemblies_with_unique_contig_names/*.renamed.fasta; do
    NEWFILENAME=$(basename ${file%.renamed.fasta}).blastout.csv ;
    echo $NEWFILENAME ;
    blastn -outfmt "10 qseqid qlen sseqid sstrand length qstart qend sstart send evalue" -query $file -db Blast_db/IR_flanked_cp_genome -out Blast_output/$NEWFILENAME ;
done

# Parse the blast output and make a rough alignment of the contigs putting them in the correct orientation and padding the starts with "-"s to put them in the correct order with approximately the correct overlap.
for file in Blast_output/*.blastout.csv; do
    ASSEMBLYNAME=$(basename ${file%.blastout.csv}).renamed.fasta ;
    NEWFILENAME=$(basename ${file%.blastout.csv}).rough_alignment.fasta ;
    echo $NEWFILENAME ;
    ./make_alignment_from_contig_blasthits.py Assemblies_with_unique_contig_names/$ASSEMBLYNAME $file > Rough_alignments_of_contigs/$NEWFILENAME ;
done


#Manually review the alignments. Make corrections and insert strings of 10Ns anywhere it is not clear that they overlap. (10N's represents a gap that is probably small, or 50N's for a gap that seems to be larger). We could guess based on the example genome but better to show the true uncertainty. A few show possible evidence of multiple chloroplast genomes. On those few, if I had to open gaps for apparent indels between multiple signals I filled them with Ns to make clear the uncertainty about the true sequence at that point. (IUWB, IUWD, BPHBZ, ISQL, ISTA, IUWJ?, IUWN?, IYQT?, IYQU?, IUUH?)


# Extract a consensus sequence from each alignment.
for file in Rough_alignments_of_contigs/*.fasta; do
     NEWFILENAME=$(basename ${file%.rough_alignment.fasta}).consensus.fasta ;
     ./make_consensus_from_aligned_fastas.py $file > Consensus_sequences/$NEWFILENAME ;
done


# Blast the each consensus sequence against itself to identify inverted repeat sections
for file in Consensus_sequences/*.fasta; do
    NEWFILENAME=$(basename ${file%.consensus.fasta}).selfblastout.csv ;
    blastn -outfmt "10 qseqid qlen sseqid sstrand length qstart qend sstart send evalue" -query $file -subject $file -out Self-blast_output/$NEWFILENAME ;
done

# Parse the selfblast output to calculate the lengths of the IRs and Single-copies.
for file in Self-blast_output/*.csv; do
    ./find_IR_from_selfblast_hits.py $file >> Directions_and_lengths/ir_sc_section_lengths.csv ;
done

# Manually check the lengths to spot oddballs and make manual adjustments. In many cases the 3 IRs are not all the same length. It is expected that the starting and ending IRB's might not be complete, but they still allow us to find both ends of IRA, so IRA > IRB is normal. IRA < IRB is unexpected, but I checked several of these and they differ because of missing bits in IRA of unknown lengths that I filled with 10Ns while manually reviewing alignments in an earlier step. I COULD potentially use the 3 copies of the IR to fill these gaps in at least some sequences, but 1) it took me over an hour to do this for one sample, and 2) many (most?) sequences have the same gaps in the same places so these are still going to be sections of the alignment with many Ns and indels, i.e., high levels of missing data. I will just remove these relatively small sections and live without them.
# End result is a table with lengths of each IR and SC section along each consensus sequence.

# Blast each consensus sequence against just the LSC and just the SSC to check whether they are oriented in the "correct" direction.
for file in Consensus_sequences/*.fasta; do
    NEWFILENAME=$(basename ${file%.consensus.fasta}).LSC_blastout.csv ;
    blastn -outfmt "10 qseqid qlen sseqid sstrand length qstart qend sstart send evalue" -query $file -subject Blast_db/LSC.fasta -out LSC_blast_output/$NEWFILENAME ;
    NEWFILENAME=$(basename ${file%.consensus.fasta}).SSC_blastout.csv ;
    blastn -outfmt "10 qseqid qlen sseqid sstrand length qstart qend sstart send evalue" -query $file -subject Blast_db/SSC.fasta -out SSC_blast_output/$NEWFILENAME ;
done

# Parse that blast output so I don't have to open 400 files to find the handful with backwards LSC or SSCs.
for file in LSC_blast_output/*.csv; do
    ./find_LSC_or_SSC_direction.py $file >> Directions_and_lengths/LSC_directions.csv ;
done
for file in SSC_blast_output/*.csv; do
    ./find_LSC_or_SSC_direction.py $file >> Directions_and_lengths/SSC_directions.csv ;
done

# Manually paste the info about LSC and SSC directions into ir_section_lengths. I have 9 consensus sequences with single copy regions that need to be flipped, are out of order, or that have messed up IRs that need to be manually inspected. The flipped SSCs and out of order ones I will correct in the step below where I extract the LSC-IR-SSC, but I manually inspected and corrected the two with IR issues:
    # BPHCA assembled with a piece of SSC at both ends of an IR fragment, so my blast process thought that piece was part of the IR. I removed the extra bit from the end of the consensus sequence.
    # IYRN appears to have a reversed piece of what is SSC included in the IR adding 7000bp to it's length. That isn't impossible, but the other acutifolia has a "normal" IR-SSC boundary. I don't know if it is assembly error or real, but even if it is real, it is an autapomorphy that won't contribute anything to the phylogenetic analyses and risks complicating alignment, so I removed it...making the IR boundary match ISRN.

# Manually Add a column to the ir_section lengths for keep/drop and for correct order SSC/LSC so my script can handle all the possibilities automatically.

# Pull the LSC-IRA-SSC for each sample (put them in the "correct" orientation and order if they aren't already, and write them to a single fasta file we can align.
./extract_LSC_from_SSC-IRB-LSC-IRA-SSC-IRB-LSC.py Directions_and_lengths/ir_sc_section_lengths.csv Consensus_sequences/ > LSC-IR-SSC_for_alignment/LSC_for_alignment.fasta
./extract_IRA_from_SSC-IRB-LSC-IRA-SSC-IRB-LSC.py Directions_and_lengths/ir_sc_section_lengths.csv Consensus_sequences/ > LSC-IR-SSC_for_alignment/IRA_for_alignment.fasta
./extract_SSC_from_SSC-IRB-LSC-IRA-SSC-IRB-LSC.py Directions_and_lengths/ir_sc_section_lengths.csv Consensus_sequences/ > LSC-IR-SSC_for_alignment/SSC_for_alignment.fasta

# Align each section
muscle -in LSC-IR-SSC_for_alignment/IRA_for_alignment.fasta -out Alignments/IRA_aligned.fasta -diags -log Alignments/IRA_align.log
muscle -in LSC-IR-SSC_for_alignment/SSC_for_alignment.fasta -out Alignments/SSC_aligned.fasta -diags -log Alignments/SSC_align.log

#The LSC takes over 16GB memory to align so I had to move it to the cluster but the process was the same (just within a SLURM requesting 60GB memory)
muscle -in LSC-IR-SSC_for_alignment/LSC_for_alignment.fasta -out Alignments/LSC_aligned.fasta -diags -log Alignments/LSC_align.log

# Bryan wanted some of the ones with big LSC gaps that I dropped so I went back and manually cut LSC-IR-SSC sequences out of the consensus sequences for BPHAW, BPHBO, IUWE, and IYRT, ISSB, ISSW, and IUUE.
