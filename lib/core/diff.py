
# This function computes the difference between two given files

import json
import sys


# Get the difference between the two input files, output a difference
# file at the specified path and return a json object representing the
# score (% matching)
def diff(filePath1, filePath2, outputDifferencePath):

    # Open the first file
    try:
        lines1 = open(filePath1).readlines()
    except:
        print "ERROR: Couldn't read file", filePath1
        raise

    # Open the second file
    try:
        lines2 = open(filePath2).readlines()
    except:
        print "ERROR: Couldn't read file", filePath2
        raise

    # Store line numbers of lines with any difference
    differences = []

    # The lowest of the number of lines in both files
    lowestLineCount = min(len(lines1), len(lines2))

    # Loop through every line in both files and note all differences
    for i in xrange(lowestLineCount):
        if (lines1[i] != lines2[i]):
            differences.append(i)

    # Create json differences file
    differencesContent = []

    # Go through every line and add difference objects
    for lineNumber in differences:
        differencesContent.append({
            "student": {"start": lineNumber},
            "instructor": {"start": lineNumber},
        })

    # Write differencesContent to output difference file
    try:
        outputDifferenceFile = open(outputDifferencePath, 'w')
        json.dump({"differences": differencesContent}, outputDifferenceFile, indent=4)
        outputDifferenceFile.close()
    except:
        print "ERROR: Error writing to difference file to", outputDifferencePath
        raise

    # Score is a percentage of differences / total lines
    score = lowestLineCount - len(differences)

    # Return the score object
    return {
        "score": score,
        "total": lowestLineCount,
        "diff": {
            "student": filePath1,
            "instructor": filePath2,
            "difference": outputDifferencePath
        }
    }



    return {"score":1}

# The following code is executed if this is called from the command line
if __name__ == "__main__":
    if len(sys.argv) == 4:
        # Print the test case grade json to stdout
        print json.dumps(diff(sys.argv[1], sys.argv[2], sys.argv[3]), indent=4)
    else:
        print "USAGE: diff path/to/instructor_file /path/to/student_file /output/difference.json"
