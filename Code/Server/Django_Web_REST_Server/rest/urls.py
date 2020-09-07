from django.urls import include, path
from rest_framework import routers

from rest import views
#
# router = routers.DefaultRouter()
# router.register(r'devices', views.DeviceViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('iptables-conf/<int:pk>/', views.IPTablesDeviceDetail.as_view()),
    path('stage1/devices/<int:pk>/', views.Stage1DeviceDetail.as_view()),
    #browsable api security flaws
    #path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
