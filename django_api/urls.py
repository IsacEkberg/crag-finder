from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from django_api import views

router = DefaultRouter()
router.register(r'areas', views.AreaViewSet)
router.register(r'rockfaces', views.RockFaceViewSet)
router.register(r'routes', views.RouteViewSet)
router.register(r'parkings', views.ParkingViewSet)

urlpatterns = [
    url(r'^v1/', include(router.urls)),
    url(r'^auth-login/', include('rest_framework.urls'))
]
