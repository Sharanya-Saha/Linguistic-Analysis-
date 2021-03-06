--------------------------
CS685A ASSIGNMENT 2 README
--------------------------

Assignment 2 for CS685A: Data Mining by Sharanya Saha (21111056).
The assignment is coded in python 3.8.10 and requires the installation of the following packages:
	-> numpy
	-> pandas
	-> scipy
	-> openpyxl
The required packages can be installed using the following command:
	pip install -r requirements.txt	


ALERT: assign2.sh runs the complete assignment (Q1 to Q9) and takes around 40 seconds. It shows some warnings in the terminal, Kindly ignore them.

To make the scripts executable please run the command chmod u+x scriptname.sh
To run the scripts write ./scriptname.sh in the terminal.

--------
CONTENTS
--------
   
	1. The folder contains 23 files and 2 folders named datasets and Outputs
		1.1. 11 shell files
		1.2. 10 Python files
		1.3. 2 txt files 
			1.3.1. README.txt
			1.3.2. requirements.txt
		1.4. Folders
			1.4.1. Datasets
			1.4.2. Outputs
		
		
The folder 'Datasets' contains all the 5 input files and 6 other folders(region wise) required for execution :
- All the files are downloaded from  https://censusindia.gov.in/2011Census/Language_MTs.html
- There are 6 folders which contains the datasets for Question 7. It is stored in region wise format for ease of execution of the code.
The folder 'Outputs' will contain the resultant csv generated by the code.

-----
NOTE:
-----
-Please do not modify the folder structures, it may break the code. 
-Please use python 3.8.10 or higher for smooth functioning of the code.

--------------------------------------------------
QUESTION WISE INPUT, EXECUTABLE AND OUTPUT FILES : 
--------------------------------------------------


COMMON ASSUMPTIONS:
-------------------

- Number of monolingual speakers for a state/ut is calculated as: Population of that state/ut - Number of people speaking 2 or more languages.
- Census file is used to find the total population for a state/ut.
- The number of people speaking exactly two languages are calculated as: Number of people speaking two or more languages - Number of people speaking three or more languages.

		
Question 1:
-----------

-> Input files:
	-> DDW-C18-0000.xlsx
	-> DDW_PCA0000_2011_Indiastatedist.xlsx
-> Executable file: percent-india.sh (which calls DM_Q1.py)
-> Output file: percent-india.csv 


Question 2:
-----------

-> Input files: 
	-> DDW-C18-0000.xlsx
	-> DDW_PCA0000_2011_Indiastatedist.xlsx
-> Executable file: gender-india.sh (calls DM_Q2.py)
-> Output files: 
	-> gender-india-a.csv (For monolinguals)
	-> gender-india-b.csv (For bilinguals)
	-> gender-india-c.csv (For trilinguals)

P-values are calculated using t-test. T-test is done on two vectors: Vector 1 contains Male:Female ratio for monolinguals, bilinguals and trilinguals for a state/ut and Vector 2 contains Male:Female population ratio for the same state/ut taken thrice.
NULL Hypothesis: There is no significant difference between the numbers of male and female. 
The threshold(alpha) is 0.05 and the NULL hpothesis gets rejected of p-value is less than alpha. For none of the states, p-value is less than alpha and hence, NULL hypothesis is accepted. 

Question 3:
-----------

-> Input files:
	-> DDW-C18-0000.xlsx
	-> DDW_PCA0000_2011_Indiastatedist.xlsx
-> Executable file: geography-india.sh (which calls DM_Q3.py) 
-> Output files:
	-> geography-india-a.csv (For monolinguals)
	-> geography-india-b.csv (For bilinguals)
	-> geography-india-c.csv (For trilinguals)

P-values are calculated using t-test. T-test is done on two vectors: Vector 1 contains Urban:Rural ratio for monolinguals, bilinguals and trilinguals for a state/ut and Vector 2 contains Urban:Rural population ratio for the same state/ut taken thrice.
NULL Hypothesis: There is no significant difference between the numbers of urban and rural. 
The threshold(alpha) is 0.05 and the NULL hpothesis gets rejected of p-value is less than alpha. For none of the states, p-value is less than alpha and hence, NULL hypothesis is accepted. 


Question 4:
-----------

-> Input files:
	-> DDW-C18-0000.xlsx
	-> DDW_PCA0000_2011_Indiastatedist.xlsx
-> Executable files: 
	-> 3-to-2-ratio.sh (which calls DM_Q4.py)
	-> 2-to-1-ratio.sh (which calls DM_Q4_2.py)
-> Output files:
	-> 3-to-2-ratio.csv
	-> 2-to-1-ratio.csv
	
The output contains 6 state-codes. First three rows contain the top-3 states sorted by higher to lower ratio followed by the worst 3 states sorted by lower to higher ratio.

Question 5:
-----------

-> Input files: 
	-> DDW-C18-0000.xlsx
	-> DDW-0000C-14.xls
-> Executable file: age-india.sh (which calls DM_Q5.py)
-> Output file:
	-> age-india.csv

In order to match the age-groups in both the data files, the age-groups in C-14 are merged. C-14 contains finer age-groups (i.e 30-34, 35-39,...) which are merged to form a larger age group (30-49) in order to match with C-18. Similarly, finer age groups between 50-69 are also merged. All the age groups above 70 are merged into a single age-group i.e. 70+.
C-14 also contains an age-group of 0-4 which is absent in C-18, so it has been ignored.
The age-group 'age not stated' is also ignored. The final age-groups taken into consideration are 5-9, 10-14, 15-19, 20-24, 25-29, 30-49, 50-69 and 70+.


Question 6:
-----------	

-> Input files: 
	-> DDW-C19-0000.xlsx
	-> DDW-0000C-08.xlsx
-> Executable file: literacy-india.sh (which calls DM_Q6.py)
-> Output file:
	-> literacy-india.csv

Literacy group 'literate' has finer subdivisions hence, 'literate' is not reported seperately as a literacy group. Matric/Secondary, Higer Secondary, Non-Technical Diploma, Technical Diploma are merged to form a larger literacy group named 'Matric/Secondary but below graduate' from C-08 file in order to match with the C-19 file.

Question 7:
-----------

-> Input files: The data files required are organised in region wise folders.
-> Executable file: region-india.sh (which calls DM_Q7.py)
-> Output files: 
	-> region-india-a.csv
	-> region-india-b.csv

C-17 files are used for this question and all the files are organised in region wise folders. The folder organisation is important for the code to execute smoothly. Ladakh and Telengana could not be included seperately as the data specific to these UTs are not available.

Question 8:
-----------

-> Input files: 
	-> DDW-C18-0000.xlsx
	-> DDW-0000C-14.xls
-> Executable file: age-gender.sh (which calls DM_Q8.py)
-> Output files:
	-> age-gender-a.csv (For trilinguals)
	-> age-gender-b.csv (For bilinguals)
	-> age-gender-c.csv (For monolinguals)

In order to match the age-groups in both the data files, the age-groups in C-14 are merged. C-14 contains finer age-groups (i.e 30-34, 35-39,...) which are merged to form a larger age group (30-49) in order to match with C-18. Similarly, finer age groups between 50-69 are also merged. All the age groups above 70 are merged into a single age-group i.e. 70+.
C-14 also contains an age-group of 0-4 which is absent in C-18, so it has been ignored.
The age-group 'age not state' is also ignored. The final age-groups taken into consideration are 5-9, 10-14, 15-19, 20-24, 25-29, 30-49, 50-69 and 70+.


Question 9:
-----------

-> Input files:
	-> DDW-C19-0000.xlsx
	-> DDW-0000C-08.xlsx
-> Executable file: literacy-gender.sh (which calls DM_Q9.py)
-> Output files: 
	-> literacy-gender-a.csv (For trilinguals)
	-> literacy-gender-b.csv (For bilinguals)
	-> literacy-gender-c.csv (For monolinguals)

Literacy group 'literate' has finer subdivisions so 'literate' is not reported seperately as a literacy group. Matric/Secondary, Higer Secondary, Non-Technical Diploma, Technical Diploma are merged to form a larger literacy group named 'Matric/Secondary but below graduate' from C-08 file in order to match with the C-19 file.


---------
RUN TIME:
---------
The runtime for assign2.sh in personal system is around 40 seconds. Please let the script run for twice the time mentioned in worst case scenario.


----------------
CONTACT DETAILS:
----------------
Sharanya Saha
Roll Number: 21111056
Please contact on sharanya21@iitk.ac.in or sharanyasaha99@gmail.com for any queries.






