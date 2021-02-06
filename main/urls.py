from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='main-home'),
    path('eyebrowSim/', views.eyebrowSim, name='main-eyebrowSim'),
    path('eyebrowResult/', views.eyebrowResult, name='main-eyebrowSim'),
]