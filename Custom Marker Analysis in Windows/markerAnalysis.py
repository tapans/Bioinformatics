## Written by Tapan Shah, University of Toronto Mississauga.
## See Readme.txt for script details and notes

import os.path
import math
import sys
import getopt

def get_valid_filename(filename):
    '''Use prompt (a string) to ask the user to type the name of a file. If
    the file does not exist, keep asking until they give a valid filename.
    Return the name of that file. '''
        
    while not os.path.exists(filename):
		print "That file does not exist"
		filename = raw_input(prompt)		
    return filename

def Usage():
    ''' Returns a usage message '''

    print 'Usage: python markerAnalysisInWindows.py inputFileName outputFileName [-w windowSize] [-s statType] [-t threshold] [-m minimumNumberOfMarkers]'
    print 'Example1: python markerAnalysis.py statFile statFileInWindows'
    print 'Example2: python markerAnalysis.py ihs-results-eas.txt ihs-windows -s ihs -t 2.0 -m 10'
    print 'Example3: python markerAnalysis.py rsb-eas-afr.out rsbEasAfr -w 25000 -s rsb -t 2.5 -m 10'
    print 'Example4: python markerAnalysis.py rsb-eas-eur.out rsbEasEur w 10000 -s rsb -t 2.5 -m 10'
    print 'Example5: python markerAnalysis.py lsbl lsblResults -w 50000 -s lsbl -t 0.2 -m 10'
    sys.exit()

def makeHeader(outputFile):
    ''' Create a header row and write it to outputFile file '''

    outputFile.write('Chr Start End CenterPos positionOfMaxStatValue maxStatValue avgStatValue %TopSignals numSignals\n')

def topSignalCheck(statisticType, statValue, threshold, tempWindowStatValue=False):
	''' Use different strategies for different statisticTypes to determine if a given marker is a topSignal or not
	If tempWindowStatValue is specified, return true only if statValue is greater than the tempWindowStatValue
	Helper of doWindowsAnalysis '''

	if statisticType=="ihs":
		absStatVal=abs(float(statValue))
		if tempWindowStatValue:
			if absStatVal>float(tempWindowStatValue):
				return True
			return False
		else:
			if absStatVal>float(threshold):
				return True		
			return False

	elif statisticType=="rsb" or statisticType=="lsbl":
		if tempWindowStatValue:
			if float(statValue)>float(tempWindowStatValue):
				return True  
			return False
		else:
			if float(statValue>threshold):
				return True
			return False

	######################################################################################################################
	''' Add other elif statements here if new statisticTypes require different strategy for topSignal determination '''
	######################################################################################################################

def stat_average(statList):
    ''' compute and return average of stat values in a list statList 
    helper of doWindowsAnalysis procedure'''

    avgStat=0.0
    if not statList: return avgStat #empty list case
    for stat in statList:
		avgStat+=stat
    return float(avgStat/len(statList))  
    
def makeWindow(row, ws, winNum, avgStatValue, topSignals, numSignals):
    ''' take a row of type list and remove unnecessary column fields, 
    add necessary ones.  
    helper of doWindowsAnalysis procedure'''

    row=row[0:3] #only interested in first three columns
    sPos=(winNum*ws)+1
    end=sPos+(ws-1)
    centerPos=(sPos+end)/2
    statValue=float(row[2])
    proportionOfTopSignals=float(topSignals/numSignals)*100.0
    maxPos=int(row.pop(1)) 
    chromosome=int(row.pop(0))
    window=[chromosome, sPos, end, centerPos, maxPos, statValue, avgStatValue, proportionOfTopSignals, numSignals]
    return window

def finalizeLastWindow(tempWindowBasis, windows, stat, ws, statList, topSignals, numSignals, minSig, output, last=False):
	''' another helper function to doWindowsAnalysis procedure '''

	oldWinNum=int(tempWindowBasis[1])/ws
	windows[oldWinNum]=makeWindow(tempWindowBasis, ws, oldWinNum, stat_average(statList), topSignals, numSignals)
	for window in windows.values():
		if int(window[8])>=minSig:			
			output.write(' '.join(str(x) for x in window))
			if not last:
				output.write('\n')

def doWindowsAnalysis(f, output, ws, stat, threshold, minSig):
    ''' place markers(chromosome, position and statisticValue triplet) in specified 'windows' that each have information 
    on the number of markers belonging to that window (numSignals), the percentage of markers that exceed a specified 
    threshold (%topSignals), the highest (or lowest) statistical value within the window along with the position at which
     this stat is highest (or lowest), and the average statistical value for that window '''

    #window preparation
    statList=[] ##store all statvalues in here, useful in computing average at any time
    windows={} ## keys are windownumbers, and final values will be the rows with information on signals within the window
    avgStat=0.0
    numSignals=0.0 ##keep count of the number of markers in a given window
    topSignals=0.0 ##keep count of markers that exceed given threshold for a statistic
    tempWindowBasis=[]
    
    #write header row to output file
    makeHeader(output)
    f.readline() ##skipping the header in the input file
	    
    #start off by adding first row to window
    row=f.readline().split()
    statValue=float(row[2])    
    winNum=int(row[1])/ws  
    statList.append(statValue)      ## adding current stat value to statList
    numSignals+=1.0		 #every marker is a potential signal    
    if topSignalCheck(stat, statValue, threshold): #check if this marker is a topSignal based on the statisticType
    	topSignals+=1.0  		   			
    windows[winNum]=row #finally, add this window to the collection of windows	          
    tempWindowBasis=row 
    curChr=int(row[0])

    #handle remaining rows
    nextRow=f.readline().split()
    while nextRow:
		pos=float(nextRow[1])
		winNum=int(pos)/ws
		thisChr=int(nextRow[0])
		statVal=float(nextRow[2])			
		if (thisChr==curChr):
		    if (windows.has_key(winNum)): ##do this if window already exists		
				numSignals+=1.0
				statList.append(statVal) ## keep adding statValues to compute average later
				winStatVal=float(tempWindowBasis[2])
				if topSignalCheck(stat, statVal, threshold): #check if this marker is a topSignal based on the statisticType
				   	topSignals+=1.0  
				if topSignalCheck(stat, statVal, threshold, winStatVal):
					tempWindowBasis=nextRow	   
				nextRow=f.readline().split()
		    else: 
				# finalize old window		
				oldWinNum=int(tempWindowBasis[1])/ws	
				windows[oldWinNum]=makeWindow(tempWindowBasis, ws, oldWinNum, stat_average(statList), topSignals, numSignals)

				#initialize new window
				topSignals=0.0
				numSignals=1.0 						
				statList=[statVal] 	
				if topSignalCheck(stat, statVal, threshold): #check if this marker is a topSignal based on the statisticType
				   	topSignals+=1.0 				    
				windows[winNum]=nextRow	 #create window and put this row in there for now							    
				tempWindowBasis=nextRow #make this row the temp windowCandidate in order to make comparisons with next row
				nextRow=f.readline().split()
		
		if (thisChr!=curChr): ##write all windows for the last chromosome to output file
		    # finalize and write window to file					
			finalizeLastWindow(tempWindowBasis, windows, stat, ws, statList, topSignals, numSignals, int(minSig), output)		    	

			#initialize new window for new chromosome		
		    #start off by processing first row of first window for new chromosome
			topSignals=0.0
			numSignals=1.0
			windows={}
			curChr=int(nextRow[0]) ##set current chromosome to new chromosome	
			statList=[statVal] ## new window starts off with fresh new stat list	
			if topSignalCheck(stat, statVal, threshold): #check if this marker is a topSignal based on the statisticType
				topSignals+=1.0
			windows[winNum]=nextRow
			tempWindowBasis=nextRow
			nextRow=f.readline().split()		    
   
    #write final window to file
    finalizeLastWindow(tempWindowBasis, windows, stat, ws, statList, topSignals, numSignals, int(minSig), output, True)       
    f.close()
    output.close()    

def main(argv):

	if len(argv)<2:
		Usage()

	#save inputfilename and outputfilename in parameters
	inputFileName=get_valid_filename(argv[0])
	outputFileName=argv[1]

	#assign default values
	windowSize=25000
	statisticType="rsb" # by default keep largest stat value as window's representative stat value - the strategy for rsb statistic
	threshold=0
	minNumSignals=0
	
	try:
	    opts, args = getopt.getopt(argv[2:],"hw:s:t:m:",["windowSize=","statisticType=", "threshold=", "minNumSignals="])
	except getopt.GetoptError:
	    Usage()	
	
	#parse optional variables
	for opt, arg in opts:
		if opt in ("-w", "--windowSize"):
			windowSize=arg
		elif opt in ("-s", "--statisticType"):
			statisticType=arg
		elif opt in ("-t", "--threshold"):
			threshold=arg
		elif opt in ("-m", "--minNumSignals"):
			minNumSignals=arg
		elif opt=="-h":
			Usage()

	#open input file in read mode and output file in write mode
	f = open(inputFileName,'r') 
	output = open(outputFileName,'w') 	
	
	#Do the windows analysis
	doWindowsAnalysis(f, output, int(windowSize), statisticType, float(threshold), float(minNumSignals))	

if __name__ == '__main__':
    main(sys.argv[1:])