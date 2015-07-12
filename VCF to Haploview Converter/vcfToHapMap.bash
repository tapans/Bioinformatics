#!/usr/bin/bash
## Written by Tapan Shah, Contact: tapan.shah@utoronto.ca for details
## This script prepares vcf files into hap files of n populations for the common markers with maf > 5% between them
## It also generates a commonMarkers.map file which can be loaded together with the .hap files in Haploview program.

PATH=/bin:/usr/bin:/usr/local/bin
# Setting the path, so commands are not executed from users PATH

if (( $# < 6 ))
	then
		echo usage example: $0 compressedVCFfile chr midPosOfWindow windowSize populationA populationB .. populationN >&2
		echo usage example: $0 dct.vcf.gz 13 95112501 25000 samples-EAS samples-EUR >&2
		echo "see README.txt for more details"
    	exit 1
    else
    	# We will store temporary files in /tmp/script$$
	# $$ is replaced by the processid of the shell so that two different executions of the same program will not collide on temporary files.
		tmp=/tmp/script$$
		
		# this will ensure that all temporary files created in $tmp during the execution will get deleted in end
		rm -fr $tmp
		mkdir $tmp
		trap "rm $tmp/*; rmdir $tmp; exit 0;" 0 1 2 15 

		# Get the beginning and end positions from the given windowSize and the midPosition of interest within it
		halfWinSize=$(( $4 / 2 ))
		from=$(( $3 - $halfWinSize ))
		to=$(( $3 + $(( $halfWinSize - 1 )) ))
		chr="$2"
		compressedVCFfile="$1"
		shift 4 #shifting the first four arguments out, so now $1 is populationA and $# is populationN

	# open compressed vcf file for each population, filter by allele frequency & given window on given chromosome, and generate new vcf file
		# get chr and position (marker) columns for each population and save in temporary file
		populations=""
		for population in $@
		do
			./vcftools --gzvcf $compressedVCFfile --remove-indels --remove-filtered-all --chr $chr --from-bp `echo $from` --to-bp `echo $to` --keep $population --maf 0.05 --out $tmp/$population --recode
			awk '{print $1 "-" $2 " " $2}'  $tmp/"$population.recode.vcf" | grep ^$chr > $tmp/"$population" ## extracting first two columns with chr pos info
			populations=$populations" $tmp/$population" #generating a space separated string of all relevant filenames
		done

		# only keep markers common to all the vcf files produced above and create a map file
		awk '$0 !~ /#/{arr[$1]=arr[$1] " " $2}END{for(i in arr)print i,arr[i]}' $populations | tr -s '' |  awk '{if ($3!="") print}' > $tmp/common
		awk '{print $1 " " $2}' $tmp/common | sort > commonMarkers.map 

		# use commonMarkers file to generate a file with list of all marker positions
		echo "chr position" > $tmp/snpList
		tr '-' ' ' < commonMarkers.map |  awk '{print $1 " " $2}' >> $tmp/snpList
		
		# use the list of marker positions generated above to make new vcf files with only common markers
		# convert all files to plink format to get genotypes of each variant for each individual and then divide each individuals genotype into two chromosomes
		for population in $@
		do
			./vcftools --vcf  $tmp/"$population.recode.vcf" --positions $tmp/snpList --out $tmp/"$population"2 --recode ## only keeping positions common to both populations
			./vcftools --vcf $tmp/"$population"2.recode.vcf --remove-indels --out $tmp/"$population"plink --plink 
			## steps below are not actually necessary because Haploview does recognize .ped (plink) files. However that requires some additional modifications anyways, so convert to .hap format instead:
			awk '{$3=$4=$5=$6=""; print}' $tmp/"$population"plink.ped > $tmp/"population".genotypes #getting rid of unnecessary columns
			python divideIntoTwoChr.py $tmp/"population".genotypes "$population".hap
		done
    fi	