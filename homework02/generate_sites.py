import json
import random
from typing import List

SyrtisMajor = {}
SyrtisMajor['Sites'] = []

for i in range(1,6):
    Lat = random.uniform(16.0,18.0)
    Long = random.uniform(82.0,84.0)
    compNum = random.randint(1,3)
    if (compNum == 1):
        Comp = "Stony"
    elif (compNum == 2):
        Comp = "Iron"
    else:
        Comp = "Stony-iron"

    SyrtisMajor['Sites'].append( {'Site_ID': i, 'Latitude': Lat, 'Longitude': Long, 'Composition': Comp})

with open('SyrtisMajor.json', 'w') as out:
    json.dump(SyrtisMajor, out, indent=2)
