#!/usr/bin/bash
#take a result file of an ihs/rsb/lsbl statistic and create a new file with only desired number of top signals

# Setting the path, so commands are not executed from users PATH
PATH=/bin:/usr/bin:/usr/local/bin

case $# in
	3)

		# We will store temporary files in /tmp/tops$$
		# $$ is replaced by the processid of the shell so that two different executions of the same program will not collide on temporary files.
		tmp=/tmp/tops$$

		rm -fr $tmp
		mkdir $tmp
		trap "rm $tmp/*; rmdir $tmp; exit 0;" 0 1 2 15 

		#store header to add to outputfile
		head -1 $1 > $tmp/header

		#remove header row from inputfile
		sed '1d' $1 > $tmp/noHeaderFile

		#sort noHeaderFile with respect to stat, starting from lowest stat value at top
		sort -g -k6 $tmp/noHeaderFile > $tmp/sortedFile

		#get required number of top Signals
		numWindowsInInput=`cat $1 | wc -l`
		percentToDecimal=`awk 'BEGIN{printf("%0.5f", '$2' / '100')}'`
		numTopSignalsNeeded=$(echo "$numWindowsInInput*$percentToDecimal" | bc)
		numTopSignalsInt=$(( `echo $numTopSignalsNeeded |  sed 's/[.].*//'` + 1))
		tail -"$numTopSignalsInt" $tmp/sortedFile > $tmp/topSignals

		#keep only necessary columns (chr, start, end, center-pos, stat, avgStat)
		cut -d " " -f 6,8,1,3,2,4,9,10 $tmp/header > $3 # add header
		cut -d " " -f 6,8,1,3,2,4,9,10 $tmp/topSignals >> $3
		;;

	*)
		echo usage: $0 statResultFile desired%TopSignal# outputFileName >&2
    	echo usage example: $0 ihs-windows 0.1 top0.1%Signals >&2
    	exit 1
    	;;

    esac
	