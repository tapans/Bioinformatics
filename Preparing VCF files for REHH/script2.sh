#!/usr/bin/bash

PATH=/bin:/usr/bin:/usr/local/bin
# Setting the path, so commands are not executed from users PATH

# script to prepare vcf files for analysis with rehh: do this for each chromosome,
# to create script file, prepare text file with commands and then use chmod 755 filename in Cygwin to make it executable

case $# in
	[0-1])
		echo usage example: $0 samples chr1.gz.vcf ch2.gz.vcf ch3.gz.vcf ... >&2
    	exit 1
    	;;

	*)
		samples=$1
		shift
		
		while (( $# ))
		do
			# replace in the file the chromosome (e.g. replace chr22 for chr21, etc...), save the file, and run dos2unix filename in 
			# cygwin. Then you can run the script again (./script1)
			# open compressed vcf file, keep only relevant samples, filter by allele frequency, remove indels, and keep info on 
			# ancestral alleles
		     ./vcftools --gzvcf "$1" --keep "$samples".txt --remove-filtered-all --maf 0.05 --geno 1 --remove-indels --recode-INFO AA --recode

			# write ancestral allele information to info file
			./vcftools --vcf out.recode.vcf --get-INFO AA

			# change lower to upper case in info file
			tr '[:lower:]' '[:upper:]'  out2.info

			# export vcf file in IMPUTE format
			./vcftools --vcf out.recode.vcf --IMPUTE

			# identify in the info file markers for which reference allele = ancestral allele and those that are reversed
			# delete first row in info file and replace tabs for spaces in info file
			more +2 out2.info | awk '{if($3==$5) print$0,"yes";if($3!=$5) print$0,"no";}' | sed -e 's/\t/ /g' > out3.info

			# merge info file and impute hap file
			# eliminate from merged file markers with no AA info (".") or ("N") or ("-")
			paste out3.info out.impute.hap | awk '($5!="." && $5!="N" && $5!="-")' > merged.out

			# change the allele codes (0 to 3 and 1 to 4) starting in column 7
			# remove potential duplicates
			awk '{for(i=7;i<=NF;i++)if($i==0)$i=3; else $i=4; print}' merged.out | awk '{if(ip[$2]=="") print; ip [$2]=1}' > merged2.out

			# prepare rehh map file using information from the first 2 columns
			awk '{print $1"-"$2,$1,$2,"1","2"}' merged2.out > map-"$1"-"$samples".out

			# change label 3 to 1 when reference allele = ancestral allele (yes)
			# change label 4 to 2 when reference allele = ancestral allele (yes)
			# change label 3 to 2 when reference allele = derived allele (no)
			# change label 4 to 1 when reference allele = derived allele (no)
			# eliminate 6 initial fields in hap file to prepare rehh input hap file
			sed -e '/yes/ s/3/1/g' -e '/yes/ s/4/2/g' -e '/no/ s/3/2/g' -e '/no/ s/4/1/g' merged2.out | cut -d " " -f7-  > merged3.out

			# transpose to create final haplotype file for rehh input
			python -c "import sys; print('\n'.join(' '.join(c) for c in zip(*(l.split() for l in sys.stdin.readlines() if l.strip()))))" < merged3.out > merged4.out

			# add first column with numbers in increasing order
			awk '{print NR " "$0}' merged4.out > hap-"$1"-"$samples".out
			
			# remove intermediate files located in file delete.txt
			xargs rm < delete.txt
			# the files map-chr*.out and hap-chr*.out are the input files for rehh

			shift
		done;
	esac