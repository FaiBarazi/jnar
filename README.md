* Run docker compose to build all the services:
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
> mongo -u flaskuser -p flaskpass --authenticationDatabase flaskdb;
> exit
`

* Copy the 2 data json files to mongodb container:
`
$ docker cp data/DVDRentals-customers.json mongodb:/tmp/customers.json
$ docker cp data/DVDRentals-films.json  mongodb:/tmp/films.json
`

* Import the 2 json files into flaskdb as 2 collections:
`
$ docker exec -i mongodb sh -c 'mongoimport -d flaskdb -c customers -u flaskuser -p flaskpass --file /tmp/customers.json --drop'
$ docker exec -i mongodb sh -c 'mongoimport -d flaskdb -c films -u flaskuser -p flaskpass --file /tmp/films.json --drop'
`
**NOTE**:
When removing the containers using `$ docker-compose rm -s -v`and redeploying, make sure to prune
the unused volumes by `$ docker volume prune`


