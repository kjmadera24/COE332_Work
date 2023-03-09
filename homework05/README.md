
## Evaluation and Calculation of Trajectory data

<p> This homework directory includes one python script that has all of the app
routes needed to get the different attributes or caclualtions wanted. This is
important seeing as when given a data set online its more likely that it will
update over time, with these routes it gives easy access to manipulate the
content. <br>
In order to access the data you must go to the website ***https://spotthestation.nasa.gov/trajectory_data.cfm*** and download one of the two formats provided. </p>

#### Flask App

<p> The flask app accesses the data set from the web and converts it from xml to a 
manipulatable python dictionary. It includes 4 different app routes; one that 
returns the entire data set, returns only the epochs in the set, returns the
state vector from the inputted epoch, and the speed of the inputted epoch.
In order to run the flask app you must type `flask --app ISS_Data --debug run`
in the terminal, then in a new terminal window you will type `curl localhost:5000/` 
followed by other routes depending on what you want to achieve. </p>

#### App Routes

***After running the flask app you will be able to type in these app routes into a different terminal window.***

* `curl localhost:5000/` this will return the entire data set which will include multiple *stateVectors* dic	tionaries with 7 key values each; *EPOCH, X, Y, Z, X_DOT, Y_DOT, and Z_DOT*.

* `curl localhost:5000/epochs` this app route will return a list of all the epochs (time stamps) in the current file. They will look something like this, *2023-051T15:07:32.948Z*.
	* `curl localhost:5000/epochs?limit=<int>` in the case that only a certain number of epoch outputs is wanted, a limit can be established to only print the inputted number of outputs.
	* `curl localhost:5000/epochs?offset=<int>` in the case that epochs from a specific starting point are wanted, an offset can be established to output the epochs from the inputted index number.
	* `curl "localhost:5000/epochs?limit=<int>&offset=<int>"` in the event that both a *limit* and *offset* are wanted you must enclose the localhost line in quotations and input the values for said parameters.

* `curl localhost:5000/epochs/<epoch>` this specific route asks for an input that you want, the way this route was coded it only accepts a string value of the specific time stamp wanted. For example with the epoch *2023-051T15:07:32.948Z* you would type `curl localhost:5000/epochs/**2023-051T15:07:32.948Z**` rather than a number. This will return the stateVector corresponding to the inputted time stamp. This will look similar to the first app route output but it will only contain one stateVector.

* `curl localhost:5000/epochs/<epoch>/speed` this app route will calculate the speed based off of the X,Y, and Z_DOT values in the specific stateVectorwanted. For example calling *curl localhost:5000/epochs/2023-051T15:07:32.948Z/speed* will give you the value 7.5468. 

* 'curl localhost:5000/help' this app route will provide the doc-strings for each app route and the corresponding app route in case of clarification for which route does what.

* 'curl localhost:5000/delete-data -X DELETE' this app route clears the current data set.

* 'curl localhost:5000/post-data -X POST' this app route redownloads the data set and assigns it to the global variable for reuse.
