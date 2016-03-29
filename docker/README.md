# Useful docker commands:
To run the container locally, run the script:

`run_local_container.sh`


###SSH:a in till en container (som är igång):
Ta reda på namnet på den:

`sudo docker ps -a`

Ersätt namnet nedan med rätt:

`sudo docker exec -i -t <namnet> bash`

Exec på en circleCI docker (Om man byggt med SSH):

`sudo lxc-attach -n "$(docker inspect --format '{{.Id}}' $MY_CONTAINER_NAME)" -- bash`

###Stoppa en kontainer:
`docker stop <name>`       # (kan tabbas fram)

Rensa kontainers och images:

$ docker rm `docker ps -a -q`

$ docker rmi `docker images -a -q`