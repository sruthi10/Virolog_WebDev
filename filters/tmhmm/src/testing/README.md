To get the data from TMHMM filter and plot the data in graphs:

(1) Execute "python longTest.py" from command line. Make sure the opt\_short in the tmhmm/bin/tmhmmformat.pl file is set to 0 in order to get long output.

(2) Output and CSV results will be in testOut.txt and testCsv.csv respectively. Scripts to create gnuplots and the corresponding data for each protein will be in a TMHMM\_#### file where # can be any random number.

(3) Execute "python plotTest.py" from command line. This will execute the plot scripts and save the jpg graphs in the "plots" directory.

OR

(1) Execute "python fullTest.py" to call TMHMM filter and graph the results all in one go. Resulting graphs will be in "plots" directory.

**Make sure "source tmhmmPath.sh" was executed first.**
