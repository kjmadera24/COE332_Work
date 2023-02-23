from flask import Flask
import requests
import xmltodict
import math

app = Flask(__name__)

APIReq = requests.get(url='https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml')
ISSData = xmltodict.parse(APIReq.text)
ISSD = ISSData['ndm']['oem']['body']['segment']['data']['stateVector']

@app.route('/', methods=['GET'])
def DataSet():
    """    
    This function returns the most up-to-date data set.

    Returns:
        ISSD (dict): The entire data set in the form of a dictionary.
    """
    return ISSD

@app.route('/epochs', methods=['GET'])
def DS_Epochs():
    """    
    This function scans the entire data set and places each value with 
    the key 'EPOCH' into a list.

    Returns:
        EpochList (list): A list of strings from the data set.
    """
    EpochList = []
    for i in range(len(ISSD)):
        EpochList.append(ISSD[i]['EPOCH'])
    return EpochList


@app.route('/epochs/<string:epoch>', methods=['GET'])
def DS_SpecificEpoch(epoch):
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
def DS_EpochSpeed(epoch):
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
            return str(speed)
            
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
