<pre>
The script "vcfToHapMap" can be used to generate N Hap files for as many as N populations (N >= 2).
It also generates a map file, which can be used together with one of the hap files in Haploview program with Haps format option.
NOTE: YOU MUST HAVE VCFTOOLS.EXE IN THE SAME FOLDER AS THIS SCRIPT ALONG WITH OTHER INPUT FILES.

The script takes a compressed .vcf.gz file, chromosome number, mid position of the window of interest, size of the window and the filenames of population files containing the ids of individuals to keep in the resulting hap file

To use the script "vcfToHapMap",

First, make the script executable by typing the following command from the directory in which vcfToHapMap script is located in

chmod +x vcfToHapMap

Now, you are ready to use this script.
Run the following with desired parameters in the termnal:

./vcfToHapMap compressedVCF.gz chr midPos winSize sampleA sampleB .. sampleN

Where:
- "compressedVCF.gz" is the name of the vcf.gz file you want to use as input,
- "chr" is the chromosome of the marker
- "midPos" is the mid position of the desired window. i.e if you are only interested in the region(window) 1 to 25000, midpos would be 12501
- "winSize" is the size of the window/region that youa re interested in. i.e if you are interested in the region 1 to 25000, winSize is 25000
- "sampleA" ,"sampleB", "sampleN" are the population filenames containing the individuals to keep for each output hap file

If you don't run the script properly, the following error statement will be displayed and the program will quit:
echo usage example: $0 compressedVCFfile chr midPosOfWindow windowSize populationA populationB .. populationN >&2
echo usage example: $0 dct.vcf.gz 13 95112501 25000 samples-EAS samples-EUR >&2
echo "see README.txt for more details"

If you are using Cygwin terminal and the script does not execute, you may have to type the following:
dos2unix vcfToHapMap
</pre>