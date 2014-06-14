
# This function checks for the existence of a README.txt file in ../student
usage = "checkReadme [path/to/student/dir]"

import json
from checkPath import checkPath
from os import path
import sys
from log import log


# Returns json object representing grade, the score will be 0 for no readme
# and 1 for readme exists
def checkReadme(pathToStudent="student"):

    log("Checking for Readme.txt at " + path.abspath(pathToStudent))

    # Try different paths to readme
    if path.exists(path.join(pathToStudent, "README.txt")):
        return {"score": 1}
    elif path.exists(path.join(pathToStudent, "Readme.txt")):
        return {"score": 1}
    elif path.exists(path.join(pathToStudent, "readme.txt")):
        return {"score": 1}
    else:
        # Couldn't find a readme
        return {"score": 0}


# The following code is executed if this is called from the command line
if __name__ == "__main__":
    if len(sys.argv) == 2:
        if (sys.argv[1] == "--help" or sys.argv[1] == "-h"):
            print "USAGE:", usage
        else:
            # Path to Readme directory provided
            print json.dumps(checkReadme(sys.argv[0]),indent=4)
    else:
        # No Readme directory path provided
        # Make sure we're in tmp directory
        checkPath()
        print json.dumps(checkReadme("student"),indent=4)
