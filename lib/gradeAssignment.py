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

    # Get assignment configuration
    assignmentConfig = getAssignmentConfig(assignmentPath)

    # Make sure the assignment has been created by instructor
    checkAssignmentExists(baseConfig, assignmentID)

    # Get all student submission paths for this assignment
    allNewSubmissions = getNewSubmissions(submissionsPath, assignmentID)

    # Go through every submission to be graded
    for submissionData in allNewSubmissions:

        # Path where student's submission was uploaded and extracted to
        submissionPath = submissionData.path

        # Path where the results of the grading are output to
        submissionOutputPath = path.join(
            resultsPath, assignmentID, submissionData.studentID,
            submissionData.submissionNumber)

        # Create temporary directory for assignment
        tmpPath = createTemporaryDirectory(tmpPath)

        # Copy (or symlink) instructor directory
        linkInstructorDirectory(assignmentPath, tmpPath)

        # Create results directory
        createResultsDirectory(tmpPath)

        # Stores results of each test case
        testCaseResults = []

        # Loop through test cases and execute
        for testCase in assignmentPath:

            # Copy student files
            copyStudentFiles(submissionPath, tmpPath)

            # Execute any pre-grading steps (typically compile and run)
            runTestCase(tmpPath, testCase)

            # Grade results of assignment
            testCaseGrade = gradeTestCase(tmpPath, testCase)

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





# Program was called from command line
if __name__ == "__main__":

    # Get command line arguments
    args = parseGradeAssignmentArguments()

    # Call grading function
    gradeAssignment(args.basePath, args.assignmentID)
