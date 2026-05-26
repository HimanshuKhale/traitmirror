from django.urls import path

from . import views

urlpatterns = [
    path('questions/next/', views.next_question_api, name='next_question_api'),
    path('answers/', views.answer_api, name='answer_api'),
    path('complete/', views.complete_api, name='complete_assessment_api'),
]
