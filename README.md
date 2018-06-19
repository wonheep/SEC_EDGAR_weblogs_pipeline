# Insight Data Engineering Coding Challenge

*Author: Wonhee Park*

## Objective
Parse through a sample SEC EDGAR weblog file and output a summarized log of sessions into a .txt file. 

## Repo Structure 
├── README.md 
    ├── run.sh
    ├── src
    │   └── sessionization.py
    │   └── sessionObject.py
    ├── input
    │   └── inactivity_period.txt
    │   └── log.csv
    ├── output
    |   └── sessionization.txt
    ├── insight_testsuite
        └── run_tests.sh
        └── tests
            └── test_1
            |   ├── input
            |   │   └── inactivity_period.txt
            |   │   └── log.csv
            |   |__ output
            |   │   └── sessionization.txt
            ├── test_2
                ├── input
                |  └── inactivity_period.txt
                │  └── log.csv
                |__ output
                │   └── sessionization.txt

### Inputs
* `log.csv` EDGAR weblog data 
	* IP address (unique user)
	* Datetime of request
	* document key = cik+accession+extension

* `inactivity_period.txt` time of inactivity unitl session ends in seconds

### Output
* `sessionization.txt` each line records a user session with below stats
	* IP address (user)
	* first document request datetime
	* last document request datetime
	* duration of session in seconds 
	* number of documents requested

## Requirements
* duration of a session is inclusive
* last timestamp of the input file will close out all active sessions
* session ends after certain amt of time of inactivity 

## Design Choices
* created `class sessionObjects` to define a session. I implemented object-oriented programming because I wanted to keep track of a given IP Address's many requests and corresponding request times without making use of multiple hashmaps. I include only one hashmap which uses the IP address as the key and its value is a session object. 
* The session object has thefollowing attributes:
	* IP address
	* list of all request times in both datetime and string form
	* list of documents requested
	* updated count of number of document requests. I thought it was best to 
```Python
class Session(Object):
	def __init__(self, ipAddress, startDatetimes, startDatetimesStr, documentList, activeStatus):
			self.ipAddress = ipAddress
			self.startDatetimes = [startDatetimes]
			self.startDatetimesStr = [startDatetimesStr]
			self.documentList = [documentList]
			self.numRequests = len(self.documentList)
```
* The realtime reporting is mimiced via this logic: after each line from input file is read it creates a new session object or updates an existing session object based on IP key and keeps track of the "current time", aka the current line being processed. 
* After every create or update of a session object it goes into `outputFinishedSessions()` and reiterates through the existing hashmap to recalculate which users have been inactive. the program  checks to see if any elements in the hashmap has been inactive for n seconds (n = time in seconds provided by inactivity_period.txt) or if the current time being read has already reached the final timestamp in the input file, then writes to the output file after a session ends and deletes that element from the hashmap. 
* I aimed to modularize the program to reduce redundant operations

## Dependencies
* written in `python3`, shell scripts reflect this change
	* if you've installed multiple python versions, you can set python alias to be python3 in bash_profile
* Libraries
	* `datetime` used to calculate time elapsed in seconds in a given session
	* `sys` used to read/write from/to files on local machine 
* developed on unix-like machine

## Run Instructions
* to run from your main grading directory, run command: './run.sh'
* to run unit tests, run command: './run_tests.sh'
* you can run the python command directly on terminal: `python3 ./src/sessionization.py ./input/log.csv ./input/inactivity_period.txt ./output/sessionization.txt`


## Testing
* created method functions to display session attributes 
* primarily used print statements to debug, commented throughout the code
* varied the second unit test minimally and verified via manual verification 

## Things to Note
* array DS for the startDatetime(Str) and documentList attributes are not needed, takes up more space. I could have sufficed with having startDatetime only be the lastest startDateTime requested and gotten rid of documentList to save space. However, I used these extra details for debugging purposes. DocumentList can continue to use an array DS if we want to handle edge case where a user requests same document twice in a session and the program needs to differentiate unique documents. 
* Though I downloaded sample EDGAR weblog files, I did not test to see how my program handles large datasets. 
* I did not test the program on any linux distributions
