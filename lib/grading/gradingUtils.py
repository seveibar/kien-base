

# Replace all instances of "oldRoot/..." with "newRoot/..." within all strings
# inside json object. Return all changed paths
def replaceJsonRoot(jsonObject, oldRoot, newRoot):

    # Track all the roots that have been changed (before change)
    changedRoots = []

    # Go through each key and value inside the jsonObject
    for k, v in jsonObject.iteritems():

        # If the field is a string, check if it has the oldRoot
        if isinstance(v, basestring) and v[:len(oldRoot)] == oldRoot:

            # Store the old root and replace
            changedRoots.append(v)
            jsonObject[k] = newRoot + v[len(oldRoot):]

        # If the field is another dict or json object, iterate through it too
        elif isinstance(v, dict):
            changedRoots += replaceJsonRoot(v, oldRoot, newRoot)

    return changedRoots
