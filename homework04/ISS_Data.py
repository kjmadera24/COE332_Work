import requests
import xmltodict
from flask import Flask

app = Flask(__name__)

def main():
    APIReq = requests.get(url='https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml')
    ISSData = xmltodict.parse(APIReq.text)
    ISSD = ISSData['ndm']['oem']['body']['segment']['data']['stateVector'])  #Just a small shortcut

    Tavg =  CurrentTurb(TD, 'calibration_constant', 'detector_current')

    if Tavg <= 1:
        print("Average turbidity based on the most recent five measurements = " + str(Tavg) + " NTU \nInfo: Turbidity is below threshold for safe use \nNo time required to reach threshold")
    else:
        print("Average turbidity based on the most recent five measurements = " + str(Tavg) + " NTU \nWarning: Turbidity is above threshold for safe use \nThe minimum time required to return below a safe threshold = " + str(MinTime(Tavg)) + " hours")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
