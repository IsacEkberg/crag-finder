""" URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.contrib.staticfiles import views
from django.conf.urls import url, include
from django.conf import settings

from .views import development_index, development_api_mock
from django_api.admin import cragfinder_admin_site
urlpatterns = [
    url(r'^admin/', cragfinder_admin_site.urls),
    url(r'^api/', include('django_api.urls'))
]


if settings.DEBUG:
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', views.serve),
        url(r'^$', view=development_index, name="development index")
    ]
