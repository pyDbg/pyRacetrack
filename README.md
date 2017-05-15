# What is Racetrack?
Racetrack is a results repository and triage tool. 
Racetrack is now the de-facto results repository for all UI automation throughout the VMware.

# pyRacetrack
Racetrack Web services helper.

## Getting started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Installing

Clone the project in your local directory.
```
git clone https://github.com/rocky1109/pyRacetrack.git
cd pyRacetrack
```

Now install/build it using **setup.py** file as
```
python setup.py install
```

This will install the package for your current python environment.

### Example
```python
>> from pyRacetrack import Racetrack
>>
>> racetrack = Racetrack(server="racetrack-dev.eng.vmware.com", port=80)
>>
>> racetrack.test_set_begin(buildid=91023, product="product_name", description="My product description", 
...                         user="rramchandani", hostos="10.112.19.17", testtype="Smoke", language="EN")
>> racetrack.test_set_id
1012549
>>
>> racetrack.test_case_begin(name="TestCase Name", feature="Feature", description="Description of my testcase", 
...                          machine_name="W7x64_1", tcmsid=31205, gos="Microsoft Windows 7 (64-bit)")
>>
>> racetrack.comment(description="My comments for the testcase")
>> racetrack.verify(description="My verification statement", actual="This Value", expected="That Value")
>>
>> racetrack.log(description="Here's description about my log file", log="./path/towords/my/log/file")
>>
>> racetrack.test_case_url()
https://racetrack-dev.eng.vmware.com/resultdetails.php?id=1012549&resultid=3500617&view=false&failonly=No
>>
>> racetrack.test_case_end()
>> racetrack.test_set_end()
```

## Index
[TestSetBegin](TestSetBegin) <br />
[TestSetUpdate](TestSetUpdate) <br />
[TestSetEnd](TestSetEnd) <br />
[TestSetData](TestSetData) <br />
[TestCaseBegin](TestCaseBegin) <br />
[TestCaseUpdate](TestCaseUpdate) <br />
[TestCaseEnd](TestCaseEnd) <br />
[TestCaseComment](TestCaseComment) <br />
[TestCaseVerification](TestCaseVerification) <br />
[TestCaseWarning](TestCaseWarning) <br />
[TestCaseScreenshot](TestCaseScreenshot) <br />
[TestCaseLog](TestCaseLog) <br />

### TestSetBegin
TestSetBegin requests will be a POST request which will return a HTML page with content consisting solely of the ResultSetId. <br />
Clients should retain this value as it is necessary for other requests. <br />
If there is an error processing the request, the server will return a 400 or 500 error code with content indicating the error condition. <br />
The table below shows the parameters that the request is capable of processing, and whether or not those parameters are required. <br />

|Param	        |Required?	|Description|
|---------------|:---------:| ---------|
|buildid	        |Yes	|The build number that is being tested|
|user	        |Yes	|The user running the test|
|product	        |Yes	|The name of the product under test|
|description	    |Yes	|A description of this test run|
|hostos	        |Yes	|The Host OS|
|serverbuildid	|No	|The build number of the "server" product|
|branch	        |No	|The perforce branch which generated the build|
|buildtype	    |No	|The type of build under test|
|testtype	    |No	|Enum of 'BATS', 'Smoke', 'Regression', 'DBT', 'Performance', 'Stress', 'Scale', 'CBATS', 'Unit' (default 'Regression')|
|language	    |No	|Enum of 'English', 'Japanese', 'French', 'Italian', 'German', 'Spanish', 'Portuguese', 'Chinese', 'Korean', 'Chinese Simplify', 'Chinese Traditional' (default 'English')|

### TestSetBegin
### TestSetUpdate
### TestSetEnd
### TestSetData
### TestCaseBegin
### TestCaseUpdate
### TestCaseEnd
### TestCaseComment
### TestCaseVerification
### TestCaseWarning
### TestCaseScreenshot
### TestCaseLog

For more information please visit, https://wiki.eng.vmware.com/RacetrackWebServices
