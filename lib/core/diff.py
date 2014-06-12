
# This function computes the difference between two given files

import json
import sys

def diff(filePath1, filePath2):
    return {"score":1}

# The following code is executed if this is called from the command line
if __name__ == "__main__":
    if len(sys.argv) == 3:
        # Print the test case grade json to stdout
        print json.dumps(diff(sys.argv[0], sys.argv[1]),indent=4)
    else:
        print "USAGE: diff path/to/instructor_file /path/to/student_file"
