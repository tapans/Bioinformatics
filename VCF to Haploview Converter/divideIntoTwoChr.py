import os 
import sys

if __name__ == '__main__':

    inputfile = str(sys.argv[1])

    f = open(inputfile,'r') 
    outputfile = open(str(sys.argv[2]),'w') 	

	# given a b 1 0 1 0 1 0 in file
	# make new file with:
	#			a b 1 1 1
	# 			a b 0 0 0 

    line=f.readline()
    while (line):
	linelist=line.split()
	length=len(linelist)
	lista=[]
	listb=[]
	lista.append(linelist[0])
	lista.append(linelist[1])
	listb.append(linelist[0])
	listb.append(linelist[1])	
	for i in range(2, length):

	    if i%2 == 0:
		lista.append(linelist[i])
	    else:
		listb.append(linelist[i])
	outputfile.write(" ".join(lista))
	outputfile.write("\n")
	outputfile.write(" ".join(listb))
	outputfile.write("\n")
	line=f.readline()