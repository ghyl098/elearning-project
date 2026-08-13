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
    path('notices/', views.notice_list, name='notice_list'),
    path('notices/add/', views.notice_add, name='notice_add'),
    path('notices/<int:pk>/delete/', views.notice_delete, name='notice_delete'),
    path('<int:pk>/edit/', views.course_edit, name='course_edit'),
    path('<int:pk>/delete/', views.course_delete, name='course_delete'),
    path('<int:pk>/', views.course_detail, name='course_detail'),
    path('<int:pk>/lessons/add/', views.lesson_add, name='lesson_add'),
    path('grades/add/', views.grade_add, name='grade_add'),
    path('grades/<int:pk>/edit/', views.grade_edit, name='grade_edit'),
    path('grades/<int:pk>/delete/', views.grade_delete, name='grade_delete'),
    path('routines/add/', views.routine_add, name='routine_add'),
    path('routines/<int:pk>/edit/', views.routine_edit, name='routine_edit'),
    path('routines/<int:pk>/delete/', views.routine_delete, name='routine_delete'),
]