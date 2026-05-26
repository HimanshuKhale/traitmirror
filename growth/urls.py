from django.urls import path

from . import views

urlpatterns = [
    path('daily-plan/', views.daily_plan, name='daily_plan'),
    path('practice-event/', views.practice_event, name='practice_event'),
]
