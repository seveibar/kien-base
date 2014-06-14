
# AssignmentData class for holding assignment configuration

from testCase import TestCase


class AssignmentData:

    # ID for assignment (name of directory in data/assignments)
    id = None

    # Name for assignment
    name = None

    # Max number of submissions
    maxSubmissions = None

    # Due date
    dueDate = None

    # List with TestCase objects for each test case of assignment
    testCases = None

    # Initializes assignment data using an assignment.json dictionary
    def __init__(self, assignmentJson):

        try:

            self.id = assignmentJson["id"]
            self.name = assignmentJson["name"]
            self.maxSubmissions = assignmentJson["max_submissions"]
            self.dueDate = assignmentJson["due_date"]
            self.testCases = map(TestCase, assignmentJson["testcases"])

        except:
            print "ERROR: Missing attribute or bad structure in assignment.json"
            raise
