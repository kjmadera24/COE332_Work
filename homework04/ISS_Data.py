import requests
import xmltodict
from flask import Flask

app = Flask(__name__)

def main():
    APIReq = requests.get(url='https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml')
    ISSData = xmltodict.parse(APIReq.text)
    ISSD = ISSData['ndm']['oem']['body']['segment']['data']['stateVector'])  #Just a small shortcut

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
