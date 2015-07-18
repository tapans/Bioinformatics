OVERVIEW:

	markerAnalysisInWindows.py scipt can be used to place markers(chromosome, position and statisticValue triplet) in specified 'windows' that each have information on the number of markers belonging to that window (numSignals), the percentage of markers that exceed a specified threshold (%topSignals), the highest (or lowest) statistical value within the window along with the position at which this stat is highest (or lowest), and the average statistical value for that window.

USAGE:

	To run markerAnalysisInWindows.py script, open terminal (or Cygwin terminal if using windows), and run the script by typing:

	python markerAnalysisInWindows.py inputFileName outputFileName [-w windowSize] [-s statType] [-t threshold] [-m minimumNumberOfMarkers]
		- Where "inputfilename" is the name of the file you want to use as input,
		- "outputfilename" is the name you want to give to the resulting file
		- the windowSize is the size (in base pairs) of the windows. In our research, we used the window size of 25000.
		- you may specify a specific statType. Script may need to be modified to change which statValue (ex: max of all   
		    stat values in the window) should 
		 	represent each window. For example, if stat is ihs, the script will keep the stat value which has the largest absolute value in the window.
		- threshold is the threshold that a marker's statValue must exceed in order to be deemed a 
		 	top Signal'. In our research, we used 2.0 for ihs, 2.5 for rsb and 0.2 for lsbl
		- minimumNumMarkersPerWindow is the minimum number of markers a window must have for it to be a valid window/
		    In our research, we specified 10 for this parameter.

NOTES:

	*parameters surrounded in [] are optional. i.e if they are not specified, the script will take default values as 25000 for the windowSize, rsb for the stat value, and 0 for both the threshold as well as the minimumNumberOfMarkers parameter. Following are some Usage examples:

		Example1: python markerAnalysis.py statFile statFileInWindows
		Example2: python markerAnalysis.py ihs-results-eas.txt ihs-windows -s ihs -t 2.0 -m 10
		Example3: python markerAnalysis.py rsb-eas-afr.out rsbEasAfr -w 25000 -s rsb -t 2.5 -m 10
		Example4: python markerAnalysis.py rsb-eas-eur.out rsbEasEur w 10000 -s rsb -t 2.5 -m 10
		Example5: python markerAnalysis.py lsbl lsblResults -w 50000 -s lsbl -t 0.2 -m 10

	**inputFileName must be located in the same folder as the markerAnalysisInWindows.py script

	***inputFileName refers to a file that has space (or tab) separated columns for CHROMOSOME, POSITION, and STATVALUES (such as ihs, rsb, lsbl or any other computed statistic) in the same order. Also, this file must be sorted. (you can quickly sort using Terminal Command sort -g inputFile > sortedInputFile). For example, a sample inputFile may look like:

		CHR POS ihs p-value other-columns ...
		1 30923 1.04646745936215 0.529669992989166 ...
		2 54421 1.25894778451328 0.681833965351423 ... 
		3 60726 -1.11803339512159 0.579132479473 ...
		3 61987 1.60421170283546 0.963900739824788 ...
		4 523471 -0.560424391373736 0.240188674280158 ... 
		4 61989 1.60421170283546 0.963900739824788 ...
		4 63671 1.71337672515842 1.06226523877241 ... 
		22 55299 1.80786606544976 1.15102709843734 ... 
		22 55326 -0.76544060338033 0.352608008938557 ...

	****output will produce a file where each row will be a marker of specified size along with columns with the analysis information for that window. For example, the output, after executing the command "python markerAnalysisInWindows.py sortedInputFile" for the inputfile shown above would be:

		Chr Start End CenterPos positionOfMaxStatValue maxStatValue avgStatValue %TopSignals numSignals
        1 25001 50000 37500 30923 1.04646745936 1.04646745936 100.0 1.0
        2 50001 75000 62500 54421 1.25894778451 1.25894778451 100.0 1.0
        3 50001 75000 62500 61987 1.60421170284 0.243089153857 100.0 2.0
        4 50001 75000 62500 63671 1.71337672516 1.658794214 100.0 2.0
        4 500001 525000 512500 523471 -0.560424391374 -0.560424391374 100.0 1.0
        22 50001 75000 62500 55299 1.80786606545 0.521212731035 100.0 2.0

	*****If you don't run the script properly, the following error statement will be displayed and the program will quit:

		Usage: python markerAnalysis.py inputfilename outputfilename statisticType statisticThreshold minimumNumMarkersPerWindow windowSize
		Example1: python markerAnalysis.py ihs-results-eas.txt ihs-windows ihs 2.0 10 25000
		Example2: python markerAnalysis.py rsb-eas-afr.out rsbEasAfr rsb 2.5 10 25000
		Example3: python markerAnalysis.py rsb-eas-eur.out rsbEasEur rsb 2.5 10 25000
		Example4: python markerAnalysis.py lsbl lsblResults lsbl 0.2 10 25000
		Example5: python markerAnalysis.py commonMarkers lsblResults computeLSBL 0.2 10 25000

TESTING:

	Add your own tests to the markerAnalysisInWindowsTests.py (located in the "Testing" folder) to test various functons of the script markerAnalysisInWindows.py
	To run the tests, simply type the following in the terminal:

		python markerAnalysisInWindowsTests.py

	If all goes well, you should something like:

		test_doWindowsAnalysis (__main__.TestMarkerAnalysisInWindows) ... ok
		test_makeHeader (__main__.TestMarkerAnalysisInWindows) ... ok
		test_makeWindow (__main__.TestMarkerAnalysisInWindows) ... ok
		test_statAverage (__main__.TestMarkerAnalysisInWindows) ... ok
		test_topSignalsCheck (__main__.TestMarkerAnalysisInWindows) ... ok

		----------------------------------------------------------------------
		Ran 5 tests in 0.029s

		OK

	Feel free to add your own tests and modify the markerAnalysisInWindows.py script for improvement.
	For more information, comments, or suggestions, contact me at tapan.shah@mail.utoronto.ca
