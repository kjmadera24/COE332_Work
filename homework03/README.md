The Need for Water Analysis

In this directory I have 2 files, my Water Analayis file and my testing file 
for the Water Analaysis file. Turbidity is when particles in water dissolve causing
a cloudy/dirty look to the water. This turbidity can cause a negative impact on
wildlife and tourists if it gets high enough, aka goes above the safe water threshold
of the specific body of water, therefore we need to calculate the recent turbidity 
average in order to know whether it is at a safe enough turbidity value.

The Turbidity data that I used to run my calculations and based my code off of was
the given Web API file https://raw.githubusercontent.com/wjallen/turbidity/main/turbidity_data.json. If you hold CTRL and left-click the link I provided, or copy paste it into your browser it will
open the data file I used. This data set is ordered from oldest to newest data points since February
1st and is updated every hour. it includes different data values(keys) including a calibration constant,
detector current, and etc. It is in a dictionary list format where each data point is in the 
"turbidity_data" Key.

My Water Analysis python script has 2 functions, one that calculates the average turbidity of the
most recent 5 data points and the other calculates the minimum time required to reach below the
safe water threshold. My test python script just has expected value tests for both of my Water
Analysis python script functions.

In order to run my code you just type "python3 WaterAnalysis.py" and it will print something
like this based on the results,
	Average turbidity based on the most recent five measurements = 0.7261 NTU
	Info: Turbidity is below threshold for safe use
	No time required to reach threshold 
The first line of this output is directed to the first function where I calculated the Turbidity
average as you can see it states what that average value was. The 2nd line then tells you whether 
it is below the threshold, in this case 1 NTU, by displaying whether the water is safe to use and
or if it isnt. The final line will display the minimum time required that was calculated with my
2nd function IF the average is below the threshold. 
