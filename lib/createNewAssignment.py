#!/bin/python

import commandLineParser
from os import path
import json
import baseLoader
import datetime
from sys import exit
import shutil

# Creates new assignment with id {assignmentID} using the resources at the
# specified base directory (namely the assignment template)
def createNewAssignment(basePath, assignmentID):
    print "Creating new assignment \""+assignmentID+"\" using base at ", basePath

    # Get the baseConfig file
    baseConfig = baseLoader.getBaseConfig(basePath)

    # Path to new assignment directory
    newAssignmentPath = path.join(baseConfig["dataPath"], "assignments", assignmentID)
    # Path to assignment template directory
    assignmentTemplateDirectory = path.join(basePath, "assignment_template")

    # Make sure assignment doesn't already exist
    if path.exists(newAssignmentPath):
        print "ERROR: Assignment already exists!"
        exit(1)

    # Create default assignment from assignment_template directory
    shutil.copytree(assignmentTemplateDirectory, newAssignmentPath)

    # Path to new assignment configuration file
    newAssignmentConfigPath = path.join(newAssignmentPath, "assignment.json")

    # Open assignment config file and modify defaults
    try:
        # Open and read from assignment config
        assignmentConfigFile = open(newAssignmentConfigPath,'r')
        assignmentConfig = json.load(assignmentConfigFile)
        assignmentConfigFile.close()

        # Modify assignment config
        # Modifications to make...
        # Change id to assignmentID
        # Change name to assignmentID (intended to be changed)
        # Change due date to one week from now

        assignmentConfig["id"] = assignmentID
        assignmentConfig["name"] = assignmentID

        # Get day and time one week from now
        weekFromNowString = str(datetime.datetime.now() + datetime.timedelta(days=7))

        assignmentConfig["due_date"] = weekFromNowString

        # Write new assignment config file
        assignmentConfigFile = open(newAssignmentConfigPath,'w')
        json.dump(assignmentConfig, assignmentConfigFile, indent=4)
        assignmentConfigFile.close()

    except:
        print "ERROR: Something bad happened when modifying assignment.json"
        raise

# Called when this script is called from the command line
if __name__ == "__main__":

    # Get command line arguments (error if any are wrong)
    args = commandLineParser.parseCreateNewAssignmentArguments()

    createNewAssignment(args.basePath, args.assignmentID)
