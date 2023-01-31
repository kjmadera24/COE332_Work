import json
import math

def calc_gcd(latitude_1, longitude_1, latitude_2, longitude_2):
    mars_radius = 3389.5    # km
    lat1, lon1, lat2, lon2 = map( math.radians, [latitude_1, longitude_1, latitude_2, longitude_2] )
    d_sigma = math.acos( math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(abs(lon1-lon2)))
    return ( mars_radius * d_sigma )

def calc_TimeTravel(Distance):
    BotSpeed = 10
    Time = round(Distance/BotSpeed,2)
    return (Time)

def calc_CompTime(Comp):
    if(Comp == 'Stony'):
        CompTime = 1
    elif(Comp == 'Iron'):
        CompTime = 2
    else:
        CompTime = 3

    return(CompTime)

def main():
    with open('SyrtisMajor.json', 'r') as f:
        SM_data = json.load(f)
    
    BotLat = 16.0
    BotLong = 82.0
    TotalTime = 0.
    for i in range(len(SM_data['Sites'])):
        SiteNum = SM_data['Sites'][i]['Site_ID']
        SiteTime =  calc_TimeTravel(calc_gcd(BotLat, BotLong, SM_data['Sites'][i]['Latitude'], SM_data['Sites'][i]['Longitude']))
        SiteComp = calc_CompTime(SM_data['Sites'][i]['Composition'])

        print("Site = " + str(SiteNum) + ", time to travel = " + str(SiteTime) + " hrs, time to sample = " + str(SiteComp) + " hours")

        TotalTime += SiteTime + SiteComp
        BotLat = SM_data['Sites'][i]['Latitude']
        BotLong = SM_data['Sites'][i]['Longitude']

    TotalTime = round(TotalTime,2)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    NumSites = len(SM_data['Sites'])
    print("Number of Sites = " + str(NumSites) + ", Total time = " + str(TotalTime) + " Hours")

if __name__ == '__main__':
    main()
