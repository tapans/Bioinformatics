#!/usr/bin/bash

# Setting the path, so commands are not executed from users PATH
PATH=/bin:/usr/bin:/usr/local/bin

# We will store temporary files in /tmp/fst$$
# $$ is replaced by the processid of the shell so that two different executions of the same program will not collide on temporary files.
tmp=/tmp/fst$$

rm -fr $tmp
mkdir $tmp
trap "rm $tmp/*; rmdir $tmp; exit 0;" 0 1 2 15 

# only keep the first four columns - don't need data from rest
cut -d " " -f 1-4 $1 > $tmp/rehh-AFR1
cut -d " " -f 1-4 $2 > $tmp/rehh-eur1
cut -d " " -f 1-4 $3 > $tmp/rehh-EAS1

# sort the files
sort $tmp/rehh-AFR1 > $tmp/rehh-AFR1.srt
sort $tmp/rehh-eur1 > $tmp/rehh-eur1.srt
sort $tmp/rehh-EAS1 > $tmp/rehh-EAS1.srt

#take all lines from each file where id is common in each and create a new file
#only keep relevant columns
join $tmp/rehh-AFR1.srt $tmp/rehh-eur1.srt > $tmp/tempFile
cut -d " " -f "1-4 7" $tmp/tempFile > $tmp/newFile
sort $tmp/newFile > $tmp/newFile2 
join $tmp/newFile2 $tmp/rehh-EAS1.srt > $tmp/modifiedFile
cut -d " " -f "1-5 8" $tmp/modifiedFile > $tmp/modifiedFile2

#add sample sizes after each frequency column. i.e 185 after freq_a, 379 after freq_eur and 189 after freq_EAS
awk 'BEGIN { OFS = " " } { $5 = "185 " $5; print }' $tmp/modifiedFile2 > $tmp/modifiedFile3
awk 'BEGIN { OFS = " " } { $7 = "379 " $7; print }' $tmp/modifiedFile3 > $tmp/modifiedFile4
awk 'BEGIN { OFS = " " } { $9 = "286 " $9; print }' $tmp/modifiedFile4 > $tmp/result

#add header line to the resulting file
echo "ID CHR POS FREQ_AFR SAMPLE_SIZE FREQ_EUR SAMPLE_SIZE FREQ-EAS SAMPLE_SIZE" > $tmp/header

#create resulting file in current directory
cat $tmp/header $tmp/result > result