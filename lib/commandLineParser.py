#!/usr/bin/python

import argparse
from os import path

# Returns default base path based on this file's location (inside base/lib)
def getDefaultBasePath():
    return path.normpath(path.join(path.dirname(__file__),".."))

# Parses command line arguments for create_new_assignment within base/bin
# Returns Namespace object with user inputted arguments
# Arguments:
# --base: path/to/base
# assignmentID: id of assignment to create (directory with id is created
#               inside data/assignments
def parseCreateNewAssignmentArguments(defaultBasePath=None):

    defaultBasePath = getDefaultBasePath()

    parser = argparse.ArgumentParser(description='Creates and sets up new assignment')

    # --config argument
    parser.add_argument(
        "--base","-b",
        action="store",
        type=str,
        dest="basePath",
        help="Path to base directory which should contain \"base.json\"",
        default=defaultBasePath)

    # Assignment id (name of directory inside data/assigments)
    parser.add_argument("assignmentID")

    # Parse command line arguments
    return parser.parse_args()

# Parses command line arguments for grade_assignment within base/bin
# Returns Namespace object with user inputted arguments
# Arguments:
# --base: path/to/base
# assignmentID: id of assignment to grade
def parseGradeAssignmentArguments(defaultBasePath=None):

    defaultBasePath = getDefaultBasePath()

    parser = argparse.ArgumentParser(description='Grades all submissions for assignment inside of assignment directory')

    # --config argument
    parser.add_argument(
        "--base","-b",
        action="store",
        type=str,
        dest="basePath",
        help="Path to base directory which should contain \"base.json\"",
        default=defaultBasePath)

    # Assignment id (name of directory inside data/assigments)
    parser.add_argument("assignmentID")

    # Parse command line arguments
    return parser.parse_args()
