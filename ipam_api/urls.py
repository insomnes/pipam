from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from ipam_api import views


urlpatterns = [
    path('ipcalc/test', views.test),
    path('ipcalc/calculate', views.calculate_ip),
    path('ipcalc/equal_to', views.equal_to),
    path('ipcalc/greater_than', views.greater_than),
    path('ipcalc/less_than', views.less_than),
    path('ipcalc/subnet_of', views.subnet_of),
    path('ipcalc/supernet_of', views.supernet_of),
    path('ipcalc/overlaps', views.overlaps)
]

format_suffix_patterns(urlpatterns)
