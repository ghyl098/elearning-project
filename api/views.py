from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from courses.models import Course, Enrollment, Routine
from .serializers import CourseSerializer, EnrollmentSerializer, RoutineSerializer

from django.shortcuts import get_object_or_404

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated



# COURSE API


class CourseListAPIView(APIView):

    # Require a valid DRF token for all course-list requests
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Any authenticated user can view available courses
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)

        return Response(serializer.data)

    def post(self, request):
        # Only teachers can create courses
        if request.user.role != 'teacher':
            return Response(
                {'detail': 'Only teachers can create courses.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = CourseSerializer(data=request.data)

        if serializer.is_valid():
            # Automatically assign the logged-in teacher as owner
            serializer.save(teacher=request.user)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class CourseDetailAPIView(APIView):

    # Require authentication for course details
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        # Authenticated teachers and students can view a course
        course = get_object_or_404(Course, id=id)
        serializer = CourseSerializer(course)

        return Response(serializer.data)

    def put(self, request, id):
        course = get_object_or_404(Course, id=id)

        # Only the teacher who owns the course can modify it
        if course.teacher != request.user:
            return Response(
                {'detail': 'You can only modify your own courses.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = CourseSerializer(
            course,
            data=request.data
        )

        if serializer.is_valid():
            # Keep the logged-in teacher as the course owner
            serializer.save(teacher=request.user)

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, id):
        course = get_object_or_404(Course, id=id)

        # Only the teacher who owns the course can modify it
        if course.teacher != request.user:
            return Response(
                {'detail': 'You can only modify your own courses.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = CourseSerializer(
            course,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            # Keep the logged-in teacher as the course owner
            serializer.save(teacher=request.user)

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, id):
        course = get_object_or_404(Course, id=id)

        # Only the teacher who owns the course can delete it
        if course.teacher != request.user:
            return Response(
                {'detail': 'You can only delete your own courses.'},
                status=status.HTTP_403_FORBIDDEN
            )

        course.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

# ENROLLMENT API

class EnrollmentListAPIView(APIView):

    # Require authentication for enrollment operations
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Only students can view their enrollments
        if request.user.role != 'student':
            return Response(
                {'detail': 'Only students can access enrollments.'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Return only enrollments belonging to the logged-in student
        enrollments = Enrollment.objects.filter(
            student=request.user
        )

        serializer = EnrollmentSerializer(
            enrollments,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):
        # Only students can enroll in courses
        if request.user.role != 'student':
            return Response(
                {'detail': 'Only students can enroll in courses.'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Get the course ID submitted by the student
        course_id = request.data.get('course')

        # Prevent duplicate enrollment
        if Enrollment.objects.filter(
            student=request.user,
            course_id=course_id
        ).exists():
            return Response(
                {'detail': 'You are already enrolled in this course.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = EnrollmentSerializer(data=request.data)

        if serializer.is_valid():
            # Automatically assign the logged-in student
            serializer.save(student=request.user)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class EnrollmentDetailAPIView(APIView):

    # Require authentication for individual enrollment operations
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        # Only students can view enrollment details
        if request.user.role != 'student':
            return Response(
                {'detail': 'Only students can access enrollments.'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Student can only access their own enrollment
        enrollment = get_object_or_404(
            Enrollment,
            id=id,
            student=request.user
        )

        serializer = EnrollmentSerializer(enrollment)

        return Response(serializer.data)

    def delete(self, request, id):
        # Only students can remove their enrollments
        if request.user.role != 'student':
            return Response(
                {'detail': 'Only students can manage enrollments.'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Student can only delete their own enrollment
        enrollment = get_object_or_404(
            Enrollment,
            id=id,
            student=request.user
        )

        enrollment.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
        

# ROUTINE API


class RoutineListAPIView(APIView):

    # Only authenticated users can access routines
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Teachers and students can view routines
        routines = Routine.objects.all()

        serializer = RoutineSerializer(
            routines,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):
        # Only teachers can create routines
        if request.user.role != 'teacher':
            return Response(
                {'detail': 'Only teachers can create routines.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = RoutineSerializer(data=request.data)

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


class RoutineDetailAPIView(APIView):

    # Only authenticated users can access routines
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        # Teachers and students can view a routine
        routine = get_object_or_404(
            Routine,
            id=id
        )

        serializer = RoutineSerializer(routine)

        return Response(serializer.data)

    def put(self, request, id):
        routine = get_object_or_404(
            Routine,
            id=id
        )

        # Only teachers can modify routines
        if request.user.role != 'teacher':
            return Response(
                {'detail': 'Only teachers can modify routines.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = RoutineSerializer(
            routine,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, id):
        routine = get_object_or_404(
            Routine,
            id=id
        )

        # Only teachers can delete routines
        if request.user.role != 'teacher':
            return Response(
                {'detail': 'Only teachers can delete routines.'},
                status=status.HTTP_403_FORBIDDEN
            )

        routine.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )