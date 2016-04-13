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
from django.contrib import admin
from django.contrib.staticfiles import views
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static

from .views import development_index, development_api_mock, reset, reset_done, reset_confirm, reset_complete

urlpatterns = [
    url(r'^admin/password_reset_admin/$', view=reset, name='admin_password_reset'),
    url(r'^admin/password_reset/$', view=reset, name='password_reset'),
    url(r'^admin/password_reset/done/$', view=reset_done, name='password_reset_done'),
    url(r'^admin/password_reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', view=reset_confirm, name='password_reset_confirm'),
    url(r'^admin/password_reset/complete/$', view=reset_complete, name='password_reset_complete'),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('django_api.urls'))
]


if settings.DEBUG:
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', views.serve),
        url(r'^$', view=development_index, name="development index")
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
