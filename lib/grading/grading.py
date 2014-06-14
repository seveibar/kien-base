#!/usr/bin/python

# This file has all the methods used for sandboxing, running and grading an
# assignment. See gradeAssignment.py.

from os import path
import os
import json
from hashlib import md5
from time import sleep
import datetime
import subprocess
import shutil

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

    # Path to the uploads.json file which stores all the latest submissions
    # information
    uploadsFilePath = path.join(submissionsPath, assignmentID, "uploads.json")
    print "Looking for new submissions in ", uploadsFilePath

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

    print "Found " + str(len(newSubmissions)) + " new submissions"

    return newSubmissions


# Create sandbox directory for assignment, return path
def createTemporaryDirectory(tmpPath):

    # Create temporary directory if it doesn't exist
    if not path.exists(tmpPath):
        try:
            print "Temporary directory does not exist, creating at ", tmpPath
            os.mkdir(tmpPath)
        except:
            print "ERROR: Couldn't create temporary directory!"
            raise

    # Generate path to sandbox based on time
    sandboxPath = path.join(tmpPath,
                            md5(str(datetime.datetime.now())).hexdigest())

    # If path exists, regenerate until we have a novel path
    while path.exists(sandboxPath):
        sleep(100)
        sandboxPath = path.join(tmpPath,
                                md5(str(datetime.datetime.now())).hexdigest())

    # Create sandbox directory
    try:
        print "Creating sandbox directory at ", sandboxPath
        os.mkdir(sandboxPath)
    except:
        print "ERROR: Error creating sandbox directory within ", tmpPath
        raise

    return sandboxPath


# Copy (or symlink) instructor directory
def linkInstructorDirectory(assignmentPath, sandboxPath):

    # Path to instructor directory
    instructorDirectoryPath = path.join(assignmentPath, "instructor")

    # Path to symlink
    instructorDirectoryLink = path.join(sandboxPath, "instructor")

    # Command to create symbolic link
    cmd = "ln -s " + instructorDirectoryPath + " " + instructorDirectoryLink

    print "Creating symlink to instructor directory"
    print cmd

    try:
        subprocess.check_output(cmd, shell=True)
    except:
        print "ERROR: Cannot create symlink"
        raise


# Create results directory
def createResultsDirectory(sandboxPath):

    # Path to results directory within sandbox
    resultsPath = path.join(sandboxPath, "results")

    try:
        os.mkdir(resultsPath)
    except:
        print "ERROR: Cannot create results directory"
        raise


# Copy student files
def copyStudentFiles(submissionPath, sandboxPath):

    # Path to copy student files to
    studentPath = path.join(sandboxPath, "students")

    try:
        shutil.copytree(submissionPath, studentPath)
    except:
        print "ERROR: Couldn't copy student files"
        raise


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


# Copy sandbox directory's results directory to output directory
def outputResultsDirectory(sandboxPath, submissionOutputPath):
    raise NotImplementedError("outputResultsDirectory")
