#! /bin/bash

git archive -o docker/mysite.tar HEAD
docker build -t cragfinder/development:latest --rm docker
rm -f docker/mysite.tar
docker run --env-file docker/local_env.conf -p 1337:8002 -d crag-finder/development:latest

echo "The container is now available att localhost:1337"