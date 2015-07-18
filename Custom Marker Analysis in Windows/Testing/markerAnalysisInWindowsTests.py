import markerAnalysisInWindows
import unittest
import subprocess

class TestMarkerAnalysisInWindows(unittest.TestCase):
    '''extends unittest.TestCase class '''

    def setUp(self):
        self.outputFile="s"

    def test_makeHeader(self):
        output = open("testFile",'w') 
        markerAnalysisInWindows.makeHeader(output)
        output.close()

        headerFile=open("testFile", 'r')
        headerLine=headerFile.readline()
        self.assertEqual(headerLine, "Chr Start End CenterPos positionOfMaxStatValue maxStatValue avgStatValue %TopSignals numSignals\n")
        headerFile.close()

    def test_topSignalsCheck(self):
        #topSignalCheck(statisticType, statValue, threshold, tempWindowStatValue=False)

        #ihs w/o tempWindowStatValue signal test 
        result= markerAnalysisInWindows.topSignalCheck("ihs", 3, -2.0)
        self.assertEqual(result, True)

        #rsb w/o tempWindowStatValue non-signal test
        result= markerAnalysisInWindows.topSignalCheck("rsb", 1, 1.5)
        self.assertEqual(result, False)

        #ihs with abs(statVal) > tempWindowStatValue
        result= markerAnalysisInWindows.topSignalCheck("ihs", -3, 2.0, 0.5)
        self.assertEqual(result, True)

        #rsb with statVal < tempWindowStatValue
        result= markerAnalysisInWindows.topSignalCheck("rsb", 3, 2.0, 31)
        self.assertEqual(result, False)

        #lsbl w/o tempWindowStatValue signal test
        result= markerAnalysisInWindows.topSignalCheck("lsbl", 3, 2.0)
        self.assertEqual(result, True)

        #lsbl w/o tempWindowStatValue non-signal test
        result= markerAnalysisInWindows.topSignalCheck("lsbl", -3, 2.0)
        self.assertEqual(result, False)

    def test_statAverage(self):

        #empty list test
        statList=[]
        result= markerAnalysisInWindows.stat_average(statList)
        self.assertEqual(result, 0)

        #1 element test
        statList=[1.2323]
        result= markerAnalysisInWindows.stat_average(statList)
        self.assertEqual(result, statList[0])

        #2 elements test (position + negative)
        statList=[-1.2323, 1.2323]
        result= markerAnalysisInWindows.stat_average(statList)
        self.assertEqual(result, 0)

        #various elements test
        statList=[0.0369926698929385, 0.062407172144715001, 0.062407172144715001, 0.79025022282864699, 0.75152514789574498, 0.806488988093786, 0.047264763166828698, 0.068495011105816198, 2.5902361145250401, 0.041490753614489402, 0.057387186241032402, 0.040672423901060802, 0.78594430394751402, 0.81377436219966504, 0.040471259321746202, 0.73859313932828397, 0.26120787535717899, 0.26120787535717899, 0.26120787535717899, 0.165223419963966, 0.116892123836134, 0.68123646092025003, 0.18224884387628301, 0.74739381056548604, 0.445759117409393, 0.11762888936909, 0.85750124483779799, 0.069816732215584501, 0.53471846404974299, 0.19672404239122901, 0.45421064239062098, 0.54935117476115203, 0.38722941792638299, 0.30338866414462101, 0.30338866414462101, 0.458599163536552, 0.30338866414462101]
        result= markerAnalysisInWindows.stat_average(statList)
        self.assertEqual(result, sum(statList)/float(len(statList)))

    def test_makeWindow(self):
        #makeWindow(row, ws, winNum, avgStatValue, topSignals, numSignals)
        #Chr Start End CenterPos positionOfMaxStatValue maxStatValue avgStatValue %TopSignals numSignals

        #Arbitrary values test
        row=["2", "24433", "3.4", "randomeStuff", "morerandomness"]
        ws=25000
        winNum=0
        avgStatValue=2.3
        topSignals=3
        numSignals=12

        expectedWindow=[2, 1, 25000, 12500, 24433, 3.4, 2.3, float(topSignals/numSignals)*100.0, numSignals]
        actualWindow= markerAnalysisInWindows.makeWindow(row, ws, winNum, avgStatValue, topSignals, numSignals)
        self.assertEqual(actualWindow, expectedWindow)

    def test_doWindowsAnalysis(self):

        ###########################################################################################
        #Input with multiple chromosomes & positions, and default parameters test       
        ###########################################################################################

        #input file "basicInput", has the following contents:
            # "CHR" "POSITION" "iHS" "Pvalue"
            # 1 30923 1.04646745936215 0.529669992989166
            # 2 54421 1.25894778451328 0.681833965351423
            # 3 60726 -1.11803339512159 0.579132479473
            # 3 61987 1.60421170283546 0.963900739824788
            # 4 523471 -0.560424391373736 0.240188674280158
            # 4 61989 1.60421170283546 0.963900739824788
            # 4 63671 1.71337672515842 1.06226523877241
            # 22 55299 1.80786606544976 1.15102709843734
            # 22 55326 -0.76544060338033 0.352608008938557

        #Actual Expected Output is saved in file "outputActual". It has the following contents:
            # Chr Start End CenterPos positionOfMaxStatValue maxStatValue avgStatValue %TopSignals numSignals
            # 1 25001 50000 37500 30923 1.04646745936 1.04646745936 100.0 1.0
            # 2 50001 75000 62500 54421 1.25894778451 1.25894778451 100.0 1.0
            # 3 50001 75000 62500 61987 1.60421170284 0.243089153857 100.0 2.0
            # 4 50001 75000 62500 63671 1.71337672516 1.658794214 100.0 2.0
            # 4 500001 525000 512500 523471 -0.560424391374 -0.560424391374 100.0 1.0
            # 22 50001 75000 62500 55299 1.80786606545 0.521212731035 100.0 2.0

        basicInput=open("basicInput", 'r')

        #Let's produce experimental output 
        output=open("outputExperimental", 'w')
        markerAnalysisInWindows.doWindowsAnalysis(basicInput, output, 25000, "ihs", 0.0, 0)    

        #check if there is any differences in the files being created
        ## if there is any difference between the two files, the lines that are different will be spit out in the shell
        subprocess.Popen('diff outputActual outputExperimental', shell=True)
        basicInput.close()
        output.close()
        
        #####################
        #ADD OTHER TESTS HERE 
        #####################

suite = unittest.TestLoader().loadTestsFromTestCase(TestMarkerAnalysisInWindows)
unittest.TextTestRunner(verbosity=2).run(suite)