from django.contrib import admin
from django.contrib.staticfiles import views
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from captcha import urls as captcha_urls

from .views import development_index, development_api_mock, reset, reset_done, reset_confirm, reset_complete
from django_api.views import new_user_view


urlpatterns = [
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^admin/password_reset_admin/$', view=reset, name='admin_password_reset'),
    url(r'^admin/password_reset/$', view=reset, name='password_reset'),
    url(r'^admin/password_reset/done/$', view=reset_done, name='password_reset_done'),
    url(r'^admin/password_reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', view=reset_confirm, name='password_reset_confirm'),
    url(r'^admin/password_reset/complete/$', view=reset_complete, name='password_reset_complete'),
    url(r'admin/captcha/', include(captcha_urls)),
    url(r'^admin/create_account/$', view=new_user_view, name="create_account"),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('django_api.urls'))
]


if settings.DEBUG:
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', views.serve),
        url(r'^$', view=development_index, name="development index")
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
