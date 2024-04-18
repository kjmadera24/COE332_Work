from flask import Flask, request
from geopy.geocoders import Nominatim
import requests
import xmltodict
import math
import time

app = Flask(__name__)
geocoder = Nominatim(user_agent='iss_tracker')

APIReq = requests.get(url='https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml')

global ISSD 
ISSData = xmltodict.parse(APIReq.text)

ISSD = ISSData['ndm']['oem']['body']['segment']['data']['stateVector']

@app.route('/', methods=['GET'])
def DataSet() -> dict:
    """    
    This route returns the most up-to-date data set.

    Returns:
        ISSD (dict): The entire data set in the form of a dictionary.
    """
    return ISSD

@app.route('/comment', methods=['GET'])
def DS_Com() -> list:
    """
    This route returns the comments in the data set.

    Returns:
        comList (list): The comments from the data set in a list.    
    """
    ISSDcom = ISSData['ndm']['oem']['body']['segment']['data']['COMMENT']
    comList = []

    for i in range(len(ISSDcom)):
        comList.append(ISSDcom[i])
    return comList

@app.route('/header', methods=['GET'])
def DS_Header() -> dict:
    """
    This route returns the header of the data set.

    Returns:
        ISSDhead (dict): The header key from the data set dictionary.
    """
    ISSDhead = ISSData['ndm']['oem']['header']
    return ISSDhead

@app.route('/metadata', methods=['GET'])
def DS_Meta() -> dict:
    """
    This route returns the metadata from the data set.

    Returns:
        ISSDmeta (dict): The metadata key from the data set.
    """
    ISSDmeta = ISSData['ndm']['oem']['body']['segment']['metadata']
    return ISSDmeta

@app.route('/epochs', methods=['GET'])
def DS_Epochs() -> list:
    """    
    This route scans the entire data set and places each value with 
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
        return("Invalid input", 400)

    offset = request.args.get("offset",0)
    try:
        offset = int(offset)
    except ValueError:
        return("Invalid limit paraneter", 400)
    
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
    This route scans the data set for the corresponding
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
    This route calculates the speed of the specific epoch
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

@app.route('/epochs/<string:epoch>/location', methods=['GET'])
def DS_EpochLocation(epoch: str) -> dict:
    """
    This route calculates the latitude, longitude, altitude and geoposition of the specific epoch. 

    Args:
        epoch (str): This should be the string epoch value inputted
        into the curl statement for the specific statevector wanted.

    Returns:
        llag (dict): The calculated lat, long, alt, and geo values.
    """
    MER = 6137

    for i in range(len(ISSD)):
        if (ISSD[i]['EPOCH'] == str(epoch)):
            #Epoch Manipulation
            Epoch = ISSD[i]['EPOCH']
            EpochHrs = int(Epoch[9:11])
            EpochMins = int(Epoch[12:14])

            #Coord Manipulation
            X = float(ISSD[i]['X']['#text'])
            Y = float(ISSD[i]['Y']['#text'])
            Z = float(ISSD[i]['Z']['#text'])
            
            #Equations
            lat = math.degrees(math.atan2(Z, math.sqrt(X**2 + Y**2)))
            lon = math.degrees(math.atan2(Y, X)) - ((EpochHrs-12)+(EpochMins/60))*(360/24) + 36
            if(lon < -180):
                lon = lon + 360
            elif(lon > 180):
                lon = lon - 360

            alt = math.sqrt(X**2 + Y**2 + Z**2) - MER  
            geo = geocoder.reverse((lat, lon), zoom=-2, language='en')
            if(str(geo) == "None"):
                geo = "Somewhere over water"
            llag = {
                    "Latitude": float(lat),
                    "Longitude": float(lon),
                    "Altitude": float(alt),
                    "Geoposition": str(geo)
                   }
            return llag

@app.route('/now', methods=['GET'])
def DS_ClosestEpoch() -> dict:
    """
    This route calculates which Epoch is the most recent to when the curl is called and calculates the latitude, longitude, altitude, geoposition, and speed of that epoch.

    Returns:
        nowOut (dict): The calculated lat, long, alt, geo, and speed values.
    """
    MER = 6371
    currTime = time.time()
    LowestTD = abs(currTime) - abs(time.mktime(time.strptime((ISSD[0]['EPOCH'])[:-5], '%Y-%jT%H:%M:%S')))
    LowestEp = ISSD[0]['EPOCH']
    
    for i in range(len(ISSD)):
        currEp = ISSD[i]['EPOCH']
        EpochT = time.mktime(time.strptime(currEp[:-5], '%Y-%jT%H:%M:%S'))
        TimeDiff = abs(currTime) - abs(EpochT)
        if(abs(TimeDiff) < LowestTD):
            LowestTD = abs(TimeDiff)
            LowestEp = currEp
            LowestEp_SV = ISSD[i]
    
    #Epoch Manipulation
    EpochHrs = int(LowestEp[9:11])
    EpochMins = int(LowestEp[12:14])

    #Coord Manipulation
    X = float(ISSD[i]['X']['#text'])
    Y = float(ISSD[i]['Y']['#text'])
    Z = float(ISSD[i]['Z']['#text'])

    #Equations
    lat = math.degrees(math.atan2(Z, math.sqrt(X**2 + Y**2)))
    lon = math.degrees(math.atan2(Y, X)) - ((EpochHrs-12)+(EpochMins/60))*(360/24) + 36
    if(lon < -180):
        lon = lon + 360
    elif(lon > 180):
        lon = lon - 360

    alt = math.sqrt(X**2 + Y**2 + Z**2) - MER
    geo = geocoder.reverse((lat, lon), zoom=4, language='en')
    if(str(geo) == "None"):
        geo = "Somewhere over water"
    xDot = abs(float(LowestEp_SV['X_DOT']['#text']))
    yDot = abs(float(LowestEp_SV['Y_DOT']['#text']))
    zDot = abs(float(LowestEp_SV['Z_DOT']['#text']))

    maf = (xDot**2 + yDot**2 + zDot**2)
    speed = round(math.sqrt(maf),4)

    nowOut = {
        "Most recent Epoch": LowestEp,
        "Seconds from now": LowestTD,
        "Location": {
            "Latitude": float(lat),
            "Longitude": float(lon),
            "Altitude": {
                "Value": float(alt),
                "Units": "km"
                        },
            "Geoposition": str(geo)
                    },
        "Speed": {
            "Value": speed,
            "Units": "km/s"
                 }
             }
    return nowOut

@app.route('/help', methods=['GET'])
def DS_Help() -> str:
    """
    This route returns the doc strings of each route.

    Returns:
        Dicthelp (str): The string of each route doc-string 
        with its corresponding route call.
    """
    Dicthelp = "/ : " + str(DataSet.__doc__) + "\n" + "/comment : " + str(DS_Com.__doc__) + "\n" + "/header : " + str(DS_Header.__doc__) + "\n" + "/metadata : " + str(DS_Meta.__doc__) + "\n" + "/epochs : " + str(DS_Epochs.__doc__) + "\n" + "\n"  + "/epochs/<epoch> : " + str(DS_SpecificEpoch.__doc__) + "\n"  + "/epochs/<epoch>/speed : " + str(DS_EpochSpeed.__doc__) + "\n"  + "/epochs/<epoch>/location : " + str(DS_EpochLocation.__doc__) + "\n" + "/now : " + str(DS_ClosestEpoch.__doc__) + "\n" + "/help : " + str(DS_Help.__doc__) + "\n" + "/delete-data : " + str(DS_Delete.__doc__) + "\n" + "/post-data : " + str(DS_Post.__doc__) + "\n"

    return Dicthelp

@app.route('/delete-data', methods=['DELETE'])
def DS_Delete() -> str:
    """
    This route deletes the data set in the global variable.

    Returns:
        ISSD (list): an empty list to represent that the data 
        has been cleared from its variable.
    """
    global ISSD
    ISSD.clear()
    return ISSD

@app.route('/post-data', methods=['POST'])
def DS_Post() -> str:
    """
    This route uploads the data set to the global variable. 

    Returns:
        ISSData (dict): The dictionary for the entire data set.
    """
    global ISSD
    APIReq = requests.get(url='https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml')
    ISSData = xmltodict.parse(APIReq.text)
    
    return ISSData

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

