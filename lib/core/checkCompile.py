
# This function checks to see if the last compiliation was a success by checking
# the success boolean within the ../results/compile_out.json file
usage = "checkCompile [path/to/compile_out.json]"

import json
from checkPath import checkPath
from os import path
import sys
from log import log

# Returns json object representing grade, the score will be 0 for unsuccessful
# compile and 1 for successful compile
def checkCompile(pathToCompileOut="compile_out.json"):

    log("Checking for compile success in " + path.abspath(pathToCompileOut))

    # Make sure compile_out.json exists and is a file
    if path.isfile(pathToCompileOut):
        try:
            # Attempt to load compile_out.json or compiler output file
            compilerOutput = json.load(open(pathToCompileOut))

            if compilerOutput["success"]:
                return {"score":1}
            else:
                if "details" in compilerOutput:
                    return {"score":0,"details": compilerOutput["details"]}
                else:
                    return {"score":0}
        except:
            # Compiler output file probably has bad json
            log("ERROR: Error reading compiler output file")
            return {"score":0}
    else:
        log("ERROR: Compiler output was never generated!")
        return {"score":0}


# The following code is executed if this is called from the command line
if __name__ == "__main__":
    if len(sys.argv) == 2:
        if (sys.argv[1] == "--help" or sys.argv[1] == "-h"):
            print "USAGE:",usage
        else:
            # Path to Readme directory provided
            print json.dumps(checkCompile(sys.argv[0]),indent=4)
    else:
        # No Readme directory path provided
        # Make sure we're in tmp directory
        checkPath()
        print json.dumps(checkCompile("compile_out.json"),indent=4)
