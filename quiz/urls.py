from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('quiz/c/', views.quiz_c, name='quiz_c'),
    path('quiz/python/', views.quiz_python, name='quiz_python'),
    path('quiz/java/', views.quiz_java, name='quiz_java'),
    path('quiz/js/', views.quiz_js, name='quiz_js'),

    
    path('download/<str:subject_name>/', views.download_pdf, name='download_pdf'),
    path('submit/<str:subject_name>/', views.submit_quiz, name='submit_quiz'),
    path('next/<str:subject_name>/', views.next_subject, name='next_subject'),
    path('end/', views.end_quiz, name='end_quiz'),
]
