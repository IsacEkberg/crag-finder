#! /bin/bash
cp requirements.txt docker/requirements.txt
mkdir -p docker/ember_app
cp ember_app/.bowerrc docker/ember_app/.bowerrc
cp ember_app/bower.json docker/ember_app/bower.json
cp ember_app/package.json docker/ember_app/package.json
git archive -o docker/mysite.tar HEAD
docker build -t cragfinder/local:latest -t cragfinder/local:1.0 --rm docker
rm -f docker/mysite.tar
rm docker/requirements.txt
echo docker run --env-file docker/local_env.conf -p 7331:8002 cragfinder/local:latest

echo "The container is then available at localhost:7331"