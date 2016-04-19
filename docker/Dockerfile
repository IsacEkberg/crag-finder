# Base python 3.4 build, inspired by https://github.com/Pakebo/eb-docker-django-simple
# Python 3.4 | Django

FROM python:3.4
MAINTAINER Isac Ekberg (isac.ekberg@gmail.com)

##############################################################################
# Environment variables
##############################################################################
# Get noninteractive frontend for Debian to avoid some problems:
#    debconf: unable to initialize frontend: Dialog
ENV DEBIAN_FRONTEND noninteractive

##############################################################################
# OS Updates and Python packages
##############################################################################

RUN apt-get update \
    && apt-get upgrade -qq -y \
    && apt-get install -qq -y

RUN apt-get install -y -qq apt-utils
# Libs required for geospatial libraries on Debian...
RUN apt-get -y -qq install binutils libproj-dev gdal-bin

##############################################################################
# A Few pip installs not commonly in requirements.txt
##############################################################################

RUN apt-get install -y -qq nano wget
# build dependencies for postgres and image bindings
RUN apt-get install -y -qq python-imaging python-psycopg2

##############################################################################
# setup startup script for gunicord WSGI service
##############################################################################

RUN groupadd webapps
RUN useradd webapp -G webapps
RUN mkdir -p /var/log/webapp/ && chown -R webapp /var/log/webapp/ && chmod -R u+rX /var/log/webapp/
RUN mkdir -p /var/run/webapp/ && chown -R webapp /var/run/webapp/ && chmod -R u+rX /var/run/webapp/


##############################################################################
# Install and configure supervisord
##############################################################################

RUN apt-get install -y -qq supervisor
RUN mkdir -p /var/log/supervisor
ADD ./supervisor_conf.d/webapp.conf /etc/supervisor/conf.d/webapp.conf

##############################################################################
# Install node and npm: https://github.com/nodesource/distributions
##############################################################################
# Install nodejs:
RUN curl -sL https://deb.nodesource.com/setup_5.x | bash -
RUN apt-get install -y -qq nodejs
# Update npm:
# RUN npm install npm -g

##############################################################################
# Install compass
##############################################################################
RUN apt-get install -y -qq ruby ruby-dev
RUN gem install -N compass

##############################################################################
# Install dependencies and run scripts.
##############################################################################
RUN npm install -g ember-cli@2.4
RUN npm install -g bower

# If the add file is not modified can the steps following be cached. => npm install doesn't take forever.
ADD requirements.txt    /var/projects/mysite/requirements.txt
WORKDIR /var/projects/mysite
RUN pip install -r requirements.txt

#ADD ember_app   /var/projects/mysite
ADD ember_app/.bowerrc      /var/projects/mysite/ember_app/.bowerrc
ADD ember_app/bower.json    /var/projects/mysite/ember_app/bower.json
ADD ember_app/package.json  /var/projects/mysite/ember_app/package.json

WORKDIR /var/projects/mysite/ember_app
RUN npm install
RUN bower install --allow-root

ADD mysite.tar      /var/projects/mysite
RUN ember build --environment production

WORKDIR /var/projects/mysite
##############################################################################
# Run start.sh script when the container starts.
# Note: If you run migrations etc outside CMD, envs won't be available!
##############################################################################
CMD ["sh", "./docker/container_start.sh"]

# Expose listen ports
EXPOSE 8002