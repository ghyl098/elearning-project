from django.contrib import admin
from .models import Course, Enrollment, Routine, Grade

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'teacher')
    search_fields = ('name', 'code')
    list_filter = ('teacher',)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_on')
    list_filter = ('course',)

@admin.register(Routine)
class RoutineAdmin(admin.ModelAdmin):
    list_display = ('course', 'day', 'start_time', 'end_time')
    list_filter = ('day', 'course')

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'marks')
    list_filter = ('course',)