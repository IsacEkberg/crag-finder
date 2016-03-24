from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from django_api import views

router = DefaultRouter()
router.register(r'rentals', views.RentalViewSet)

urlpatterns = [
    url(r'^v1/', include(router.urls)),
    url(r'^auth-login/', include('rest_framework.urls'))
]
