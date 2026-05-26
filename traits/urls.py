from django.urls import path

from . import views

urlpatterns = [
    path('ideal-profile/', views.ideal_profile, name='ideal_profile'),
]
