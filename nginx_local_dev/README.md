# Nginx
Use nginx as a reverse proxy to serve both the django app 
and the ember app. The reason is to avoid CORS.
 
Make sure Nginx is installed (or install it):
nginx -v
sudo apg-get install nginx

Copy the file nginx.conf in this folder to /etc/nginx/ (On Ubuntu)

Restart the service:
sudo services nginx restart

Now to access the app:
- Run ember with: 'ember serve' on 127.0.0.1:4200
- Run django with: 'python manage.py runserver' on 127.0.0.1:8000

The website is now accessible on 127.0.0.1:1337

## Why?
The .conf file contains redirect rules for requests. So /admin and /api goes to django.

Making CORS requests to django is not supported currently, as django-cors-header is not 
maintained. So this setup makes sense. 
