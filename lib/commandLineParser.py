#!/usr/bin/python

import argparse

# Parses command line arguments for Setup and returns a Namespace with the
# variables the user passed
def parseCreateNewAssignmentArguments(defaultBasePath="../"):

    parser = argparse.ArgumentParser(description='Creates and sets up new assignment')

    # --config argument
    parser.add_argument(
        "--base","-b",
        action="store",
        type=str,
        dest="basePath",
        help="Path to base directory which should contain \"base.json\"",
        default=defaultBasePath)

    parser.add_argument("assignmentID")

    # Parse command line arguments
    return parser.parse_args()
