
# Class for storing data about a single submission upload

from os import path


class SubmissionData:

    # Time the submission was submitted
    submitTime = None

    # Name of submitting student (this is a student id)
    student = None

    # Submission number
    submissionNumber = None

    def __init__(self, submissionJson):

        try:
            self.submitTime = submissionJson["submitTime"]
            self.student = submissionJson["student"]
            self.submissionNumber = submissionJson["submissionNumber"]
        except:
            print "ERROR: Missing attribute in uploads.json within a submission"
            raise

    # Returns path to the files the student submitted
    def getPath(self,submissionsPath,assignmentID):
        return path.join(submissionsPath,assignmentID, self.student,
            str(self.submissionNumber))
