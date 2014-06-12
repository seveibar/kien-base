
# Used to log the grading and running of an assignment, outputting messages
# a global log file

logFilePath = None

def log(*args):

    # Convert arguments to more manageable string
    logString = "  ".join(map(str,args))

    # If the log file path was specified, output to log file
    if (logFilePath):
        try:
            fi = open(logFilePath,'a')
            fi.write(logString + "\n")
            fi.close()
        except:
            print "ERROR: COULD NOT OPEN LOGFILE"
    else:
        print logString
        # pass
