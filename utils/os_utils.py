import os 

def getEnvVariable(varName,required):
    envVar = os.getenv(varName)
    if isNotBlank(envVar):
        return envVar
    else:
        if required:
            raise EnvironmentError(varName + ' is required')
                

def isNotBlank(string):
    if string and string.strip():
        return True
    else:
        return False

