
# Not a instructor function, this function is for making sure the scripts
# are running within the temporary directory containing "instructor","student"
# and "results"

from os import path

def checkPath():
    if  not (path.exists("student") or path.exists("instructor") or path.exists("results")):
        throw Exception("Not in temporary directory! Make sure you execute the command from the directory containing instructor, student and results directories")
