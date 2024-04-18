
## Evaluation and Calculation of Trajectory data

This project gives the ability to manipulate real data from the internet and make calculations for 
the latitude, longitude, altitude, geoposition, and speed. When analyzing data like this you are going to want to analyze the characteristics of specific data values to make calculations such as those stated above and get further information from the recorded data. Having a python script such as this one gives the flexibility of having recent data easily rather than a set time frame or values. In order to access the data you can go to the website *https://spotthestation.nasa.gov/trajectory_data.cfm* and download one of the two formats provided.

#### Flask App

The flask app accesses the data set from the web and converts it from xml to a manipulatable python dictionary. It includes 12 different app routes as described below.
In order to run the flask app you must pull the docker file from docker hub with the `docker pull kamimadera24/iss_tracker:HW05` command in the terminal, then in a new terminal window you will type your curl commands with the different routes depending on what you want to achieve.

#### Docker File

The docker file is pushed onto docker hub and as stated above you will need to pull it with the command ` docker pull username/filename:tag` <p> in order to run the iss_tracker script with the Flask app.
After pulling the docker file you will need to run it within your terminal with the simple command of ` docker run -it --rm -p 5000:5000 username/filename:tag`, in order to pull Kami's docker file you would change the call to `docker pull kamimadera24/iss_tracker:MTProj` same with the run command `docker run...kamimadera24/iss_tracker:MTProj`.

**Your screen should look something like this if it succesfully pulled**
> MTProj: Pulling from kamimadera24/iss_tracker
> Digest: sha256:f7f4a255d641bbeb0b01be9b7d524c1bb335491ab3363dd2ba3d1bde8c6e39fb
> Status: Image is up to date for kamimadera24/iss_tracker:MTProj
> docker.io/kamimadera24/iss_tracker:MTProj

**After using the run command you should then get this**
> <p> * Serving Flask app 'iss_tracker' </p>
> <p> * Debug mode: on </p>
> <p> ...
> <p> * Debugger is active! </p>
> <p> * Debugger PIN: 858-942-451 </p>

#### App Routes

***After running the dockerfile you will be able to type in these app routes into a different terminal window.***

* `curl localhost:5000/` this will return the entire data set which will include multiple *stateVectors* dic	tionaries with 7 key values each; *EPOCH, X, Y, Z, X_DOT, Y_DOT, and Z_DOT*.

* `curl localhost:5000/comment` this will return the comments made in the data set, inlcuding things such as the units, some constant values, and other things.

* `curl localhost:5000/header` this app route will return the header of the data set, which inlcudes the Date the data was created and the originator.

* `curl localhost:5000/metadata` this returns the metadata from the data set with characteristics about the object.

* `curl localhost:5000/epochs` this app route will return a list of all the epochs (time stamps) in the current file. They will look something like this, *2023-051T15:07:32.948Z*.
	* `curl localhost:5000/epochs?limit=<int>` in the case that only a certain number of epoch outputs is wanted, a limit can be established to only print the inputted number of outputs.
	* `curl localhost:5000/epochs?offset=<int>` in the case that epochs from a specific starting point are wanted, an offset can be established to output the epochs from the inputted index number.
	* `curl "localhost:5000/epochs?limit=<int>&offset=<int>"` in the event that both a *limit* and *offset* are wanted you must enclose the localhost line in quotations and input the values for said parameters.

* `curl localhost:5000/epochs/<epoch>` this specific route asks for an input that you want, the way this route was coded it only accepts a string value of the specific time stamp wanted. For example with the epoch *2023-051T15:07:32.948Z* you would type `curl localhost:5000/epochs/**2023-051T15:07:32.948Z**` rather than a number. This will return the stateVector corresponding to the inputted time stamp. This will look similar to the first app route output but it will only contain one stateVector.

* `curl localhost:5000/epochs/<epoch>/speed` this app route will calculate the speed based off of the X,Y, and Z_DOT values in the specific stateVectorwanted. For example calling *curl localhost:5000/epochs/2023-051T15:07:32.948Z/speed* will give you the value 7.5468. 

* `curl localhost:5000/epochs/<epoch>/location` this route will calculate the latitude, longitude, altitude, and geoposition of the specific epoch based off of its X,Y, and Z values. For example *curl localhost:5000/epochs/2023-084T11:08:00.000Z/location* will return
` {
 "Altitude": 655.6382379151719,
 "Geoposition": "Somewhere over water",
 "Latitude": 6.097665442280389,
 "Longitude": -112.72245100740523
  } `

* `curl localhost:5000/help` this app route will provide the doc-strings for each app route and the corresponding app route in case of clarification for which route does what.

* `curl localhost:5000/delete-data -X DELETE` this app route clears the current data set.

* `curl localhost:5000/post-data -X POST` this app route redownloads the data set and assigns it to the global variable for reuse.
