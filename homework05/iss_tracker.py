from flask import Flask, request
import requests
import xmltodict
import math

app = Flask(__name__)

APIReq = requests.get(url='https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml')

global ISSD 
ISSData = xmltodict.parse(APIReq.text)

ISSD = ISSData['ndm']['oem']['body']['segment']['data']['stateVector']

@app.route('/', methods=['GET'])
def DataSet() -> dict:
    """    
    This function returns the most up-to-date data set.

    Returns:
        ISSD (dict): The entire data set in the form of a dictionary.
    """
    return ISSD

@app.route('/epochs', methods=['GET'])
def DS_Epochs() -> list:
    """    
    This function scans the entire data set and places each value with 
    the key 'EPOCH' into a list.
    If a limit and or offset is provided in the call then the outputted 
    list will return the amount of epochs starting from the offset stated
    and only the amount given from the limit input.  
    
    Returns:
        EpochList (list): A list of strings from the data set.
    """
    limit = request.args.get("limit",len(ISSD))
    try:
        limit = int(limit)
    except ValueError:
        return("Invalid limit parameter \n", 400)

    offset = request.args.get("offset",0)
    try:
        offset = int(offset)
    except ValueError:
        return("Invalid offset parameter \n", 400)
    
    EpochList = []
    for i in range(offset,len(ISSD),1):
        if(len(EpochList) < limit):
            EpochList.append(ISSD[i]['EPOCH'])
        else:
            break
    return EpochList

@app.route('/epochs/<string:epoch>', methods=['GET'])
def DS_SpecificEpoch(epoch: str) -> dict:
    """
    This function scans the data set for the corresponding
    statevector with the epoch inputted.

    Args:
        epoch (str): This should be the string epoch value inputted 
        into the curl statement for the specific statevector wanted.

    Returns:
        ISSD[i] (dict): The dictionary for the statevector with the
        corresponding epoch.
   """
    for i in range(len(ISSD)):
        if (ISSD[i]['EPOCH'] == str(epoch)):
            return ISSD[i]

@app.route('/epochs/<string:epoch>/speed', methods=['GET'])
def DS_EpochSpeed(epoch: str) -> str:
    """
    This function calculates the speed of the specific epoch
    inputted with the corresponding X,Y and Z_dots.

    Args:
        epoch (str): This should be the string epoch value inputted
        into the curl statement for the specific statevector wanted.

    Returns:
        speed (str): The str value of the calculated speed.
    """
    for i in range(len(ISSD)):
        if (ISSD[i]['EPOCH'] == str(epoch)):
            xDot = abs(float(ISSD[i]['X_DOT']['#text']))
            yDot = abs(float(ISSD[i]['Y_DOT']['#text']))
            zDot = abs(float(ISSD[i]['Z_DOT']['#text']))

            maf = (xDot**2 + yDot**2 + zDot**2)
            speed = round(math.sqrt(maf),4)
            return str(speed) + "\n" 
            
@app.route('/help', methods=['GET'])
def DS_Help() -> str:
    """
    This function returns the doc strings of each function.

    Returns:
        Dicthelp (str): The string of each function doc-string 
        with its corresponding route call.
    """
    Dicthelp = "/ : " + str(DataSet.__doc__) + "\n" + "/epochs : " + str(DS_Epochs.__doc__) + "\n" + "/epochs?limit=int&offset=int : " + str(DataSet.__doc__) + "\n" + "/epochs/<epoch> : " + str(DS_SpecificEpoch.__doc__) + "\n" + "/epochs/<epoch>/speed : " + str(DS_EpochSpeed.__doc__) + "\n" + "/help : " + str(DS_Help.__doc__) + "\n" + "/delete-data : " + str(DS_Delete.__doc__) + "\n" + "/post-data : " + str(DS_Post.__doc__)

    return Dicthelp

@app.route('/delete-data', methods=['DELETE'])
def DS_Delete() -> list:
    """
    This function clears the data.

    Returns:
        ISSD (list): an empty list to represent that the data 
        has been cleared from its variable.
    """
    global ISSD
    ISSD.clear()
    return ISSD

@app.route('/post-data', methods=['POST'])
def DS_Post() -> dict:
    """
    This function 

    Returns:
        ISSData (dict): The dictionary for the entire data set.
    """
    global ISSD
    APIReq = requests.get(url='https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml')
    ISSData = xmltodict.parse(APIReq.text)
    ISSD = ISSData['ndm']['oem']['body']['segment']['data']['stateVector'] 
    
    return ISSData

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
