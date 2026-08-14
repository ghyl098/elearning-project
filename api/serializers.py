from rest_framework import serializers
from courses.models import Course, Enrollment, Routine


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class EnrollmentSerializer(serializers.ModelSerializer):
    # Student is assigned automatically from the logged-in user
    student = serializers.PrimaryKeyRelatedField(read_only=True)

    # Enrollment date is generated automatically by the model
    enrolled_on = serializers.DateField(read_only=True)

    class Meta:
        model = Enrollment
        fields = '__all__'

class RoutineSerializer(serializers.ModelSerializer):
    # Handles course, day, start time and end time
    class Meta:
        model = Routine
        fields = '__all__'