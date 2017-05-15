__author__ = 'rramchandani'

import os
import urlparse
import requests
from collections import namedtuple

import logging


Result = namedtuple("Result", "passs fail running config script product rerunpass unsupported")
Verify = namedtuple("Verify", "true false")

RESULT = Result("PASS", "FAIL", "RUNNING", "CONFIG", "SCRIPT", "PRODUCT", "RERUNPASS", "UNSUPPORTED")
VERIFY = Verify("TRUE", "FALSE")


log = logging.getLogger()


class RacetrackError(BaseException): pass


class Racetrack(object):
    """
    Racetrack is a results repository and triage tool. 
    Racetrack is now the de-facto results repository for all UI automation throughout the VMware.
    This is a helper class to access the Racetrack WebServices.
    """

    _url = None

    def __init__(self, server="racetrack.eng.vmware.com", port=443):
        """
        :param server: (str) Racetrack server. Use 'racetrack-dev.eng.vmware.com' for stagging/tests.
         Default: "racetrack.eng.vmware.com"
         
        :param port: (int) Racetrack port. 'racetrack.eng.vmware.com' requires to be connect over port 80.
         Default: 443, for racetrack.eng.vmware.com
        """
        self.server = server
        self.port = port
        self._testset_defaults()
        self._testcase_defaults()

        #try:
        #    check = requests.get(self.url)
        #    if check.status_code != requests.codes.ok:
        #        raise ValueError("Invalid racetrack URL. - {0}".format(self.url))
        #except Exception as err:
        #    raise err.__class__(err.message)

    def _testset_defaults(self):
        self.test_set_id = None
        self.user = None
        self.product = None
        self.description = None
        self.buildid = None
        self.hostos = "127.0.0.1"
        self.branch = None
        self.testtype = "Regression"
        self.language = "English"
        self.buildtype = "ob"

    def _testcase_defaults(self):
        self.feature = None
        self.test_case_id = None
        self.test_case_name = None
        self.result = RESULT.passs

    @property
    def url(self):
        if self._url is None:
            self._url = "http{0}://{1}".format(("s" if self.port == 443 else ""), self.server) \
                        if not self.server.startswith("http") else self.server
        return self._url

    @property
    def test_case_url(self):
        return urlparse.urljoin(self.url, "resultdetails.php?id={0}&resultid={1}&view=false&failonly=No"\
                                .format(self.test_case_id, self.test_set_id))

    def _post(self, method, parameters):
        uri = urlparse.urljoin(self.url, method)

        log.debug("[Racetrack]: Post request.")
        log.debug("  URI:     {0}".format(uri))
        log.debug("  Params:  {0}".format(parameters))

        headers = {"charset": "UTF-8"}

        files = {}

        if parameters.has_key('Screenshot'):
            files['Screenshot'] = parameters['Screenshot']
            del parameters['Screenshot']

        if parameters.has_key('Log'):
            files['Log'] = parameters['Log']
            del parameters['Log']

        response = requests.post(uri, data=parameters, files=files, headers=headers)

        if response.status_code == requests.codes.ok:
            log.debug("[Racetrack]: Post response.")
            log.debug("  Return code:    {0}".format(response.status_code))
            log.debug("  Response data:  {0}".format(response.content))
        else:
            log.error("[Racetrack]: Post response.")
            log.error("  Return code:    {0}".format(response.status_code))
            log.error("  Response data:  {0}".format(response.content))

        return response.content

    def test_set_begin(self, buildid, product, description, user, hostos=None,
                       server_buildid=None, branch=None, buildtype=None, testtype=None, language=None):
        """
        TestSetBegin requests will be a POST request which will return a HTML page with content consisting solely of the ResultSetId.
        Clients should retain this value as it is necessary for other requests.
        If there is an error processing the request, the server will return a 400 or 500 error code with content indicating the error condition.
        The table below shows the parameters that the request is capable of processing, and whether or not those parameters are required.

        Param	        Required?	Description
        BuildID	        Yes	The build number that is being tested
        User	        Yes	The user running the test
        Product	        Yes	The name of the product under test
        Description	    Yes	A description of this test run
        HostOS	        Yes	The Host OS
        ServerBuildID	No	The build number of the "server" product
        Branch	        No	The perforce branch which generated the build
        BuildType	    No	The type of build under test
        TestType	    No	Enum of 'BATS', 'Smoke', 'Regression', 'DBT', 'Performance', 'Stress', 'Scale', 'CBATS', 'Unit' (default 'Regression')
        Language	    No	Enum of 'English', 'Japanese', 'French', 'Italian', 'German', 'Spanish', 'Portuguese', 'Chinese', 'Korean', 'Chinese Simplify', 'Chinese Traditional' (default 'English')
        """
        if not user: user = self.user
        else: self.user = user

        if not hostos: hostos = self.hostos
        else: self.hostos = hostos

        if not buildid: buildid = self.buildid
        else: self.buildid = buildid

        if not product: product = self.product
        else: self.product = product

        if not branch: branch = self.branch
        else: self.branch = branch

        if not buildtype: buildtype = self.buildtype or "ob"
        else: self.buildtype = buildtype

        if not testtype: testtype = self.testtype or "Regression"
        else: self.testtype = testtype

        if not language: language = self.language or "EN"
        else: self.language = language

        params = {
            'BuildID': buildid,
            'User': user,
            'Product': product,
            'Description': description,
            'HostOS': hostos,
            'ServerBuildID': server_buildid,
            'Branch': branch,
            'BuildType': buildtype,
            'TestType': testtype,
            'Language': language
        }
        self.test_set_id = self._post("TestSetBegin.php", parameters=params)

    def test_set_update(self, id=None, buildid=None, user=None, product=None, description=None, hostos=None,
                        server_buildid=None, branch=None, buildtype="ob", testtype="Regression", language="English"):
        """
        TestSetUpdate requests will be a POST request which will return a HTML page with NO content.
        If there is an error processing the request, the server will return a 400 or 500 error code with content indicating the error condition.
        The table below shows the parameters that the request is capable of processing, and whether or not those parameters are required.

        Param	Required?	Description
        ID	Yes	The test set/run that is being completed. ID is returned by a call to #TestSetBegin.
        BuildID	No	The build number that is being tested
        User	No	The user running the test
        Product	No	The name of the product under test
        Description	No	A description of this test run
        HostOS	No	The Host OS
        ServerBuildID	No	The build number of the "server" product
        Branch	No	The perforce branch which generated the build
        BuildType	No	The type of build under test
        TestType	No	Enum of 'BATS', 'Smoke', 'Regression', 'DBT', 'Performance' (default 'Regression')
        Language	No	Enum of 'English', 'Japanese', 'French', 'Italian', 'German', 'Spanish', 'Portuguese', 'Chinese', 'Korean' (default 'English')

        Example
        TestSetUpdate.php?ID=1&BuildID=118412&Product=sim&Description=Svi%3a%3aFunctional%3a%3aPreCheckin%2eWin2k3EntSp1%2eOracle9iR2HostOS=Windows%2003%20Enterprise%20SP1&Type=BATS
        """
        if not id:
            if self.test_set_id is None:
                raise RacetrackError("No active TestSet Id was found. Have you executed 'test_set_begin' first \
                or modified the variable 'test_set_id'?")

            id = self.test_set_id

        params = {
            'ID': id,
            'BuildID': buildid,
            'User': user,
            'Product': product,
            'Description': description,
            'HostOS': hostos,
            'ServerBuildID': server_buildid,
            'Branch': branch,
            'BuildType': buildtype,
            'TestType': testtype,
            'Language': language
        }

        self._post("TestSetUpdate.php", parameters=params)

    def test_set_end(self, id=None):
        """
        TestSetEnd will be a POST request which will return a HTML page with NO content.
        If there is an error processing the request, the server will return a 400 or 500 error code with content indicating the error condition.
        The table below shows the parameters that the request is capable of processing, and whether or not those parameters are required.

        Param	Required?	Description
        ID	Yes	The test set/run that is being completed. ID is returned by a call to #TestSetBegin.

        Example
        TestSetEnd.php?ID=1
        """
        if not id:
            if self.test_set_id is None:
                raise RacetrackError("No active TestSet Id was found. Have you executed 'test_set_begin' first \
                or modified the variable 'test_set_id'?")
            id = self.test_set_id

        params = {
            'ID': id
        }

        self._post("TestSetEnd.php", parameters=params)

        self.test_set_id = None
        self._testset_defaults()

    def test_set_data(self, name, value, result_set_id=None):
        """
        TestSetData will be a POST request which will return a HTML page with content consisting solely of the ResultSetDataId.
        This request associates a Name/Value pair with an existing TestSet. If there is an error processing the request, the server will return a 400 or 500 error code with content indicating the error condition.
        The table below shows the parameters that the request is capable of processing, and whether or not those parameters are required.

        Param	Required?	Description
        ResultSetID	Yes	The test set/run that the data should be associated with. ID is returned by a call to #TestSetBegin.
        Name	Yes	The key in the key/value pair of data.
        Value	Yes	The value in the key/value pair of data.

        Example
        TestSetData.php?ResultSetID=1&Name=ViewComposer&Value=195158
        """
        if not result_set_id:
            if self.test_set_id is None:
                raise RacetrackError("No active TestSet Id was found. Have you executed 'test_set_begin' first \
                or modified the variable 'test_set_id'?")
            result_set_id = self.test_set_id

        params = {
            'ResultSetID': result_set_id,
            'Name': name,
            'Value': value
        }
        result_set_data_id = int(self._post("TestSetData.php", parameters=params))
        return result_set_data_id

    def test_case_begin(self, name, feature, description=None, machine_name=None, tcmsid=None,
                        input_language="EN", gos=None, start_time=None, result_set_id=None):
        """
        Param	Required?	Description
        ResultSetID	Yes	The result set this test case is associated with. ResultSetID is returned by a call to #TestSetBegin.
        Name	Yes	The name of the test case
        Feature	Yes	The feature that is being tested
        Description	No	A description of this test case (defaults to whatever was provided for Name)
        MachineName	No	The host that the test is running against
        TCMSID	No	A comma-separated set of values that correspond to the Testlink Test Case Management System Id's (TCMSID) of this test case.
        InputLanguage	No	The two letter abbreviation for the language used (e.g. 'EN', 'JP')
        GOS	No	The Guest Operating System
        StartTime	No	If not provided, Now() is used.
        """
        if not result_set_id:
            if self.test_set_id is None:
                raise RacetrackError("No active TestSet Id was found. Have you executed 'test_set_begin' first \
                or modified the variable 'test_set_id'?")
            result_set_id = self.test_set_id

        if description is None:
            description = name

        self.test_case_name = name

        params = {
            'ResultSetID': result_set_id,
            'Name': name,
            'Feature': feature,
            'Description': description,
            'MachineName': machine_name,
            'TCMSID': tcmsid,
            'InputLanguage': input_language,
            'GOS': gos,
            'StartTime': start_time
        }

        self.test_case_id = self._post("TestCaseBegin.php", parameters=params)
        return self.test_case_id

    def test_case_update(self, id=None, name=None, feature=None, description=None, machine_name=None, tcmsid=None,
                         input_language="EN", gos=None):
        """
        TestCaseUpdate will be a POST request which will return a HTML page with NO content.
        If there is an error processing the request, the server will return a 400 or 500 error code with content indicating the error condition.
        The table below shows the parameters that the request is capable of processing, and whether or not those parameters are required.

        Param	Required?	Description
        ID	Yes	The ID of the test result to update. ID is returned by a call to #TestCaseBegin.
        Name	No	The name of the test case
        Feature	No	The feature that is being tested
        Description	No	A description of this test case (defaults to whatever was provided for Name)
        MachineName	No	The host that the test is running against
        TCMSID	No	A comma-separated set of values that correspond to the Testlink Test Case Management System Id's (TCMSID) of this test case.
        InputLanguage	No	The two letter abbreviation for the language used (e.g. 'EN', 'JP')
        GOS	No	The Guest Operating System

        Examples
        TestCaseUpdate.php?ResultID=1&MachineName=snc-081
        TestCaseUpdate.php?ResultID=1&TCMSID=102456
        TestCaseUpdate.php?ResultID=1&MachineName=snc-081&TCMSID=102456,102859
        """

        if not id:
            if self.test_set_id is None:
                raise RacetrackError("No active TestSet Id was found. Have you executed 'test_set_begin' first \
                or modified the variable 'test_set_id'?")
            if self.test_case_id is None:
                raise RacetrackError("No active TestCase Id was found. Have you executed 'test_case_begin' first \
                or modified the variable 'test_case_id'?")

            id = self.test_case_id

        if name is not None:
            self.test_case_name = name

        params = {
            'ID': id,
            'Name': name,
            'Feature': feature,
            'Description': description,
            'MachineName': machine_name,
            'TCMSID': tcmsid,
            'InputLanguage': input_language,
            'GOS': gos,
        }

        self._post("TestCaseUpdate.php", parameters=params)

    def test_case_end(self, id=None, result=None, end_time=None):
        """
        TestCaseEnd will be a POST request which will return a HTML page with NO content.
        If there is an error processing the request, the server will return a 400 or 500 error code with content indicating the error condition.
        The table below shows the parameters that the request is capable of processing, and whether or not those parameters are required.

        Param	Required?	Description
        ID	Yes	The test case that is being completed. ID is returned by a call to #TestCaseBegin
        Result	Yes	The result of the test. Enum of 'PASS', 'FAIL', 'RUNNING','CONFIG','SCRIPT','PRODUCT','RERUNPASS', or 'UNSUPPORTED'
        EndTime	No	If not provided, Now() is used.

        Example
        TestCaseEnd.php?ID=1&Result=PASS
        """
        if not id:
            if self.test_set_id is None:
                raise RacetrackError("No active TestSet Id was found. Have you executed 'test_set_begin' first \
                or modified the variable 'test_set_id'?")
            if self.test_case_id is None:
                raise RacetrackError("No active TestCase Id was found. Have you executed 'test_case_begin' first \
                or modified the variable 'test_case_id'?")

            id = self.test_case_id

        if result is None:
            result = self.result
        elif isinstance(result, bool):
            result = RESULT.passs if result else RESULT.fail
        else:
            result = result.upper()

        params = {
            'ID': id,
            'Result': result,
            'EndTime': end_time
        }

        self._post("TestCaseEnd.php", parameters=params)

        self._testcase_defaults()

    def comment(self, description, result_id=None):
        """
        TestCaseComment will be a POST request which will return a HTML page with NO content.
        If there is an error processing the request, the server will return a 400 or 500 error code with content indicating the error condition.
        The table below shows the parameters that the request is capable of processing, and whether or not those parameters are required.

        Param	Required?	Description
        ResultID	Yes	The test case that the comment is being added to. ResultID is returned by a call to #TestCaseBegin.
        Description	Yes	The comment.

        Example
        TestCaseComment.php?ResultID=1&Description=This%20test%20will%20do%20some%20testing
        """
        if not result_id:
            if self.test_set_id is None:
                raise RacetrackError("No active TestSet Id was found. Have you executed 'test_set_begin' first \
                or modified the variable 'test_set_id'?")
            if self.test_case_id is None:
                raise RacetrackError("No active TestCase Id was found. Have you executed 'test_case_begin' first \
                or modified the variable 'test_case_id'?")
            result_id = self.test_case_id

        params = {
            'ResultID': result_id,
            'Description': description
        }

        self._post("TestCaseComment.php", parameters=params)

    def warning(self, description, result_id=None):
        """
        TestCaseWarning is a POST request which will return a HTML page with NO content.
        If there is an error processing the request, the server will return a 400 or 500 error code with content indicating the error condition.
        The table below shows the parameters that the request is capable of processing, and whether or not those parameters are required.

        Param	Required?	Description
        ResultID	Yes	The test case that the comment is being added to. ResultID is returned by a call to #TestCaseBegin.
        Description	Yes	The warning.

        Example
        TestCaseWarning.php?ResultID=1&Description=This%20test%20will%20do%20some%20testing
        """
        if not result_id:
            if self.test_set_id is None:
                raise RacetrackError("No active TestSet Id was found. Have you executed 'test_set_begin' first \
                or modified the variable 'test_set_id'?")
            if self.test_case_id is None:
                raise RacetrackError("No active TestCase Id was found. Have you executed 'test_case_begin' first \
                or modified the variable 'test_case_id'?")
            result_id = self.test_case_id

        params = {
            'ResultID': result_id,
            'Description': description
        }

        self._post("TestCaseWarning.php", parameters=params)

    def screenshot(self, description, screenshot, result_id=None):
        """
        TestCaseComment will be a POST request which will return a HTML page with NO content.
        If there is an error processing the request, the server will return a 400 or 500 error code with content indicating the error condition.
        The table below shows the parameters that the request is capable of processing, and whether or not those parameters are required.

        Param	Required?	Description
        ResultID	Yes	The test case that the comment is being added to. ResultID is returned by a call to #TestCaseBegin.
        Description	Yes	The comment.

        Example
        TestCaseComment.php?ResultID=1&Description=This%20test%20will%20do%20some%20testing
        """
        if not result_id:
            if self.test_set_id is None:
                raise RacetrackError("No active TestSet Id was found. Have you executed 'test_set_begin' first \
                or modified the variable 'test_set_id'?")
            if self.test_case_id is None:
                raise RacetrackError("No active TestCase Id was found. Have you executed 'test_case_begin' first \
                or modified the variable 'test_case_id'?")
            result_id = self.test_case_id

        if not os.path.isfile(screenshot):
            raise IOError("Screenshot path: '{0}' doesn't exists.".format(screenshot))

        params = {
            'ResultID': result_id,
            'Description': description,
            'Screenshot': (os.path.basename(screenshot), open(screenshot, 'rb'))
        }

        self._post("TestCaseScreenshot.php", parameters=params)

    def log(self, description, log, result_id=None):
        """
        TestCaseLog will be a POST request which will return a HTML page with NO content.
        If there is an error processing the request, the server will return a 400 or 500 error code with content indicating the error condition.
        The table below shows the parameters that the request is capable of processing, and whether or not those parameters are required.

        Param	Required?	Description
        ResultID	Yes	The test case that the log is being added to. ResultID is returned by a call to #TestCaseBegin.
        Description	Yes	The description of the log.
        Log	Yes	The logfile

        Example
        TBD - file upload will be POST request, client code samples are probably more useful.
        """
        if not result_id:
            if self.test_set_id is None:
                raise RacetrackError("No active TestSet Id was found. Have you executed 'test_set_begin' first \
                or modified the variable 'test_set_id'?")
            if self.test_case_id is None:
                raise RacetrackError("No active TestCase Id was found. Have you executed 'test_case_begin' first \
                or modified the variable 'test_case_id'?")
            result_id = self.test_case_id

        if not os.path.isfile(log):
            raise IOError("Log path: '{0}' doesn't not exists".format(log))

        params = {
            'ResultID': result_id,
            'Description': description,
            'Log': (os.path.basename(log), open(log, 'rb'))
        }

        self._post("TestCaseLog.php", parameters=params)

    def verify(self, description, actual, expected, screenshot=None, result_id=None):
        """
        TestCaseVerification will be a POST request which will return a HTML page with NO content.
        If there is an error processing the request, the server will return a 400 or 500 error code with content indicating the error condition.
        The table below shows the parameters that the request is capable of processing, and whether or not those parameters are required.

        Param	Required?	Description
        ResultID	Yes	The test case that the verification is being added to. ResultID is returned by a call to #TestCaseBegin.
        Description	Yes	A description of the verification.
        Actual	Yes	The actual value
        Expected	Yes	The expected value.
        Result	Yes	The outcome of the verification. (TRUE or FALSE)
        Screenshot	No	A screenshot associated with the (failed) verification

        Example
        TestCaseVerification.php?ResultID=1&Description=Verify%20VC%20connection%20initialized&Actual=foo&Expected=foo&Result=TRUE
        """
        if not result_id:
            if self.test_set_id is None:
                raise RacetrackError("No active TestSet Id was found. Have you executed 'test_set_begin' first \
                or modified the variable 'test_set_id'?")
            if self.test_case_id is None:
                raise RacetrackError("No active TestCase Id was found. Have you executed 'test_case_begin' first \
                or modified the variable 'test_case_id'?")
            result_id = self.test_case_id

        verification_result = VERIFY.true if actual == expected else VERIFY.false

        if actual == expected and self.result == RESULT.passs:
            self.result = RESULT.passs
        else:
            self.result = RESULT.fail

        params = {
            'ResultID': result_id,
            'Description': description,
            'Actual': actual,
            'Expected': expected,
            'Result': verification_result,
        }

        if screenshot and os.path.exists(screenshot):
            params['Screenshot'] = (os.path.basename(screenshot), open(screenshot, 'rb'))

        self._post("TestCaseVerification.php", parameters=params)



if __name__ == "__main__":
    rt = Racetrack()
    rt.test_set_begin(buildid=12345, user="rramchandani", product="UEM", description="some desc", hostos="10.112.19.19", server_buildid="1234", branch="master")
    print(rt.test_set_id)
    rt.test_set_update(testtype="BATs", buildid=23456)
    rt.test_case_begin("testcase", "feature", "some des", "machine", tcmsid=98765)
    print(rt.test_case_id)
    rt.test_case_update(description="new description")
    rt.comment("some comment")
    rt.warning("some warning")
    rt.verify("some verfication", True, True, screenshot=r"C:\Users\rramchandani\Desktop\ADSites.jpg")
    rt.log("some log", log=r"C:\Users\rramchandani\Desktop\NoAD.xml")
    rt.screenshot(description="screenshot desc", screenshot=r"C:\Users\rramchandani\Desktop\ADSites.jpg")
    rt.verify("second verfication", False, False, screenshot=r"C:\Users\rramchandani\Desktop\ADSites.jpg")
    rt.test_case_end()
    rt.test_set_end()
