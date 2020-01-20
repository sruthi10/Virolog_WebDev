To run the tmhmm.py program:

(1) Do "source tmhmmPath.sh" to add the tmhmm command to your environment path. 

(2) The tmhmmPath.sh file may need to be edited to change the path to point to your current folder with the tmhmm/bin/tmhmm file. (Make sure path is full path (starting from root directory)).

(3) Edit the "inputfile" variable in tmhmm.py file to reflect the name of the input file you want to perform TMHMM filter on. The file should be a .faa file.

(4) Edit the "txt_file" variable to be the text output file you desire, and change "csv_file" to be the CSV output file you desire. Change the name when running a new inputfile so other results don't get overridden, unless you edit the file to append to an existing text and CSV file.

(5) If you want long and detailed output, go into filters/tmhmm/bin/tmhmmformat.pl and edit line 20 so the short option can be 0 (meaning false). If you want short output (which results in faster execution and is what tmhmm.py is built to expect), edit line 20 of the tmhmmformat.pl file to equal 1. If you want plots to be made, line 21 of tmhmmformat.pl should be 1, else 0 if you do not want plots.

(6) Run "python tmhmm.py" on the command line, making sure the .faa file is in the same folder.

(7) Results will be appended in tmhmmResults.txt file. Results will be converted to tmhmmResults.csv file as well.
