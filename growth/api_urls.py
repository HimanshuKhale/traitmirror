from django.urls import path

from . import views

urlpatterns = [
    path('daily-plan/', views.daily_plan_api, name='daily_plan_api'),
    path('practice-event/', views.practice_event_api, name='practice_event_api'),
]
