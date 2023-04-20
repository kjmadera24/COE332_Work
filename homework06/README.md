
## Jeans- I Mean Genes and Manipulating HGNC Data

<p> This homework directory includes one python script that has all of the app
routes needed to get different attributes from this Data set. This is
important seeing as when given a data set online, especially one as large as this
one, it can become very cumbersome to go through the data manually. <br>
In order to access the data you must go to the [HGNC website](https://www.genenames.org/download/archive/) and download one of the two formats provided, in this homework the [Json format](https://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/json/hgnc_complete_set.json) was used. </p>

#### Flask App

The flask app accesses the data set from the web and converts it from xml to a 
manipulatable python dictionary. It includes 7 different app routes as described below.
In order to run the flask app you must pull the docker file from docker hub with the 
`docker pull kamimadera24/iss_tracker:HW05` command in the terminal, then in a new terminal 
window you will type your curl commands with the different routes depending on what you want to achieve.

#### Docker File

The docker file is pushed onto docker hub and as stated above you will need to pull it with the command
` docker pull kamimadera24/iss_tracker:HW05` in order to run the iss_tracker script with the Flask app.
After pulling the docker file you will need to run it within your terminal with the simple command of
` docker run -it --rm -p 5000:5000 kamimadera24/iss_tracker:HW05`, in the event of wanting to pull someone elses docker file you must change the call to `docker pull username/filename:tag` same with the run command
`docker run...username/filename:tag`.

#### App Routes

***After running the dockerfile you will be able to type in these app routes into a different terminal window.***

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
