from django.urls import path

from .views import (
    CourseListAPIView,
    CourseDetailAPIView,
    EnrollmentListAPIView,
    EnrollmentDetailAPIView,
)


urlpatterns = [

    # Course endpoints
    path(
        'courses/',
        CourseListAPIView.as_view(),
        name='api_course_list'
    ),

    path(
        'courses/<int:id>/',
        CourseDetailAPIView.as_view(),
        name='api_course_detail'
    ),

    # Enrollment endpoints
    path(
        'enrollments/',
        EnrollmentListAPIView.as_view(),
        name='api_enrollment_list'
    ),

    path(
        'enrollments/<int:id>/',
        EnrollmentDetailAPIView.as_view(),
        name='api_enrollment_detail'
    ),
]