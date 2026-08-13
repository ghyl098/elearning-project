from django.urls import path
from .views import CourseListAPIView, CourseDetailAPIView


urlpatterns = [
    path('courses/', CourseListAPIView.as_view(), name='api_course_list'),
    path('courses/<int:id>/', CourseDetailAPIView.as_view(), name='api_course_detail'),
]