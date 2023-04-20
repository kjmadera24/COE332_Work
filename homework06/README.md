
## Jeans- I Mean Genes and Manipulating HGNC Data

This homework directory includes one python script that has all of the app
routes needed to get different attributes from this Data set. This is
important seeing as when given a data set online, especially one as large as this
one, it can become very cumbersome to go through the data manually.
In order to access the data you must go to the [HGNC website][1] and download one of the two formats provided, in this homework the [Json format][2] was used.

[1]: <https://www.genenames.org/download/archive/> "HGNC link"
[2]: <https://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/json/hgnc_complete_set.json> "Json Link"

#### Flask App

The flask app accesses the data set from the web and uploads it to a redis database where the user can manipulate the data through. It includes 3 different app routes 
as described below.
In order to run the flask app you must either pull the docker file from docker hub 
with the `docker pull kamimadera24/gene_api:1.0` command in the terminal or simply 
pull the data from the repository. Then in a new terminal window you will type your curl commands with the different routes depending on what you want to achieve.

#### Docker Compose

The docker-compose file makes it easier to use the Dockerfile without typing in 
all the commands but one would need to pull the repository in order to run the file.
Once having pulled the repository and having the docker-compose file the user can
type `docker-compose up --build` in order to build and run the dockerfile. <br>
*Note: if you edit the gene_api.py file you must take down the docker-compose file 
with * `docker-compose down` * then build and run it again. This will update the 
docker file allowing the use of any new additions and or edits made.*

#### Docker File

The docker file is pushed onto docker hub and as stated above you will need to pull it with the command ` docker pull kamimadera24/iss_tracker:HW05` in order to run th
gene_api script with the Flask app. After pulling the docker file you will need to 
run it within your terminal with the simple command of 
`docker run -it --rm -p 5000:5000 kamimadera24/gene_api:1.0`, in the event of 
wanting to pull someone elses docker file you must change the call to 
`docker pull username/filename:tag` same with the run command
`docker run...username/filename:tag`.

#### App Routes

***After running the dockerfile/dockercompose you will be able to type in these app routes into a different terminal window.***

* `curl localhost:5000/data` This app route will let you do 3 things with the entire
data set depending on which route method you use.
	* `curl localhost:5000/data -X POST` in this case the user uploads the 
data set to the redis database.
	* `curl localhost:5000/data -X GET` in this case the user retrieves the 
data set from the database and prints it.
	* `curl localhost:5000/data -X DELETE` in this case the user deletes the
contents in the database.

* `curl localhost:5000/genes` This app route will return all the hgnc_ids from the
data set in a list.

* `curl localhost:5000/genes/<hgnc_id>` This app route asks for an input of a 
string. the string should be a specific hgnc_id from the list provided in the
previous route. The information for the corresponding id will be returned.
