from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from django_api import views

router = DefaultRouter()
router.register(r'areas', views.AreaViewSet)
router.register(r'rockfaces', views.RockFaceViewSet)
router.register(r'routes', views.RouteViewSet)
router.register(r'parkings', views.ParkingViewSet)
router.register(r'clubs', views.ClubViewSet)
router.register(r'areaimages', views.AreaImageViewSet)
router.register(r'rockfaceimages', views.RockFaceImageViewSet)
router.register(r'accessdata', views.AccessViewSet)
router.register(r'routenodes', views.RouteNodeViewSet)

urlpatterns = [
    url(r'^v1/', include(router.urls)),
    url(r'^auth-login/', include('rest_framework.urls')),
    url(r'v1/routenodes/save/(?P<pk>[0-9]+)/$', view=views.save_route_nodes, name="save routenode")
]
