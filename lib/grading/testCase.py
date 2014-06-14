
# Class for storing information about test cases from assignment.json


class TestCase:

    # If extracredit, these points are added in addition to the total points
    extracredit = False

    # The command to run the student written portion of a test case
    # This command is run as an untrusted user
    run = None

    # The name of the test case
    title = None

    # The command to grade the test case output, run as trusted user
    grade = None

    # Command to compile assignment, run as trusted user
    compile = None

    # The number of points this test case is worth
    points = None

    # Information for the user about this test case
    details = ""

    # If hidden, this test case is not shown to the user
    hidden = False

    # TODO add steps

    def __init__(self, testCaseJson):

        if "extracredit" in testCaseJson:
            self.extracredit = testCaseJson["extracredit"]

        if "hidden" in testCaseJson:
            self.hidden = testCaseJson["hidden"]

        try:
            self.run = testCaseJson["run"]
            self.title = testCaseJson["title"]
            self.grade = testCaseJson["grade"]
            self.compile = testCaseJson["compile"]
            self.points = testCaseJson["points"]
            self.details = testCaseJson["details"]
        except:
            print "ERROR: Test case missing required attribute"
            raise
