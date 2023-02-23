
##Evaluation and Calculation of Trajectory data

This homework directory includes one python script that has all of the app
routes needed to get the different attributes or caclualtions wanted. This is
important seeing as when given a data set online its more likely that it will
update over time, with these routes it gives easy access to manipulate the
conetnt.
In order to access the data you must go to the website 
*https://spotthestation.nasa.gov/trajectory_data.cfm* and download one of the 
two formats provided.

**Flask App**
The flask app accesses the data set from the web and converts it from xml to a 
manipulatable python dictionary. It includes 4 different app routes; one that 
returns the entire data set, returns only the epochs in the set, returns the
state vector from the inputted epoch, and the speed of the inputted epoch.
In order to run the flask app you must type `flask --app ISS_Data --debug run`
in the terminal, then in a new terminal window you will type `curl localhost:5000/` 
followed by other routes depending on what you want to achieve.

