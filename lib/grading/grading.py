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
import pickle
import errno

from assignmentData import AssignmentData
from submissionData import SubmissionData
from gradingUtils import replaceJsonRoot


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

    # Delete uploads.json so it can be populated with new uploads
    try:
        # TODO backup this file
        os.remove(uploadsFilePath)
    except:
        print "ERROR: Couldn't remove uploads.json"
        raise

    newSubmissions = []

    # Create SubmissionData object for every submission in uploads
    for submissionJson in uploadsData["submissions"]:
        newSubmissions.append(SubmissionData(submissionJson))

    print "Found " + str(len(newSubmissions)) + " new submissions"

    return newSubmissions


# Create sandbox directory for assignment, return path
def createSandBoxDirectory(tmpPath):

    # Create temporary directory if it doesn't exist
    if not path.exists(tmpPath):
        try:
            print "Temporary directory does not exist, creating at ", tmpPath
            os.mkdir(tmpPath)
        except:
            print "ERROR: Couldn't create temporary directory!"
            raise

    # Generate path to sandbox based on time
    sandBoxPath = path.join(tmpPath,
                            md5(str(datetime.datetime.now())).hexdigest())

    # If path exists, regenerate until we have a novel path
    while path.exists(sandBoxPath):
        sleep(100)
        sandBoxPath = path.join(tmpPath,
                                md5(str(datetime.datetime.now())).hexdigest())

    # Create sandbox directory
    try:
        print "Creating sandbox directory at ", sandBoxPath
        os.mkdir(sandBoxPath)
    except:
        print "ERROR: Error creating sandbox directory within ", tmpPath
        raise

    return sandBoxPath


# Copy (or symlink) instructor directory
def linkInstructorDirectory(assignmentPath, sandBoxPath):

    # Path to instructor directory
    instructorDirectoryPath = path.join(assignmentPath, "instructor")

    # Path to symlink
    instructorDirectoryLink = path.join(sandBoxPath, "instructor")

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
def createResultsDirectory(sandBoxPath):

    # Path to results directory within sandbox
    resultsPath = path.join(sandBoxPath, "results")

    try:
        os.mkdir(resultsPath)
    except:
        print "ERROR: Cannot create results directory"
        raise


# Copy student files
def copyStudentFiles(submissionPath, sandBoxPath):

    # Path to copy student files to
    studentPath = path.join(sandBoxPath, "student")

    try:
        shutil.copytree(submissionPath, studentPath)
    except:
        print "ERROR: Couldn't copy student files"
        raise


# Execute any pre-grading steps (typically compile and run)
def runTestCase(sandBoxPath, testCase):

    print "Running Test Case:", testCase.title

    # Path to results directory
    resultsPath = path.join(sandBoxPath, "results")

    # Path to student directory
    studentPath = path.join(sandBoxPath, "student")

    # Run Compilation commands

    # Store stdout and stderr for compilation output
    compileOutput = None
    # True if compile executed successfully
    success = None

    # If compile command is blank, no compilation is necessary
    if testCase.compile == "" or testCase.compile is None:
        print "No compilation command"
        compileOutput = ""
        success = True
    else:
        try:
            print "Running compilation command:", testCase.compile

            # Attempt to get compilation output and run command with the
            # sandbox as the current working directory
            compileOutput = subprocess.check_output(testCase.compile,
                                                    stderr=subprocess.STDOUT,
                                                    cwd=sandBoxPath,
                                                    shell=True)
            success = True
        except subprocess.CalledProcessError as error:
            # There was an error during compilation
            compileOutput = error.output
            success = False
        except:
            print "ERROR: There was an unusual error during compiliation"
            raise

    # Create the compile out data object
    compileOutJson = {
        "success": success,
        "details": compileOutput
    }

    # Get path to compile_out.json
    compileOutPath = path.join(sandBoxPath, "compile_out.json")

    # Write to compile_out.json
    try:
        print "Writing compile output file"
        compileOutFile = open(compileOutPath, 'w')
        json.dump(compileOutJson, compileOutFile)
        compileOutFile.close()
    except:
        print "ERROR: Cannot write to compile_out.json"
        raise

    # Run "run" command as untrusted user

    success = None

    # If compile command is blank, no compilation is necessary
    if testCase.run == "" or testCase.run is None:
        print "No run command"
        success = True
    else:
        try:
            print "Running run command (within student):", testCase.run

            # TODO CRITICAL Switch to untrusted user!
            # This can be done via an untrusted user executable called
            # with the run command as it's arguments

            # Attempt to get compilation output and run command with the
            # sandbox as the current working directory
            subprocess.check_output(testCase.run,
                                    cwd=studentPath,
                                    shell=True)
            success = True
        except subprocess.CalledProcessError as error:
            # There was an error during compilation
            success = False
        except:
            print "ERROR: There was an unusual error during compiliation"
            raise


# Grade results of assignment
# Return a test case grade object
def gradeTestCase(sandBoxPath, testCase):

    print "Grading Test Case:", testCase.title

    # Run grade command

    # Store stdout for outputting grade output
    gradeOutput = None

    # If compile command is blank, no compilation is necessary
    if testCase.grade == "" or testCase.grade is None:
        print "ERROR: No grade command"
        raise Exception("Grade command is required")
    else:
        try:
            print "Running grade command:", testCase.grade

            # Attempt to get compilation output and run command with the
            # sandbox as the current working directory
            gradeOutput = subprocess.check_output(testCase.grade,
                                                  cwd=sandBoxPath,
                                                  shell=True)
        except:
            print "ERROR: There was an error grading this test case"
            raise

    # The server needs to display certain output files to the student when they
    # view the server, but it doesn't know which of the student's files are
    # important without parsing the grades object and looking for paths to
    # student/

    # Attempt to parse grade output
    try:
        gradeOutputJson = json.loads(gradeOutput)
    except:
        print "ERROR: Grade function outputted bad JSON"
        print pickle.dumps(gradeOutput)
        raise

    print "Copying relevant files from student/ to results/"
    # Look for any paths to student/ and replace them with paths to results/
    changedPaths = replaceJsonRoot(gradeOutputJson, "student", "results")

    # Copy each changed path (from student) to results
    for oldPath in changedPaths:

        # make sure old path refers to the sandbox directory
        oldPathFull = path.join(sandBoxPath, oldPath)

        # Get the path we're moving it to (in results)
        newPathFull = path.join(sandBoxPath, "results" +
                                             oldPath[len("student"):])

        # Create any directories that don't exist in results
        # e.g. student/testcase1/out.txt requires creation of results/testcase1
        try:
            os.makedirs(path.basename(newPathFull))
        except OSError:
            # Directory already exists
            pass
        except:
            print "ERROR: Problem creating a directory within results"
            raise

        # Copy file from results to students
        try:
            print "Copying " + oldPath + " to results"
            # TODO this can probably be a move
            shutil.move(oldPathFull, newPathFull)
        except:
            print "ERROR: Couldn't copy file from students to results"

    # Adjust score

    return gradeOutputJson


# Reset the student directory (so it is how it was submitted)
# TODO this shouldn't be done if testCase says not to
# TODO more efficient reset then deleting and copying
def cleanStudentDirectory(submissionPath, sandBoxPath):

    # Path to student directory to reset
    studentPath = path.join(sandBoxPath, "student")

    print "Reseting student directory"
    try:
        print studentPath
        shutil.rmtree(studentPath)
    except:
        print "ERROR: Problem reseting student directory"
        raise

    copyStudentFiles(submissionPath, sandBoxPath)


# Get final grade data from all the test case grades
# This returns the json for the submission.json file
# testCaseResults = list of tuples [(testCase, gradeOutput)]
def getFinalGrade(assignmentConfig, testCaseResults, submissionData):

    # All the fields necessary for the submission.json file
    submissionJson = {}

    submissionJson["testcases"] = []
    submissionJson["submission_number"] = submissionData.submissionNumber
    submissionJson["submission_time"] = submissionData.submitTime

    # Points awarded, incremented when looping through test cases
    awardedPointsSum = 0

    # Loop through test cases, calculate grade and write fields to submission
    # json
    for testCase, result in testCaseResults:

        # The percentage this student got on a test case
        percentageCorrect = result["score"]
        if "total" in result:
            percentageCorrect /= float(result["total"])

        # Calculate points awarded for test case based on test case total
        pointsAwarded = int(testCase.points * percentageCorrect)

        # Add test case points to the sums
        awardedPointsSum += pointsAwarded

        # Add all the information for this test case to the submission data
        submissionJson["testcases"].append({
            "test_name": testCase.title,
            "points_awarded": pointsAwarded,
            "message": result.get("message", ""),
            "diff": result.get("diff", "")
        })

    submissionJson["points_awarded"] = awardedPointsSum

    return submissionJson


# Create submission output directory
def createOutputDirectory(submissionOutputPath):
    print "Creating submission output directory"
    try:
        os.makedirs(submissionOutputPath)
    except OSError as e:
        if e.errno == errno.EEXIST:
            pass  # The user directory may already exist
        else:
            print "ERROR: Problem creating directory!"
            raise


# Write final grade data to submission output directory
def outputFinalGrade(submissionOutputPath, finalGrade):
    print "Writing automated testing grade (submission.json)"

    # The submission.json file is at the root of the submission directory
    submissionJsonPath = path.join(submissionOutputPath, "submission.json")

    try:
        submissionFile = open(submissionJsonPath, 'w')
        json.dump(finalGrade, submissionFile)
        submissionFile.close()
    except:
        print "ERROR: Cannot write to submission.json file"
        raise


# Copy sandbox directory's results directory to output directory
def outputResultsDirectory(sandBoxPath, submissionOutputPath):
    print "Moving results folder from sandbox to submission directory"

    # Path to results within sandbox
    sandBoxResultsPath = path.join(sandBoxPath, "results")

    # Path to move results to within submission directory
    submissionResultsPath = path.join(submissionOutputPath, "results")

    try:
        shutil.move(sandBoxResultsPath, submissionResultsPath)
    except:
        print "ERROR: Cannot move results directory to submission directory"
        raise


# Remove temporary (sandbox) directory
def removeSandBoxDirectory(sandBoxPath):

    print "Removing sandbox directory"

    try:
        shutil.rmtree(sandBoxPath)
    except:
        print "ERROR: Couldn't delete sandbox directory!"
        # no need to raise, the temporary directory is probably auto-cleared
