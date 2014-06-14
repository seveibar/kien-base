#!/usr/bin/python

# This file has all the methods used for sandboxing, running and grading an
# assignment. See gradeAssignment.py.

from os import path
import json
from assignmentData import AssignmentData
from submissionData import SubmissionData


# Make sure the assignment has been created by instructor
def checkAssignmentExists(assignmentPath):
    if not path.exists(assignmentPath):
        print "ERROR: Assignment does not exist"
        raise Exception("Assignment does not exist")


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


# Get all student submission paths for this assignment
# Returns list of SubmissionData objects
def getNewSubmissions(submissionsPath, assignmentID):
    print "Looking for new submissions in ", submissionsPath

    # Path to the uploads.json file which stores all the latest submissions
    # information
    uploadsFilePath = path.join(submissionsPath, assignmentID, "uploads.json")

    if not path.exists(uploadsFilePath):
        print "No uploads.json file, no new uploads"
        return []

    # Attempt to parse latest uploads file if it exists
    try:
        uploadsFile = open(uploadsFilePath)
        uploadsData = json.load(uploadsFile)
        uploadsFile.close()
    except:
        print "ERROR: Cannot read or parse uploads.json"
        raise

    # Successfully loaded and parsed uploads.json

    newSubmissions = []

    # Create SubmissionData object for every submission in uploads
    for submissionJson in uploadsData["submissions"]:
        newSubmissions.append(SubmissionData(submissionJson))

    return newSubmissions

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
