import json
import requests
import math

from typing import List
def CurrentTurb(TurbData: List[dict], KeyConst: str, KeyDetector: str) -> float:
    """This function takes in Turbidity data and calculates the turbidity average of 
    the 5 most recent data points.

    This function takes specific data values, based off of the keys given, from the 
    provided dictionary in order to get the last 5, since our Web API File is ordered 
    from oldest to newest, data points. This value is then divided by 5 seeing as we 
    want the average of the Turbidity. Our calculation is done by taking the calbration 
    constant and 90 degree detector current of each data point and multiplying them together.

    Args:
        TurbData (List[dict]): The wanted Turbidity data dictionary.
        KeyConst (str): The calibration constant Keystring from the dictionary.
	KeyDetector (str): The 90 degree detector current Keystring from the dictionary.

    Returns:
        Tavg (float): The average Turbidity data of the 5 most recent
        data points rounded to 4 decimal places.
    """
    
    #T = a0 * I90
    T = 0
    for i in range(1,6):
        T += TurbData[-i][KeyConst] * TurbData[-i][KeyDetector]
    
    Tavg = round((T/5),4)

    return(Tavg)

def MinTime(CurrT: float) -> float:
    """This function takes in a value and calculates the minimum time 
	needed in order to reach below the safe water threshold.

	This function takes in the specific calculated Turbidity average
	and is ran ONLY when the Turbidity average is above the safe
	water threshold, which in this case was 1 NTU. 
	For the sake of simplification I will be using these nicknames 
	for these variables; Ts = Safe Water Threshold, To = Current
	Turbidity (average), DpH = Decay per Hour.
	I used the equation log(Ts/To)/log(1-DpH) this is with respect to
	my already stated variable constants such as the Ts and DpH.
	
	Args:
	    CurrT (float): The average Turbidity of the most recent 5
	    data points.

	Returns: 
	    Time (float): The minimum amount of time needed to reach 
	    below the Safe water threshold.    
    """

    #B = log(Ts-To)/log(1-d)
    DpH = 0.02
    SafeT = 1

    Time = round((math.log(SafeT/CurrT)/math.log(1-DpH)),2)
    
    return(Time)


def main():
    APIReq = requests.get(url='https://raw.githubusercontent.com/wjallen/turbidity/main/turbidity_data.json')
    TurbData = APIReq.json()
    TD = TurbData['turbidity_data'] #Just a small shortcut
    
    Tavg =  CurrentTurb(TD, 'calibration_constant', 'detector_current')
    
    if Tavg <= 1:
        print("Average turbidity based on the most recent five measurements = " + str(Tavg) + " NTU \nInfo: Turbidity is below threshold for safe use \nNo time required to reach threshold")
    else:
        print("Average turbidity based on the most recent five measurements = " + str(Tavg) + " NTU \nWarning: Turbidity is above threshold for safe use \nThe minimum time required to return below a safe threshold = " + str(MinTime(Tavg)) + " hours")

if __name__ == '__main__':
    main()
