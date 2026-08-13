from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from courses.models import Course
from .serializers import CourseSerializer
from django.shortcuts import get_object_or_404

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class CourseListAPIView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = CourseSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
class CourseDetailAPIView(APIView):

    def get(self, request, id):
        course = get_object_or_404(Course, id=id)
        serializer = CourseSerializer(course)

        return Response(serializer.data)

    def put(self, request, id):
        course = get_object_or_404(Course, id=id)

        serializer = CourseSerializer(
            course,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, id):
        course = get_object_or_404(Course, id=id)

        serializer = CourseSerializer(
            course,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, id):
        course = get_object_or_404(Course, id=id)

        course.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )