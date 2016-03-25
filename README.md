
[![Circle CI](https://circleci.com/gh/IsacEkberg/crag-finder.svg?style=svg)](https://circleci.com/gh/IsacEkberg/crag-finder)

Crag-finder
============================================
Ember & Django Webapps. Deploys to AWS using Elasticbeanstalk, S3 and cloudfront.
 
Ember is the front_end app, django backend. Local dev enviroment is setup using nginx. 

Starting your project
---------------------

##Install dependecies:
###Node, Npm

`sudo npm install -g npm`

`sudo npm cache clean -f`

`sudo npm install -g n`

`sudo n stable`

`sudo ln -sf /usr/local/n/versions/node/<VERSION>/bin/node /usr/bin/node`

###Ember
`sudo npm install -g ember-cli@2.4`

###Virtualenv 
Is used in order to run the django app. 

###Nginx
See the README.md in crag-finder/nginx. 

##Start a local server
1. Make sure Nginx is running att 127.0.0.1:1337
2. In a terminal, start ember by running (from crag-finder/ember_app)
`ember server`
3. In another terminal, start django:
`python manage.py runserver`
4. Enter 127.0.0.1:1337

