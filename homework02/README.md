		Homework 2: Data Analyzation and Simulation

In this homework02 directory I have 2 python files; one that generates data
(into a Json file), and the other that analyzes the data. By making the Json
file I create the flexibility of having the dictionaries with specific key 
values to interact with specific values when needed.

My "generate_sites" script is self explanatory but it specifically makes a 
Json file that generates sites with random Latitude and Longitudes in a set 
range, and a Composition randomly chosen from 3 types. These "Sites" are 
separated being placed into their own dictionaries. 
My "calculate_trip" script is where I make the calculations for these Sites 
when simulating a robot that travels at 10 km/hr traveling and taking 
samples from each site. I calculate the distance from each starting to 
ending point, the time it takes to travel that distance, and the amount of 
time it takes to get a sample from each site.

To run the code you simply first type "python3 generate_sites.py" in the 
command lineand it will add a Json file to the directory, in this file you 
can see the different specific dictionaries for each site we randomly 
generated. We now want to analyze the data and we do so by typing 
"python3 calculate_trip.py", this gives us the calculations for each site
and the ending calculation for the total sites and time analyzed.
