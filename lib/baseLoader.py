#!/bin/python

import json
from os import path

# Load base config using base path and return json base config
def getBaseConfig(basePath):
    print "Attempting to read base config at ",basePath

    # Get path to base.json file from base path
    baseConfigPath = path.join(basePath, "base.json")

    try:
        # Open base config file
        baseConfigFile = open(baseConfigPath)

        # Attempt to parse base config file
        baseConfig = json.load(baseConfigFile)

        # Close up base config file
        baseConfigFile.close()
    except:
        # Couldn't read base config file
        if not path.exists(baseConfigPath):
            print "ERROR: No base.json in directory"
            raise
        else:
            print "ERROR: Couldn't parse/read base.json, bad json?"
            raise

    return baseConfig
