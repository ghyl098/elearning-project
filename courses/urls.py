from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('create/', views.course_create, name='course_create'),
    path('enroll/', views.enroll_view, name='enroll'),
    path('grades/', views.grade_list, name='grade_list'),
    path('grades/add/', views.grade_add, name='grade_add'),
    path('routines/', views.routine_list, name='routine_list'),
    path('routines/add/', views.routine_add, name='routine_add'),
]