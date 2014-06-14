#!/usr/bin/python

# This file has all the methods used for sandboxing, running and grading an
# assignment. See gradeAssignment.py.

from os import path
import json
from assignmentData import AssignmentData


# Returns AssignmentData assignment built from assignment at specified path
def getAssignmentConfig(assignmentPath):

    print "Getting assignment config at ", assignmentPath

    # Get path to assignment config from assignmentPath
    assignmentConfigPath = path.join(assignmentPath, "assignment.json")

    try:
        # Open file and parse json
        assignmentFile = open(assignmentConfigPath)
        assignmentJson = json.load(assignmentFile)
        assignmentFile.close()
    except:
        print "ERROR: Problem reading assignment configuration"
        raise

    # Assignment json was successfully parsed

    # Create assignment data object from assignment json data
    return AssignmentData(assignmentJson)


# Make sure the assignment has been created by instructor
def checkAssignmentExists(baseConfig, assignmentID):
    raise NotImplementedError("checkAssignmentExists")


# Get all student submission paths for this assignment
# Returns list of SubmissionData objects
def getNewSubmissions(submissionsPath, assignmentID):
    raise NotImplementedError("allNewSubmissions")


# Create temporary directory for assignment
def createTemporaryDirectory(tmpPath):
    raise NotImplementedError("createTemporaryDirectory")


# Copy (or symlink) instructor directory
def linkInstructorDirectory(assignmentPath, tmpPath):
    raise NotImplementedError("linkInstructorDirectory")


# Create results directory
def createResultsDirectory(tmpPath):
    raise NotImplementedError("createResultsDirectory")


# Copy student files
def copyStudentFiles(submissionPath, tmpPath):
    raise NotImplementedError("copyStudentFiles")


# Execute any pre-grading steps (typically compile and run)
def runTestCase(tmpPath, testCase):
    raise NotImplementedError("runTestCase")


# Grade results of assignment
def gradeTestCase(tmpPath, testCase):
    raise NotImplementedError("gradeTestCase")


# Get final grade data from all the test case grades
def getFinalGrade(assignmentConfig, testCaseResults):
    raise NotImplementedError("getFinalGrade")


# Create submission output directory
def createOutputDirectory(submissionOutputPath):
    raise NotImplementedError("createOutputDirectory")


# Write final grade data to submission output directory
def outputFinalGrade(submissionOutputPath, finalGrade):
    raise NotImplementedError("outputFinalGrade")


# Copy temporary directory's results directory to output directory
def outputResultsDirectory(tmpPath, submissionOutputPath):
    raise NotImplementedError("outputResultsDirectory")
