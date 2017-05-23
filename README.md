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
[TestSetBegin](#testsetbegin) <br />
[TestSetUpdate](#testsetupdate) <br />
[TestSetEnd](#testsetend) <br />
[TestSetData](#testsetdata) <br />
[TestCaseBegin](#testcasebegin) <br />
[TestCaseUpdate](#testcaseupdate) <br />
[TestCaseEnd](#testcaseend) <br />
[TestCaseComment](#testcasecomment) <br />
[TestCaseVerification](#testcaseverification) <br />
[TestCaseWarning](#testcasewarning) <br />
[TestCaseScreenshot](#testcasescreenshot) <br />
[TestCaseLog](#testcaselog) <br />

### TestSetBegin

__Racetrack.test_set_set_begin__

```python
    def test_set_begin(self, buildid, product, description, user, hostos=None,
                       server_buildid=None, branch=None, buildtype=None, testtype=None, language=None):
        ...
```
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
|testtype	    |No	|Enum of 'BATS', 'Smoke', 'Regression', 'DBT', 'Performance', 'Stress', 'Scale', 'CBATS', 'Unit' (default **Regression**)|
|language	    |No	|Enum of 'English', 'Japanese', 'French', 'Italian', 'German', 'Spanish', 'Portuguese', 'Chinese', 'Korean', 'Chinese Simplify', 'Chinese Traditional' (default **English**)|

[top](#index) <br />


### TestSetUpdate

__Racetrack.test_set_update__

```python
    def test_set_update(self, id=None, buildid=None, user=None, product=None, description=None, hostos=None,
                        server_buildid=None, branch=None, buildtype="ob", testtype="Regression", language="English"):
        ...
```
TestSetUpdate requests will be a POST request which will return a HTML page with NO content.
If there is an error processing the request, the server will return a 400 or 500 error code with content indicating the error condition.
The table below shows the parameters that the request is capable of processing, and whether or not those parameters are required.

|Param	        |Required?	|Description|
|---------------|:---------:| ---------|
|id|	Yes (optional)|	The test set/run that is being completed. ID is returned by a call to #TestSetBegin.|
|buildid|	No|	The build number that is being tested|
|user|	No|	The user running the test|
|product|	No|	The name of the product under test|
|description|	No|	A description of this test run|
|hostos|	No|	The Host OS|
|server_buildid|	No|	The build number of the "server" product|
|branch|	No|	The perforce branch which generated the build|
|buildtype|	No|	The type of build under test|
|testtype|	No|	Enum of 'BATS', 'Smoke', 'Regression', 'DBT', 'Performance' (default 'Regression')|
|language|	No|	Enum of 'English', 'Japanese', 'French', 'Italian', 'German', 'Spanish', 'Portuguese', 'Chinese', 'Korean' (default 'English')|

[top](#index) <br />


### TestSetEnd

__Racetrack.test_set_end__

```python
    def test_set_end(self, id=None):
        ...
```

TestSetEnd will be a POST request which will return a HTML page with NO content.
If there is an error processing the request, the server will return a 400 or 500 error code with content indicating the error condition.
The table below shows the parameters that the request is capable of processing, and whether or not those parameters are required.

|Param	        |Required?	|Description|
|---------------|:---------:| ---------|
|id|	Yes (optional)|	The test set/run that is being completed. ID is returned by a call to #TestSetBegin.|

[top](#index) <br />


### TestSetData

__Racetrack.test_set_data__

```python
    def test_set_data(self, name, value, result_set_id=None):
        ...
```

TestSetData will be a POST request which will return a HTML page with content consisting solely of the ResultSetDataId.
This request associates a Name/Value pair with an existing TestSet.
If there is an error processing the request, the server will return a 400 or 500 error code with content indicating the error condition.
The table below shows the parameters that the request is capable of processing, and whether or not those parameters are required.

|Param	        |Required?	|Description|
|---------------|:---------:| ---------|
|result_set_id|	Yes (optional)|	The test set/run that the data should be associated with. ID is returned by a call to #TestSetBegin.|
|name|	Yes|	The key in the key/value pair of data.|
|value|	Yes|	The value in the key/value pair of data.|

[top](#index) <br />


### TestCaseBegin

__Racetrack.test_case_begin__

```python
    def test_case_begin(self, name, feature, description=None, machine_name=None, tcmsid=None,
                        input_language="EN", gos=None, start_time=None, result_set_id=None):
        ...
```

|Param	        |Required?	|Description|
|---------------|:---------:| ---------|
|result_set_id|	Yes (optional)|	The result set this test case is associated with. ResultSetID is returned by a call to #TestSetBegin.|
|name|	Yes|	The name of the test case|
|feature|	Yes|	The feature that is being tested|
|description|	No|	A description of this test case (defaults to whatever was provided for Name)|
|machine_name|	No|	The host that the test is running against|
|tcmsid|	No|	A comma-separated set of values that correspond to the Testlink Test Case Management System Id's (TCMSID) of this test case.|
|input_language|	No|	The two letter abbreviation for the language used (e.g. 'EN', 'JP')|
|gos|	No|	The Guest Operating System|
|start_time|	No|	If not provided, Now() is used.|

[top](#index) <br />


### TestCaseUpdate

__Racetrack.test_case_update__

```python
     def test_case_update(self, id=None, name=None, feature=None, description=None, machine_name=None, tcmsid=None,
                         input_language="EN", gos=None):
        ...
```

TestCaseUpdate will be a POST request which will return a HTML page with NO content.
If there is an error processing the request, the server will return a 400 or 500 error code with content indicating the error condition.
The table below shows the parameters that the request is capable of processing, and whether or not those parameters are required.

|Param	        |Required?	|Description|
|---------------|:---------:| ---------|
|id|	Yes (optional)|	The ID of the test result to update. ID is returned by a call to #TestCaseBegin.|
|name|	No|	The name of the test case|
|feature|	No|	The feature that is being tested|
|description|	No|	A description of this test case (defaults to whatever was provided for Name)|
|machine_name|	No|	The host that the test is running against|
|tcmsid|	No|	A comma-separated set of values that correspond to the Testlink Test Case Management System Id's (TCMSID) of this test case.|
|input_language|	No|	The two letter abbreviation for the language used (e.g. 'EN', 'JP')|
|gos|	No|	The Guest Operating System|

[top](#index) <br />


### TestCaseEnd

__Racetrack.test_case_end__

```python
     def test_case_end(self, id=None, result=None, end_time=None):
        ...
```

TestCaseEnd will be a POST request which will return a HTML page with NO content.
If there is an error processing the request, the server will return a 400 or 500 error code with content indicating the error condition.
The table below shows the parameters that the request is capable of processing, and whether or not those parameters are required.

|Param	        |Required?	|Description|
|---------------|:---------:| ---------|
|id|	Yes (optional)|	The test case that is being completed. ID is returned by a call to #TestCaseBegin|
|result|	Yes|	The result of the test. Enum of 'PASS', 'FAIL', 'RUNNING','CONFIG','SCRIPT','PRODUCT','RERUNPASS', or 'UNSUPPORTED'|
|end_time|	No|	If not provided, Now() is used.|

[top](#index) <br />


### TestCaseComment

__Racetrack.test_case_end__

```python
     def comment(self, description, result_id=None):
        ...
```

TestCaseComment will be a POST request which will return a HTML page with NO content.
If there is an error processing the request, the server will return a 400 or 500 error code with content indicating the error condition.
The table below shows the parameters that the request is capable of processing, and whether or not those parameters are required.

|Param	        |Required?	|Description|
|---------------|:---------:| ---------|
|result_id|	Yes (optional)|	The test case that the comment is being added to. ResultID is returned by a call to #TestCaseBegin.|
|description|	Yes|	The comment.|

[top](#index) <br />


### TestCaseVerification

__Racetrack.verify__

```python
     def verify(self, description, actual, expected, screenshot=None, result_id=None):
        ...
```

TestCaseVerification will be a POST request which will return a HTML page with NO content.
If there is an error processing the request, the server will return a 400 or 500 error code with content indicating the error condition.
The table below shows the parameters that the request is capable of processing, and whether or not those parameters are required.

|Param	        |Required?	|Description|
|---------------|:---------:| ---------|
|ResultID|	Yes (optional)|	The test case that the verification is being added to. ResultID is returned by a call to #TestCaseBegin.|
|Description|	Yes|	A description of the verification.|
|Actual|	Yes|	The actual value|
|Expected|	Yes|	The expected value.|
|Result|	Yes|	The outcome of the verification. (TRUE or FALSE)|
|Screenshot|	No|	A screenshot associated with the (failed) verification|

[top](#index) <br />


### TestCaseWarning

__Racetrack.warning__

```python
     def warning(self, description, result_id=None):
        ...
```

TestCaseWarning is a POST request which will return a HTML page with NO content.
If there is an error processing the request, the server will return a 400 or 500 error code with content indicating the error condition.
The table below shows the parameters that the request is capable of processing, and whether or not those parameters are required.

|Param	        |Required?	|Description|
|---------------|:---------:| ---------|
|result_id|	Yes (optional)|	The test case that the comment is being added to. ResultID is returned by a call to #TestCaseBegin.|
|description|	Yes|	The warning.|

[top](#index) <br />


### TestCaseScreenshot

__Racetrack.screenshot__

```python
     def screenshot(self, description, screenshot, result_id=None):
        ...
```

TestCaseScreenshot will be a POST request which will return a HTML page with NO content.
If there is an error processing the request, the server will return a 400 or 500 error code with content indicating the error condition.
The table below shows the parameters that the request is capable of processing, and whether or not those parameters are required.

|Param	        |Required?	|Description|
|---------------|:---------:| ---------|
|result_id|	Yes (optional)|	The test case that the comment is being added to. ResultID is returned by a call to #TestCaseBegin.|
|description|	Yes|	The comment.|
|screenshot|   Yes|     Screenshot/Image file path|

[top](#index) <br />


### TestCaseLog

__Racetrack.log__

```python
     def log(self, description, log, result_id=None):
        ...
```

TestCaseLog will be a POST request which will return a HTML page with NO content.
If there is an error processing the request, the server will return a 400 or 500 error code with content indicating the error condition.
The table below shows the parameters that the request is capable of processing, and whether or not those parameters are required.

|Param	        |Required?	|Description|
|---------------|:---------:| ---------|
|result_id|	Yes (optional)|	The test case that the log is being added to. ResultID is returned by a call to #TestCaseBegin.|
|description|	Yes|	The description of the log.|
|log|	Yes|	The logfile|

[top](#index) <br />


For more information please visit, https://wiki.eng.vmware.com/RacetrackWebServices
