from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from ipam_api import views


urlpatterns = [
    path('ipcalc/calculate', views.calculate_ip),
    path('ipcalc/overlaps', views.overlaps)
]

format_suffix_patterns(urlpatterns)

