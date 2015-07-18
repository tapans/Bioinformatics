#!/usr/bin/bash

PATH=/bin:/usr/bin:/usr/local/bin
# Setting the path, so commands are not executed from users PATH

# This script will automatically run the main script on all chromosomes from [1-22] to prepare files for REHH
# NOTE: input chromsomes files must be named as "chrI.vcf.gz" where "I" corresponds to the chromosome number


case $# in
	1)
		for i in {1..22}
		do 
			./main "$1" "chr$i.vcf.gz"
		done
		;;

	*)
	
    	echo usage example: $0 samples.txt >&2
    	exit 1
    	;;

    esac
