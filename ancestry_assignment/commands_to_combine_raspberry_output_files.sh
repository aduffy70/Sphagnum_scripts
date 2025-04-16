#! /bin/sh

# For each chromosome, RASPberry gives a file for each admixed sample. I want to combine all of those sample files into one big file for plotting in R, but I need to add a column to the data with the sample number.

# This code leaves multiple copies of the header line interspersed in the combined file but I can easily eliminate them in R. Run this for each chromosome.

mychr="8"

myfolder="./raspberry_run_$mychr"

for i  in {1..42} 
do
    myfile="$myfolder"/chr"$mychr"_paramId_1_Ind_"$i".txt
    IFS=$'\n'
    for myline in $(cat "$myfile")
    do
        echo -e "$i\t$myline" >> chr"$mychr"_paramId_1_AllInd.txt
    done
done
