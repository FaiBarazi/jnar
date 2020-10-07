# DVD Rental API
* Overview
* Repo content
* Setup
* Server calls
* Acknowledgment

## Overview:
The web service builds 3 containers; flask web application container, nginx server for 
reverse proxy handling and a NoSQL mongodb database for which we import 2 collections to 
manually.

## Repo content:
* docker-compose.yml: docker instructions to handle the deployment of different containers.
* app: Flask web application. 
  * Dockerfile: particular instructions for the web application container setup
  * app.py: The flask app code with the logic of handling the GET calls.
  * requirements.txt: python lib requirements to run the service.
  * wsgi.py: python web server gateway interface ¯\_(ツ)_/¯ .
* nginx: nginx web server container that handles reverse proxy.
  * conf.d: contains app.conf, configuration for nginx and upstream server.
* data: 2 json files that are loaded as collections to MongoDB.

## Setup:
Make sure you have docker and docker-compose installed.
Clone the repo locally and cd to it. 
Then follow these steps:

* Run docker compose to build all the services. the 'd' - detached - flag could be ommited:
`$ docker-compose up -d`

* Run an interactive shell using:
`$ docker exec -it mongodb bash`

* Log in to mongo DB using the root username and password defined in docker-compose.
`$ mongo -u mongodbuser -p mongodbpass`

* Do show dbs to make sure that user has access to admin at the mongo prompt.
`> show dbs;`

* Create a flaskdb with use command
`> use flaskdb;`

* Create db user using the user provided in the docker-cmpose for flask
`
> db.createUser({user: 'flaskuser', pwd: 'flaskpass', roles: [{role: 'readWrite', db: 'flaskdb'}]})
> exit
`
* Log in into authenticated DB with the following, then exit db and interactive shell.
`
$ mongo -u flaskuser -p flaskpass --authenticationDatabase flaskdb;
> exit
`

* Copy the 2 data json files to mongodb container:
`
$ docker cp data/DVDRentals-customers.json mongodb:/tmp/customers.json
$ docker cp data/DVDRentals-films.json  mongodb:/tmp/films.json
`

* Import the 2 json files into flaskdb as 2 collections.:
`
$ docker exec -i mongodb sh -c 'mongoimport -d flaskdb -c customers -u flaskuser -p flaskpass --file /tmp/customers.json --drop'
$ docker exec -i mongodb sh -c 'mongoimport -d flaskdb -c films -u flaskuser -p flaskpass --file /tmp/films.json --drop'
`
## Making server RESTFUL API calls:
We can use `curl`from the command line to the different endpoints.
* Main page call to make sure it is working:
`$ curl -i http://127.0.0.1:80`

* Get all customers(no offset or limit is set here):
`$ curl -i http://127.0.0.1:80/customers`

* Get all films:
`$ curl -i http://127.0.0.1:80/films`

* Get a film by id:
`$ curl -i http://127.0.0.1:80/film/<film_id>`

* Get a customer by id:
`$ curl -i http://127.0.0.1:80/customer/<customer_id>`

## Acknowledgement:
The docker-compose files are provided [here](https://www.digitalocean.com/community/tutorials/how-to-set-up-flask-with-mongodb-and-docker)

**NOTE**:
To stop the service with all the container connections run:
`$docker-compose down`
Note that for the mongodb we are presisting the data using a local volume.

