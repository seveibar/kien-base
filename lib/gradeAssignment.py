#!/usr/bin/python

from os import path

from grading.grading import *
from baseLoader import getBaseConfig
from commandLineParser import parseGradeAssignmentArguments

# Grade assignment using information at base
def gradeAssignment(basePath, assignmentID):

    # Load and parse base config file
    baseConfig = getBaseConfig(basePath)

    # Get necessary paths
    tmpPath = baseConfig["tmpPath"]
    dataPath = baseConfig["dataPath"]
    resultsPath = path.join(dataPath, "results")
    submissionsPath = path.join(dataPath, "submissions")
    assignmentsPath = path.join(dataPath, "assignments")
    assignmentPath = path.join(assignmentsPath, assignmentID)

    # Make sure the assignment has been created by instructor
    checkAssignmentExists(assignmentPath)

    # Get assignment configuration
    assignmentConfig = getAssignmentConfig(assignmentPath)

    # Get all student submission paths for this assignment
    allNewSubmissions = getNewSubmissions(submissionsPath, assignmentID)

    # Go through every submission to be graded
    for submissionData in allNewSubmissions:

        # Path where student's submission was uploaded and extracted to
        submissionPath = submissionData.getPath(submissionsPath, assignmentID)

        # Path where the results of the grading are output to
        submissionOutputPath = path.join(
            resultsPath, assignmentID, submissionData.student,
            str(submissionData.submissionNumber))

        # Create sandbox directory for assignment within temporary directory
        sandboxPath = createTemporaryDirectory(tmpPath)

        # Copy (or symlink) instructor directory
        linkInstructorDirectory(assignmentPath, sandboxPath)

        # Create results directory
        createResultsDirectory(sandboxPath)

        # Stores results of each test case
        testCaseResults = []

        # Loop through test cases and execute
        for testCase in assignmentPath:

            # Copy student files
            copyStudentFiles(submissionPath, sandboxPath)

            # Execute any pre-grading steps (typically compile and run)
            runTestCase(sandboxPath, testCase)

            # Grade results of assignment
            testCaseGrade = gradeTestCase(sandboxPath, testCase)

            # Add test case grade to the list of test cases
            testCaseResults.append((testCase.name, testCaseGrade))

        # Get final grade data from all the test case grades
        finalGrade = getFinalGrade(assignmentConfig, testCaseResults)

        # Create submission output directory
        createOutputDirectory(submissionOutputPath)

        # Write final grade data to submission output directory
        outputFinalGrade(submissionOutputPath, finalGrade)

        # Copy temporary directory's results directory to output directory
        outputResultsDirectory(tmpPath, submissionOutputPath)

    print "All assignments graded!"




# Program was called from command line
if __name__ == "__main__":

    # Get command line arguments
    args = parseGradeAssignmentArguments()

    # Call grading function
    gradeAssignment(args.basePath, args.assignmentID)
